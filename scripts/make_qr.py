"""Make QR code images for the Share Links section of My Channel.

Reads "links" from mychannel.json and saves one QR code per link as
images/mychannel/qr_<id>.png. Everything happens on your computer; no link is
sent anywhere. .gitignore keeps the QR images out of the repo.

Usage:
    python3 scripts/make_qr.py                 # uses the launcher in this repo
    python3 scripts/make_qr.py --app <FOLDER>  # a launcher folder somewhere else

Private values: write ${NAME} in a link and set NAME in your environment, e.g.
    "link": "WIFI:T:WPA;S:MyGuestWifi;P:${GUEST_WIFI_PASSWORD};;"
    GUEST_WIFI_PASSWORD='...' python3 scripts/make_qr.py
The password ends up only in the QR image on your Roku, never in mychannel.json.

Needs the segno library (pure Python): pip3 install segno
"""
import argparse, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QR_PX = 420  # matches the QR poster size in HomeScene.xml

def expand(link):
    # Replaces ${NAME} with the NAME environment variable. Returns None if one isn't set.
    missing = [n for n in re.findall(r"\$\{(\w+)\}", link) if n not in os.environ]
    if missing:
        return None, missing
    return re.sub(r"\$\{(\w+)\}", lambda m: os.environ[m.group(1)], link), []

def main():
    p = argparse.ArgumentParser(description="Make QR code images for My Channel's Share Links.")
    p.add_argument("--app", default=ROOT,
                   help="launcher folder that holds mychannel.json (default: this repo)")
    args = p.parse_args()
    app = os.path.expanduser(args.app)

    try:
        import segno
    except ImportError:
        sys.exit("This script needs segno. Install it with: pip3 install segno")

    path = os.path.join(app, "mychannel.json")
    try:
        with open(path) as f:
            links = json.load(f).get("links", [])
    except FileNotFoundError:
        sys.exit("No mychannel.json in " + app)
    except json.JSONDecodeError as e:
        sys.exit("mychannel.json has a typo near line " + str(e.lineno) + ": " + e.msg)

    out_dir = os.path.join(app, "images", "mychannel")
    os.makedirs(out_dir, exist_ok=True)
    for link in links:
        lid, raw = link.get("id", ""), link.get("link", "")
        if not re.fullmatch(r"[a-z0-9_]+", lid):
            print("skip    ", repr(lid), "- ids must be lowercase letters, numbers or _ (they become file names)")
            continue
        if raw.startswith("WIFI:") and re.search(r"P:(?!\$\{)[^;]", raw):
            print("warning ", lid, "- this Wi-Fi password is typed into mychannel.json. Consider ${GUEST_WIFI_PASSWORD} "
                  "instead, and don't commit it.")
        text, missing = expand(raw)
        if text is None:
            print("skip    ", lid, "- set", ", ".join(missing), "in your environment first")
            continue
        qr = segno.make(text, error="m")
        size = qr.symbol_size(border=2)[0]
        out = os.path.join(out_dir, "qr_" + lid + ".png")
        qr.save(out, scale=max(1, QR_PX // size), border=2, dark="#000000", light="#FFFFFF")
        print("saved   ", lid, "->", os.path.relpath(out, app))

    print("Rebuild the zip and reinstall to see them on your TV.")

if __name__ == "__main__":
    main()
