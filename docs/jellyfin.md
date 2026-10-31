# Jellyfin setup: your own videos and music, with the key kept out of Git

My Channel can play videos and music from [Jellyfin](https://jellyfin.org), a free media server you run on a computer in your home. This is optional. Without it, the launcher still works, but anything in My Channel that streams from Jellyfin won't load.

**Why Jellyfin:** your family videos stay on your own computer and network. No upload to someone else's service, and no recommendations next to them.

> **Tested on one setup only:** one Jellyfin server and one Roku streaming player on a home network. Menu names can change between Jellyfin versions.

---

## 1. Set up the server

1. Install Jellyfin from [jellyfin.org/downloads](https://jellyfin.org/downloads) on a computer that stays on while you watch.
2. Finish the setup wizard and add a library for your videos and one for your music.
3. Find that computer's local IP address. These steps call it `<JELLYFIN_IP>`. Jellyfin's web page is at `http://<JELLYFIN_IP>:8096`.
4. Reserve that IP in your router, if it lets you. If the address changes, the links stop working until you rebuild.
5. In Jellyfin's admin dashboard, open **API Keys** and create a new key for CleanYourRoku.

**Why the API key matters:** anyone on your network who has it can reach your Jellyfin server. Treat it like a password. See [SECURITY.md](../SECURITY.md).

---

## 2. Point `mychannel.json` at your files

Open an item in Jellyfin's web page. Its long ID is in the address bar. Then use that ID in `mychannel.json`, leaving the two placeholders exactly as they are:

```json
{
  "title": "My video",
  "length": "0:58",
  "thumb": "http://YOUR_JELLYFIN_IP:8096/Items/<ITEM_ID>/Images/Primary?maxWidth=1920&ApiKey=YOUR_JELLYFIN_API_KEY",
  "url": "http://YOUR_JELLYFIN_IP:8096/Videos/<ITEM_ID>/stream.mp4?static=true&ApiKey=YOUR_JELLYFIN_API_KEY",
  "video": "http://YOUR_JELLYFIN_IP:8096/Videos/<ITEM_ID>/stream.mp4?static=true&ApiKey=YOUR_JELLYFIN_API_KEY"
}
```

Music works the same way, in the `music` list:

```json
"url": "http://YOUR_JELLYFIN_IP:8096/Audio/<ITEM_ID>/stream.mp3?AudioCodec=mp3&ApiKey=YOUR_JELLYFIN_API_KEY"
```

**Why keep the placeholders:** `mychannel.json` is tracked by Git. Your real key never goes in it, so it can't be committed by accident.

---

## 3. Build with your real values

Add these lines to `~/.zshrc`, then open a new Terminal window:

```bash
export JELLYFIN_IP="<JELLYFIN_IP>"
export JELLYFIN_API_KEY="<YOUR_API_KEY>"
```

Build the zip as usual, then swap in a filled-in copy of `mychannel.json`:

```bash
zip -r cleanyourroku.zip manifest source components mychannel.json images \
  -x "*.DS_Store" "images/roku-*" "images/dreamer-tv-*" "images/phone-remote.png"

mkdir -p build
sed -e "s/YOUR_JELLYFIN_IP/$JELLYFIN_IP/g" \
    -e "s/YOUR_JELLYFIN_API_KEY/$JELLYFIN_API_KEY/g" mychannel.json > build/mychannel.json
(cd build && zip ../cleanyourroku.zip mychannel.json)
```

Then install it with [Delete → Upload → Install](roku-setup.md#4-install-the-delete--upload--install-routine).

**Why this way:** the real values exist only in `build/` and in the zip. Git ignores both.

**The zip now holds your key.** Don't share it, attach it to an issue or send it to anyone. To see for yourself that the key is safe, run `git status` and check that neither `build/` nor the zip is listed.

---

## If something won't play

- **Is the server on?** The computer running Jellyfin has to be awake and on the same network as the Roku.
- **Does the link work?** Paste the filled-in link from `build/mychannel.json` into a browser on your computer. If it won't play there, the problem is the link, not the Roku.
- **Did the IP change?** Update `JELLYFIN_IP`, open a new Terminal window, then rebuild and reinstall.
- **Think your key leaked?** Delete it in Jellyfin's dashboard and create a new one.
