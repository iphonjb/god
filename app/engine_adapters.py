import os, json, subprocess, requests, time
BASE = "/var/mobile/Media/GOD"
SETTINGS_PATH = os.path.join(BASE, "data", "settings.json")
DEFAULTS = {
    "engine": "echo",
    "external_url": "",
    "llama": {"exe": os.path.join(BASE, "bin", "llama"), "model": os.path.join(BASE, "models", "model.gguf"), "tokens": 200, "temp": 0.7, "seed": -1},
    "imaging": {"stable_horde_url": "", "a1111_url": ""},
    "av": {"tesseract_path": "/opt/local/bin/tesseract", "ffmpeg_path": "/usr/local/bin/ffmpeg", "whisper_url": ""},
    "updater": {"zip_url": "", "allow_override": True},
    "search": {"default_source": "ddg"}
}
def ensure_dirs():
    for p in ["data","logs","backups","bin","models","tmp","overrides"]:
        os.makedirs(os.path.join(BASE,p), exist_ok=True)
    if not os.path.exists(SETTINGS_PATH): save_settings(DEFAULTS)
def load_settings():
    ensure_dirs()
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f: s = json.load(f)
    except: s = {}
    out = DEFAULTS.copy(); out.update(s); return out
def save_settings(obj):
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f: json.dump(obj, f, ensure_ascii=False, indent=2)
def reply_echo(prompt): return f"[echo] {prompt}"
def reply_external(prompt, url):
    if not url: return "[external] External URL not set"
    try:
        r = requests.post(url, json={"prompt": prompt}, timeout=60); r.raise_for_status(); j = r.json(); return j.get("reply") or j.get("text") or str(j)
    except Exception as e: return f"[external] error: {e}"
def reply_llama(prompt, cfg):
    exe = cfg.get("exe"); model = cfg.get("model")
    if not (os.path.exists(exe) and os.path.exists(model)): return "[llama] binary or model missing"
    cmd = [exe, "-m", model, "-p", prompt, "-n", str(cfg.get("tokens",200)), "--temp", str(cfg.get("temp",0.7))]
    if cfg.get("seed", -1) != -1: cmd += ["--seed", str(cfg.get("seed"))]
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=180)
        return out.decode(errors='ignore')[-4000:]
    except Exception as e:
        return f"[llama] error: {e}"
def ai_reply(prompt):
    s = load_settings(); eng = s.get("engine","echo")
    if eng == "llama": return reply_llama(prompt, s.get("llama", {}))
    if eng == "external": return reply_external(prompt, s.get("external_url",""))
    return reply_echo(prompt)
