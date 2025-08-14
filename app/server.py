from flask import Flask, render_template, request, jsonify
import os, json, requests, time

from engine_adapters import ai_reply, load_settings, save_settings, ensure_dirs
from file_ops import ensure_base, read_json, write_json, read_plist, write_plist, backup_zip, restore_zip, read_file, write_file
from sys_tools import frida_list, run_tool, which
from providers import txt2img_stable_horde, txt2img_a1111, ocr_tesseract, whisper_transcribe
from updater import apply_zip_from_url

APP_DIR = os.path.dirname(__file__)
BASE = "/var/mobile/Media/GOD"

# override support
ovr_templates = os.path.join(BASE, "overrides", "app", "templates")
ovr_static = os.path.join(BASE, "overrides", "app", "static")
tpl_folder = ovr_templates if os.path.exists(ovr_templates) else os.path.join(APP_DIR, "templates")
static_folder = ovr_static if os.path.exists(ovr_static) else os.path.join(APP_DIR, "static")

app = Flask(__name__, template_folder=tpl_folder, static_folder=static_folder)

def app_version():
    vf = os.path.join(APP_DIR, "VERSION")
    try:
        with open(vf, "r", encoding="utf-8") as f:
            return f.read().strip()
    except:
        return "0.0.0"

@app.route("/")
def index():
    ensure_dirs(); ensure_base()
    return render_template("index.html", version=app_version())

@app.route("/ping")
def ping():
    return jsonify({"status":"ok","message":"pong","version":app_version()})

@app.route("/status")
def status():
    info = {
        "base": BASE,
        "dirs": os.listdir(BASE) if os.path.exists(BASE) else [],
        "settings": load_settings(),
        "version": app_version(),
        "tools": {"frida": bool(which('frida-ps'))}
    }
    return jsonify(info)

@app.route("/settings", methods=["GET","POST"])
def settings():
    if request.method == "POST":
        data = request.get_json() or {}
        cur = load_settings(); cur.update(data); save_settings(cur)
        return jsonify({"ok": True, "settings": cur})
    return jsonify(load_settings())

@app.route("/api/ai", methods=["POST"])
def api_ai():
    data = request.get_json() or {}
    prompt = data.get("prompt", "")
    return jsonify({"reply": ai_reply(prompt)})

@app.route("/api/search")
def api_search():
    q = request.args.get("q", "")
    source = request.args.get("source", load_settings().get("search", {}).get("default_source", "ddg"))
    try:
        ua = {"User-Agent":"Mozilla/5.0"}
        if source == "naver":
            r = requests.get("https://m.search.naver.com/search.naver", params={"query": q}, headers=ua, timeout=10)
        elif source == "google":
            r = requests.get("https://www.google.com/search", params={"q": q}, headers=ua, timeout=10)
        else:
            r = requests.get("https://duckduckgo.com/html/", params={"q": q}, headers=ua, timeout=10)
        return jsonify({"ok": True, "source": source, "url": r.url, "html_preview": r.text[:8000]})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route("/api/file/read", methods=["POST"])
def file_read():
    d = request.get_json() or {}; path, typ = d.get("path",""), d.get("type","raw")
    try:
        if typ == "json": return jsonify({"type":"json","data": read_json(path)})
        if typ == "plist": return jsonify({"type":"plist","data": read_plist(path)})
        return jsonify({"type":"raw","data": read_file(path).decode(errors="ignore")})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/file/write", methods=["POST"])
def file_write():
    d = request.get_json() or {}; path, typ = d.get("path",""), d.get("type","raw")
    try:
        if typ == "json": write_json(path, d.get("data", {}))
        elif typ == "plist": write_plist(path, d.get("data", {}))
        else: write_file(path, (d.get("data","") or "").encode())
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/tools/frida")
def api_frida(): return jsonify(frida_list())

@app.route("/api/tools/run", methods=["POST"])
def api_run():
    d = request.get_json() or {}; cmd = d.get("cmd",""); return jsonify(run_tool(cmd))

@app.route("/api/backup")
def api_backup():
    try: path = backup_zip(); return jsonify({"ok": True, "zip": path})
    except Exception as e: return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/restore", methods=["POST"])
def api_restore():
    d = request.get_json() or {}; path = d.get("zip","")
    try: ok = restore_zip(path); return jsonify({"ok": ok})
    except Exception as e: return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/img/txt2img", methods=["POST"])
def api_txt2img():
    d = request.get_json() or {}; prompt = d.get("prompt",""); mode = d.get("mode","horde")
    settings = load_settings()
    if mode == "a1111": return jsonify(txt2img_a1111(prompt, settings.get("imaging",{}).get("a1111_url","")))
    return jsonify(txt2img_stable_horde(prompt, settings.get("imaging",{}).get("stable_horde_url","")))

@app.route("/api/ocr", methods=["POST"])
def api_ocr():
    d = request.get_json() or {}; image_path = d.get("path",""); exe = load_settings().get("av",{}).get("tesseract_path","")
    return jsonify(ocr_tesseract(image_path, exe))

@app.route("/api/whisper", methods=["POST"])
def api_whisper():
    d = request.get_json() or {}; audio_path = d.get("path",""); url = load_settings().get("av",{}).get("whisper_url","")
    return jsonify(whisper_transcribe(audio_path, url))

@app.route("/api/update/check")
def api_update_check(): return jsonify({"ok": True, "version": app_version(), "note": "ZIP URL 설정 후 Update 실행 가능"})

@app.route("/api/update/run", methods=["POST"])
def api_update_run():
    d = request.get_json() or {}; url = d.get("zip_url") or load_settings().get("updater",{}).get("zip_url","")
    if not url: return jsonify({"ok": False, "msg": "zip_url 미설정"})
    res = apply_zip_from_url(url); return jsonify(res)
