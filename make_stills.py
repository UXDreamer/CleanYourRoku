# Makes photos from the family videos: grabs 2 stills from each video.
# Put your real Jellyfin address and API key in mychannel.json only while this runs, and keep the server on.
# Uses ffmpeg if it's installed; otherwise grabs Jellyfin's own frame (1 per video).
import json, os, shutil, subprocess, urllib.request
d = json.load(open("mychannel.json"))
if any(p.get("still") for p in d["photos"]):
    raise SystemExit("ALREADY APPLIED - nothing changed")
PLAN = {
 "Bike Ride with Dad": ["Isabella Rides Solo", "Down Willow Creek Park"],
 "Susan's Birthday at the Fair": ["Up on the Swings", "Susan's Fair Day"],
 "Winter Holiday in the Mountains": ["Cable Cars in the Snow", "Silver Peak View"],
 "The New Pup's First Walk": ["Duke and Peanut", "Walk in MacArthur Park"],
 "Tyler's First Gig": ["Tyler on Stage", "The Backyard Echoes"],
}
ff = shutil.which("ffmpeg") or ("/opt/homebrew/bin/ffmpeg" if os.path.exists("/opt/homebrew/bin/ffmpeg") else None)
print("Using ffmpeg" if ff else "No ffmpeg found - using Jellyfin's frame, 1 photo per video")
out = []
n = 0
for v in d["videos"]:
    titles = PLAN.get(v["title"])
    if not titles: continue
    mm, ss = (v.get("length") or "1:00").split(":")
    secs = int(mm) * 60 + int(ss)
    shots = []
    if ff:
        for j, frac in enumerate([0.35, 0.7]):
            n += 1
            fn = "images/mychannel/still_%d.jpg" % n
            r = subprocess.run([ff, "-y", "-loglevel", "error", "-ss", str(max(1, int(secs * frac))), "-i", v["video"],
                                "-frames:v", "1", "-vf", "scale=1920:-2", "-q:v", "3", fn], timeout=120)
            if r.returncode == 0 and os.path.exists(fn) and os.path.getsize(fn) > 1000:
                shots.append((fn, titles[j]))
    if not shots:
        n += 1
        fn = "images/mychannel/still_%d.jpg" % n
        urllib.request.urlretrieve(v["thumb"], fn)
        shots.append((fn, titles[0]))
    for fn, t in shots:
        out.append({"title": t, "still": True, "category": v.get("category", ""), "season": v.get("season", ""),
                    "date": v.get("date", ""), "filmedBy": v.get("filmedBy", ""), "who": v.get("who", ""),
                    "where": v.get("where", ""), "people": v.get("people", []),
                    "image": "pkg:/" + fn, "thumb": "pkg:/" + fn, "caption": t})
        print("  ", v.get("category", ""), "-", t, "-", fn, os.path.getsize(fn) // 1024, "KB")
if not out:
    raise SystemExit("NO STILLS MADE - is your Jellyfin server running?")
d["photos"] = out
json.dump(d, open("mychannel.json", "w"), indent=2)
print("STILLS READY: %d photos" % len(out))
