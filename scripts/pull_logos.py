"""Pull app icons from your own Roku for the CleanYourRoku launcher.

Reads the app list in components/HomeScene.xml, asks your Roku for each app's
icon over the local network (ECP, port 8060), and saves them as
images/app_<id>.png. Logos stay on your machine; .gitignore keeps them out of
the repo.

Usage:
    python3 scripts/pull_logos.py --roku <ROKU_IP> --list   # show installed apps and their IDs
    python3 scripts/pull_logos.py --roku <ROKU_IP>          # download icons for the launcher's apps

You can also set ROKU_IP in your environment instead of passing --roku.
Uses only the Python standard library. On a Mac, non-PNG icons are converted with sips.
"""
import argparse, os, re, shutil, subprocess, sys, urllib.error, urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENE = os.path.join(ROOT, "components", "HomeScene.xml")
IMAGES = os.path.join(ROOT, "images")

def get(roku, path):
    try:
        with urllib.request.urlopen("http://" + roku + ":8060" + path, timeout=5) as r:
            return r.read(), r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        if e.code == 403:
            sys.exit("403 Forbidden: your Roku is blocking network control. Set Settings > System > "
                     "Advanced system settings > Control by mobile apps > Network access to Permissive. "
                     "See docs/faq.md.")
        raise
    except urllib.error.URLError as e:
        sys.exit("Couldn't reach a Roku at " + roku + " (" + str(e.reason) + "). Check the IP address "
                 "in Settings > Network > About, and that this computer is on the same Wi-Fi.")

def installed(roku):
    body, _ = get(roku, "/query/apps")
    return {a.get("id"): a.text for a in ET.fromstring(body).iter("app")}

def launcher_apps():
    # Matches entries like ["Netflix", "12"] in HomeScene.xml; numeric IDs only (skips the "uxd" tile)
    with open(SCENE) as f:
        return re.findall(r'\["([^"]+)",\s*"(\d+)"\]', f.read())

def main():
    p = argparse.ArgumentParser(description="Pull app icons from your Roku for the CleanYourRoku launcher.")
    p.add_argument("--roku", default=os.environ.get("ROKU_IP"), help="your Roku's IP address")
    p.add_argument("--list", action="store_true", help="list installed apps and their IDs, then exit")
    args = p.parse_args()
    if not args.roku:
        p.error("give your Roku's IP with --roku <ROKU_IP> or set ROKU_IP")

    apps = installed(args.roku)
    if args.list:
        for app_id, name in sorted(apps.items(), key=lambda x: (x[1] or "").lower()):
            print(app_id.rjust(8), " ", name)
        return

    os.makedirs(IMAGES, exist_ok=True)
    for name, app_id in launcher_apps():
        if app_id not in apps:
            print("skip   ", name, "(" + app_id + ") is not installed on this Roku")
            continue
        data, ctype = get(args.roku, "/query/icon/" + app_id)
        out = os.path.join(IMAGES, "app_" + app_id + ".png")
        if "png" in ctype or not shutil.which("sips"):
            with open(out, "wb") as f:
                f.write(data)
        else:
            tmp = out + ".download"
            with open(tmp, "wb") as f:
                f.write(data)
            subprocess.run(["sips", "-s", "format", "png", tmp, "--out", out], capture_output=True)
            os.remove(tmp)
        print("saved  ", name, "->", os.path.relpath(out, ROOT))

if __name__ == "__main__":
    main()
