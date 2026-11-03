# Jellyfin setup: your own videos and music, with the key kept out of Git

My Channel and the launcher's **Music** button can play videos and music from [Jellyfin](https://jellyfin.org), a free media server you run on a computer in your home. This is optional. Without it, the launcher still works, but anything that streams from Jellyfin won't load.

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

Add these lines to `~/.zshrc`, then open a new Terminal window. The last two are for the [Music button](#4-the-music-button); leave them out if you don't use it.

```bash
export JELLYFIN_IP="<JELLYFIN_IP>"
export JELLYFIN_API_KEY="<YOUR_API_KEY>"
export JELLYFIN_MUSIC_LIBRARY_ID="<YOUR_MUSIC_LIBRARY_ID>"
export JELLYFIN_USER_ID="<YOUR_JELLYFIN_USER_ID>"
```

Build the zip as usual, then swap in filled-in copies of `mychannel.json` and `source/jellyfin.json`:

```bash
zip -r cleanyourroku.zip manifest source components mychannel.json images \
  -x "*.DS_Store" "images/roku-*" "images/dreamer-tv-*" "images/phone-remote.png"

mkdir -p build/source
fill() {
  sed -e "s/YOUR_JELLYFIN_IP/$JELLYFIN_IP/g" \
      -e "s/YOUR_JELLYFIN_API_KEY/$JELLYFIN_API_KEY/g" \
      -e "s/YOUR_MUSIC_LIBRARY_ID/$JELLYFIN_MUSIC_LIBRARY_ID/g" \
      -e "s/YOUR_JELLYFIN_USER_ID/$JELLYFIN_USER_ID/g" "$1" > "build/$1"
}
fill mychannel.json
fill source/jellyfin.json
(cd build && zip ../cleanyourroku.zip mychannel.json source/jellyfin.json)
```

Then install it with [Delete → Upload → Install](roku-setup.md#4-install-the-delete--upload--install-routine).

**Why this way:** the real values exist only in `build/` and in the zip. Git ignores both.

**The zip now holds your key.** Don't share it, attach it to an issue or send it to anyone. To see for yourself that the key is safe, run `git status` and check that neither `build/` nor the zip is listed.

---

## 4. The Music button

The **Music** button to the left of your apps opens a pop-up that plays songs straight from your Jellyfin music library: **Songs**, **Artists**, **Albums**, **Playlists** and **Recently Played**. A Now Playing line sits under the grid, and the Play/Pause button on your remote pauses and resumes.

It reads its settings from `source/jellyfin.json`. That file keeps placeholders in Git, just like `mychannel.json`:

```json
{
  "server": "http://YOUR_JELLYFIN_IP:8096",
  "key": "YOUR_JELLYFIN_API_KEY",
  "musicLibrary": "YOUR_MUSIC_LIBRARY_ID",
  "videoLibrary": "",
  "userId": "YOUR_JELLYFIN_USER_ID"
}
```

Leave them as they are. The [build step](#3-build-with-your-real-values) fills in your real values. Until then, the pop-up says Jellyfin isn't set up yet. `videoLibrary` is for the Video button, which is coming in the next update.

**Send the key in a header, not in the link.** Newer Jellyfin versions answer `401 Unauthorized` when the key is in the address (`?api_key=...`). The launcher sends it in the `Authorization` header instead, as `MediaBrowser Token="<YOUR_API_KEY>"`. Do the same when you look up the IDs below.

### Find your music library ID

Ask your server for its libraries. Run this on a computer on the same network, with the variables from step 3 set:

```bash
curl -s -H "Authorization: MediaBrowser Token=\"$JELLYFIN_API_KEY\"" \
  "http://$JELLYFIN_IP:8096/Library/MediaFolders" | python3 -m json.tool | grep -E '"(Name|Id|CollectionType)"'
```

Find the library whose `CollectionType` is `music`. Its `Id` is your music library ID. (In Jellyfin's web page, opening that library usually shows the same ID after `topParentId=` in the address bar.)

### Find your user ID

Playlists need a user ID. List the users on your server:

```bash
curl -s -H "Authorization: MediaBrowser Token=\"$JELLYFIN_API_KEY\"" \
  "http://$JELLYFIN_IP:8096/Users" | python3 -m json.tool | grep -E '"(Name|Id)"'
```

Use the `Id` next to your user name. Put both IDs in `JELLYFIN_MUSIC_LIBRARY_ID` and `JELLYFIN_USER_ID` in `~/.zshrc`, never in a tracked file.

**Why the IDs stay out of Git, too:** they aren't passwords, but together with your server's address they map out your home network and accounts. There's no reason to publish them.

---

## If something won't play

- **Is the server on?** The computer running Jellyfin has to be awake and on the same network as the Roku.
- **Does the link work?** Paste the filled-in link from `build/mychannel.json` into a browser on your computer. If it won't play there, the problem is the link, not the Roku.
- **Did the IP change?** Update `JELLYFIN_IP`, open a new Terminal window, then rebuild and reinstall.
- **Music pop-up says it couldn't reach Jellyfin?** Check that the server is on, then that the library ID is your *music* library, and rebuild. A `401` from the curl commands above means the key is wrong or was sent in the link instead of the header.
- **Think your key leaked?** Delete it in Jellyfin's dashboard and create a new one.
