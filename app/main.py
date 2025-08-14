import threading, time, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from server import app
def run_server():
    # run with minimal workers to conserve CPU/battery
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
if __name__ == '__main__':
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        pass
