# My Channel: make it your own

The first tile in the CleanYourRoku launcher is **My Channel**, a small personal channel on your own TV. In this repo it's set up as **My Album**, a family album filled with sample content.

**Everything in the sample is made up.** The family, their birthdays and the obituary are fictional, there to show what each section can do. Replace them with your own.

| Section | What it shows |
| --- | --- |
| **Family** | A family tree with profiles, birthdays and In Memory pages |
| **Photos** | Your photos |
| **Videos** | Videos played from direct links, or from [Jellyfin](jellyfin.md) |
| **Recipes** | Family recipes with ingredients, step cards and optional videos |
| **Music** | Songs played from direct links, or from Jellyfin |
| **Links** | QR codes with labels, for everyday links |
| **About** | A name, a short bio and a photo |

Up and Down move between sections. Each section shows its own remote hints at the bottom of the screen.

**Why it exists:** your TV's home screen is usually somewhere companies put *their* content. This is a corner of it that's yours.

---

## Everything lives in one file

You customize My Channel by editing **`mychannel.json`**. You don't need to touch any code.

| Field | What it does |
| --- | --- |
| `name` | Shown on the tile and at the top of My Channel. |
| `tagline` | One line under the name. Leave it `""` for none. |
| `tile_image` | The picture on the tile. |
| `about.name`, `about.photo`, `about.bio` | Your About section. |
| `family` | People in the Family section. |
| `photos` | Your photos, in order. |
| `videos` | Each `url` must link **directly to a video file**, not to a YouTube or Instagram page. |
| `recipes` | Recipe cards. |
| `music` | Songs, with a direct link to each audio file. |
| `links` | `id` names the QR image (lowercase letters, numbers and `_` only), `label` is what people see, `link` is what the QR code opens. |

The easiest way to learn the fields is to copy a sample entry and change it. Adding `people` to a photo, video or song puts it on those people's Family profiles.

**Leave a section out** by making its list `[]`, and it disappears from the menu. About is always there.

Images inside the app start with `pkg:/`, which means "inside this app's zip." `pkg:/images/mychannel/still_1.jpg` is the file `images/mychannel/still_1.jpg`.

**If you make a typo** (a missing comma or quote is the usual one), My Channel still opens, and the About section tells you it couldn't read the file. `python3 -m json.tool mychannel.json` will point to the line.

---

## Step by step

1. **Edit `mychannel.json`.**
2. **Add your images** to `images/mychannel/` and point to them in the JSON.
3. **Make the QR codes:**
   ```bash
   pip3 install segno            # once
   python3 scripts/make_qr.py
   ```
   This creates `images/mychannel/qr_<id>.png` for each link. A link's QR code stays blank on the TV until you do this.
4. **Rebuild the zip and reinstall:** see [roku-setup.md](roku-setup.md#3-build-the-zip), steps 3 and 4.

Change the JSON or images later? Repeat steps 3 and 4. The Roku only sees what's in the zip.

Two things aren't in `mychannel.json` yet. The three QR codes on the About page are the fixed images `qr_about_web.png`, `qr_about_github.png` and `qr_about_coffee.png`, so replace those files to use your own links. Family profiles look for `qr_social_facebook.png`, `qr_social_instagram.png` and `qr_social_tiktok.png`, which aren't included.

---

## Links and private info

QR codes are handy for things you'd otherwise read out loud, like a payment link or the guest Wi-Fi. Some of those are private, so:

- **Never put a real Wi-Fi password in `mychannel.json`.** Write `${GUEST_WIFI_PASSWORD}` instead, and give the real value only when you make the QR codes:
  ```bash
  GUEST_WIFI_PASSWORD='your-password' python3 scripts/make_qr.py
  ```
  The password ends up only in the QR image that goes on your TV. The included `wifi` example works this way; without the variable set, the script skips it.
- **Any link can use `${NAME}`** the same way, for anything you'd rather keep out of the file.
- **Generated QR images are git-ignored** (`images/mychannel/qr_*.png`), so they don't end up in a repo even when they hold a password. The only exceptions are `qr_about_*` and `qr_recipe_*`, which hold public links. Don't put anything private in images with those names.
- **Remember who can see your TV.** Anyone in the room can scan these codes. Share a guest network, not your main one.

**Why QR codes are made on your computer:** online QR generators see every link you give them, and some swap in their own tracking redirect. `make_qr.py` runs locally, so your links go straight from your file into the image.

---

## Keep it under 4 MB

Roku recommends packages under 4 MB, and big images are what push you over. (It's a warning, not a blocker, but smaller loads faster.)

- **Photos:** JPEG, about **1280×720**, usually 50–200 KB each. On a Mac: `sips -Z 1280 -s format jpeg photo.png --out photo_1.jpg`
- **About photo:** about **600×600** JPEG.
- **Delete images you don't use.** Everything in `images/` goes into the zip unless the build command leaves it out.

Check the size after building: `ls -lh cleanyourroku.zip`.

**Before you add photos,** check the backgrounds for anything personal (addresses, badges, screens) and strip location data (re-exporting or screenshotting a photo usually drops it). [CONTRIBUTING.md](../CONTRIBUTING.md) has more on photo privacy.

---

## Videos and music

Videos and music are optional and stream from wherever you host them. A link has to go straight to the file. Pages on YouTube, TikTok or Instagram won't work, because they're web pages, not video files.

The sample videos and songs use [Jellyfin](jellyfin.md), so they won't play until you set it up or replace them. If a video won't play, My Channel says so and shows Roku's error message, so you know it's the link and not you.

---

## Don't want My Channel?

Delete this entry from the app list in `components/HomeScene.xml`:

```brightscript
[m.ch.name, "mychannel"],
```

It's your home screen. That's the point.
