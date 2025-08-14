import os, json, plistlib, zipfile
BASE = "/var/mobile/Media/GOD"
def ensure_base():
    for p in ["data","logs","backups","bin","models","tmp","overrides"]:
        os.makedirs(os.path.join(BASE,p), exist_ok=True)
def read_file(path):
    with open(path, "rb") as f: return f.read()
def write_file(path, data:bytes):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f: f.write(data)
def read_json(path):
    with open(path, "r", encoding="utf-8") as f: return json.load(f)
def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f: json.dump(obj, f, ensure_ascii=False, indent=2)
def read_plist(path):
    with open(path, "rb") as f: return plistlib.load(f)
def write_plist(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f: plistlib.dump(obj, f)
def backup_zip():
    import datetime
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = os.path.join(BASE, "backups", f"god_{ts}.zip")
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(BASE):
            if "/backups" in root: continue
            for fn in files:
                full = os.path.join(root, fn); rel = os.path.relpath(full, BASE); z.write(full, arcname=rel)
    return dst
def restore_zip(zip_path):
    with zipfile.ZipFile(zip_path, "r") as z: z.extractall(BASE)
    return True
