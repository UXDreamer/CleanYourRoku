# Roku setup: install the CleanYourRoku launcher

This guide puts the **CleanYourRoku launcher**, a home screen with only your apps, on your Roku. You'll need:

- A Roku device. This was tested on a Roku streaming player.
- A computer on the **same Wi-Fi** as the Roku
- Python 3, only for the optional logo step
- About 20 minutes

Haven't done [Step 0: privacy settings](roku-privacy-settings.md) yet? Start there. It needs no code and turns off most of the tracking.

> **Why sideload at all?** Roku's own home screen belongs to Roku, and settings can only change so much of it. The ad panel stays no matter what. Roku's developer mode is an official feature that lets you install your own app from your own computer. Nothing is hacked, nothing about the Roku is permanently changed, and you can remove it any time. It's the most control Roku gives you, so this project uses all of it.

---

## 1. Turn on developer mode

On your Roku remote, press this sequence. It's Roku's official way in:

**Home ×3, Up ×2, Right, Left, Right, Left, Right**

1. The Developer Settings screen appears. **Write down the IP address** it shows. These guides call it `<ROKU_IP>`.
2. Select **Enable installer and restart**.
3. Accept the developer agreement.
4. **Set a password.** You'll use it to log into the install page. Don't reuse a password you use anywhere else, and never commit it to a repo (see [SECURITY.md](../SECURITY.md)).
5. The Roku restarts.

**Why the password matters:** anyone on your Wi-Fi who knows it can install apps on your Roku. Developer mode gives *you* control; the password keeps it yours.

You can also find your Roku's IP anytime in **Settings → Network → About**.

---

## 2. Open the install page

On your computer, open a browser and go to:

```
http://<ROKU_IP>
```

Log in with username **`rokudev`** and the password you just set.

*Screenshot coming: the Roku Development Application Installer page.*

---

## 3. Build the zip

Roku installs apps from a zip file. The `manifest` file has to be at the **top level** of the zip, not inside a folder. From the repo folder:

```bash
zip -r cleanyourroku.zip manifest source components mychannel.json images \
  -x "*.DS_Store" "images/roku-*" "images/dreamer-tv-*" "images/phone-remote.png"
```

**Why this way:** the repo also holds docs, scripts and website files that don't belong on your TV. This command packs only the app, and leaves out the screenshots used in the guides. If you right-click the repo folder and choose "Compress," the zip contains the folder itself, the Roku can't find the `manifest`, and the install fails.

Using Jellyfin for your videos and music? Build with the extra steps in [jellyfin.md](jellyfin.md#3-build-with-your-real-values) instead.

`.gitignore` blocks `*.zip`, so your build files never end up in the repo.

---

## 4. Install: the Delete → Upload → Install routine

On the install page:

1. **Delete.** If an app is already installed, delete it first.
2. **Upload.** Choose `cleanyourroku.zip`.
3. **Install.** Click Install. The launcher opens on your TV right away.

Do all three every time you update the app.

**Why delete first:** Roku allows only **one** sideloaded app at a time, and replacing in place doesn't always pick up every change. Deleting first gives you a clean install, so what you see on the TV is what's in your zip.

After installing, the launcher shows up in your Roku's app list as **CleanYourRoku** (the `title` in the `manifest`). Move it to the top of your Roku home so it's one click away.

*Screenshot coming: the launcher running with placeholder tiles.*

---

## 5. Make it yours: edit the app list

The launcher shows whatever apps are listed in `components/HomeScene.xml`:

```brightscript
m.apps = [
    [m.ch.name, "mychannel"], ["YouTube", "837"], ["Netflix", "12"], ...
]
```

Each entry is `["Name to show", "Roku app ID"]`.

**Find your apps' IDs:**

```bash
python3 scripts/pull_logos.py --roku <ROKU_IP> --list
```

This prints every app installed on your Roku with its ID. Add the ones you want, remove the ones you don't, and put them in **the order you choose**.

**Why this matters:** this list is the whole point. On Roku's home screen, an algorithm decides what comes first. Here, you do. Whatever's on this list is what you see, nothing else.

> The first entry, `"mychannel"`, is **My Channel**: a personal tile that opens your own Family, Photos, Videos, Recipes, Music, Links and About pages instead of an app. Its label is `name` from `mychannel.json` (My Album in this repo). Make it yours with [my-channel.md](my-channel.md), or delete that line to leave it out.

---

## 6. Pull your app logos

App logos belong to their companies, so they aren't in the repo, and app tiles stay blank until you add them. Pull them from your own Roku:

```bash
python3 scripts/pull_logos.py --roku <ROKU_IP>
```

This downloads each listed app's icon from your Roku into `images/`. An app that isn't installed on your Roku gets skipped, so remove it from the list or install it first. `.gitignore` keeps logos out of the repo. Then rebuild the zip (step 3) and reinstall (step 4).

**Why from your Roku:** the icons come from apps you already have, on a device you own, over your own network. Nothing gets scraped from the internet.

Getting a **403 error**? See the [FAQ](faq.md#i-get-a-403-error).

---

## 7. Take screenshots

The install page has a built-in screenshot tool. That's how the launcher screenshots in the README were made.

1. With the launcher on screen, open `http://<ROKU_IP>` on your computer.
2. Go to **Utilities → Screenshot**.
3. Save the image.

It captures the sideloaded app at full resolution, much cleaner than a phone photo of the TV. If you share before-and-afters (please do! See [CONTRIBUTING.md](../CONTRIBUTING.md)), check that nothing personal is on screen.

---

## 8. Optional: publish as a private beta

Sideloading works great on your own Roku. If you want the launcher on **other** Roku devices, like a family member's, without developer mode on each one, you can publish it as a **beta channel**. A beta is private: only people you invite can install it.

> When I started this, the AI I was working with said publishing a Roku beta wasn't possible for a project like this. I tried anyway, and it worked. Tools are good at telling you what's typical. You get to decide what to try. See [ABOUT.md](../ABOUT.md).

**a. Generate a signing key.** Connect to your Roku's developer console from Terminal:

```bash
nc <ROKU_IP> 8080
```

Type `genkey` and press Enter. It prints a **password** and a **DevID**. Save both somewhere private, like a password manager.

**b. Package the app.** Sideload the version you want (step 4), then on the install page go to **Utilities → Packager**. Enter an app name and version and the `genkey` password, then click **Package**. Download the `.pkg` file.

**c. Upload it.** In the Roku Developer Dashboard (developer.roku.com), create a new beta channel and upload the `.pkg`.

**d. Static analysis.** Roku automatically scans your package. **Warnings are OK.** You'll likely see one about `LaunchApp`, and one about package size if you've added large images. They don't block a beta. See the [FAQ](faq.md) for what they mean.

**Why the signing key is a big deal:** the key proves updates come from you. Anyone who has it could publish an update in your name. Never commit the key, its password or `.pkg` files. `.gitignore` blocks `*.pkg`, and [SECURITY.md](../SECURITY.md) explains the rest.

---

## What the launcher can't do

Be clear-eyed about the limits, so the decision to use it is an informed one:

- **Back goes to Roku's home.** Pressing Back inside Netflix or another app returns you to Roku's home screen, not the launcher. Roku controls this, and an app can't override it. Tip: you can jump straight back from any computer on your Wi-Fi with `curl -d '' http://<ROKU_IP>:8060/launch/dev`. That's the same command behind the one-tap "CleanYourRoku" button on the [phone remote](../scripts/rokuremote.py) (work in progress: only that button works so far).
- **It curates; it doesn't control.** The launcher changes what you *see*. It doesn't uninstall, block or lock any apps.
- **Roku's home is still there.** The launcher is an alternative home, not a replacement for Roku's.

More in the [FAQ](faq.md).
