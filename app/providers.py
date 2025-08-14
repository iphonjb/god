import requests, os, json, base64, tempfile, subprocess
def txt2img_stable_horde(prompt, url):
    if not url: return {"ok": False, "msg": "Stable Horde URL not set"}
    try:
        r = requests.post(url, json={"prompt": prompt}, timeout=60); return {"ok": True, "data": r.json()}
    except Exception as e: return {"ok": False, "msg": str(e)}
def txt2img_a1111(prompt, base_url):
    if not base_url: return {"ok": False, "msg": "A1111 URL not set"}
    try:
        r = requests.post(f"{base_url}/sdapi/v1/txt2img", json={"prompt": prompt, "steps": 20}, timeout=120)
        j = r.json(); img_b64 = (j.get("images") or [None])[0]; return {"ok": True, "image_b64": img_b64}
    except Exception as e:
        return {"ok": False, "msg": str(e)}
def ocr_tesseract(image_path, exe):
    if not exe or not os.path.exists(exe): return {"ok": False, "msg": "tesseract not found"}
    if not os.path.exists(image_path): return {"ok": False, "msg": "image missing"}
    out_txt = tempfile.mktemp(); cmd = [exe, image_path, out_txt]
    subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=60)
    with open(out_txt + ".txt","r",encoding="utf-8",errors="ignore") as f: text = f.read()
    return {"ok": True, "text": text}
def whisper_transcribe(audio_path, url):
    if not url: return {"ok": False, "msg": "Whisper URL not set"}
    if not os.path.exists(audio_path): return {"ok": False, "msg": "audio missing"}
    files = {"file": open(audio_path,"rb")}
    r = requests.post(url, files=files, timeout=300); return {"ok": True, "data": r.json()}
