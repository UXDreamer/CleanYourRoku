# Phone remote for Roku -- WORK IN PROGRESS
# Serves a page of big buttons from your computer; open it on your phone (same Wi-Fi).
# Right now only the one-tap "CleanYourRoku" button works reliably. The other buttons are still being fixed.
# Setup: find your Roku's IP (Settings > Network > About), then run:
#   ROKU_IP=<ROKU_IP> python3 scripts/rokuremote.py
# and open http://<YOUR_COMPUTER_IP>:8001 on your phone. Getting 403 errors? See docs/faq.md.
import http.server, os, sys, urllib.request
if not os.environ.get("ROKU_IP"):
    sys.exit("Set ROKU_IP first: ROKU_IP=<ROKU_IP> python3 scripts/rokuremote.py")
ROKU = "http://" + os.environ["ROKU_IP"] + ":8060"
def roku(path):
    try: urllib.request.urlopen(urllib.request.Request(ROKU + path, data=b"", method="POST"), timeout=3)
    except Exception as e: print("error:", e)
BUTTONS = [("CleanYourRoku","/launch/dev"),("Home","/keypress/Home"),("Back","/keypress/Back"),
           ("Up","/keypress/Up"),("Left","/keypress/Left"),("OK","/keypress/Select"),("Right","/keypress/Right"),
           ("Down","/keypress/Down"),("Vol +","/keypress/VolumeUp"),("Vol -","/keypress/VolumeDown"),
           ("Mute","/keypress/VolumeMute"),("Power","/keypress/Power")]
PAGE = """<html><head><meta name=viewport content='width=device-width,initial-scale=1'>
<meta name=apple-mobile-web-app-capable content=yes><title>Roku Remote</title>
<style>body{background:#0e1116;color:#fff;font-family:sans-serif;text-align:center;margin:20px}
button{width:42%;padding:22px;margin:6px;font-size:20px;border:0;border-radius:14px;background:#26303c;color:#fff}
.big{width:88%;background:#e6aa28;color:#0e1116;font-weight:bold;font-size:24px}</style></head><body>
<h2>Roku Remote</h2>""" + "".join(
    "<button class=%s onclick=\"fetch('/go?p=%s')\">%s</button>" % ("big" if i==0 else "", p, n)
    for i,(n,p) in enumerate(BUTTONS)) + "</body></html>"
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/go?p="):
            roku(self.path[6:]); self.send_response(204); self.end_headers(); return
        self.send_response(200); self.send_header("Content-Type","text/html"); self.end_headers()
        self.wfile.write(PAGE.encode())
    def log_message(self,*a): pass
print("Roku remote running at http://<YOUR_COMPUTER_IP>:8001")
http.server.HTTPServer(("", 8001), H).serve_forever()
