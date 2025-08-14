import os, zipfile, requests, tempfile, shutil
BASE = "/var/mobile/Media/GOD"
OVR = os.path.join(BASE, "overrides")
def apply_zip_from_url(url:str):
    if not url: return {"ok": False, "msg": "ZIP URL empty"}
    os.makedirs(OVR, exist_ok=True)
    tmpfd, tmpzip = tempfile.mkstemp(suffix=".zip"); os.close(tmpfd)
    try:
        with requests.get(url, stream=True, timeout=120) as r:
            r.raise_for_status()
            with open(tmpzip, "wb") as f:
                for chunk in r.iter_content(chunk_size=65536):
                    if chunk: f.write(chunk)
        with zipfile.ZipFile(tmpzip, "r") as z: z.extractall(OVR)
        return {"ok": True, "msg": "applied", "path": OVR}
    except Exception as e:
        return {"ok": False, "msg": str(e)}
    finally:
        try: os.remove(tmpzip)
        except: pass
