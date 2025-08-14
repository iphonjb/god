import shutil, subprocess
def which(cmd): return shutil.which(cmd) or ""
def frida_list():
    exe = which('frida-ps'); 
    if not exe: return {"ok": False, "msg": "frida-ps not installed"}
    try:
        out = subprocess.check_output([exe, "-U"], stderr=subprocess.STDOUT, timeout=15)
        return {"ok": True, "out": out.decode(errors='ignore')}
    except Exception as e:
        return {"ok": False, "msg": str(e)}
def run_tool(cmdline):
    try:
        out = subprocess.check_output(cmdline, shell=True, stderr=subprocess.STDOUT, timeout=30)
        return {"ok": True, "out": out.decode(errors='ignore')[-6000:]}
    except Exception as e:
        return {"ok": False, "out": str(e)}
