# FAQ

Common questions and fixes. Don't see yours? [Open an issue](https://github.com/dlpressl/CleanYourRoku/issues/new).

---

## I get a 403 error

**What you see:** `403 Forbidden` when the logo puller, a phone remote, or a `curl` command tries to talk to your Roku on port 8060.

**Why it happens:** newer Roku software limits which devices on your network can control the Roku. That's a reasonable safety default, since it stops random devices from controlling your TV. But it also blocks you.

**Fix:** on the Roku, go to **Settings → System → Advanced system settings → Control by mobile apps → Network access** and set it to **Permissive**.

**The trade-off:** Permissive lets any device on your Wi-Fi send remote commands to your Roku. On a home network you trust, that's usually fine. On a shared network (dorm, apartment Wi-Fi, office), think twice. This is your call. Agency includes deciding which risks are worth it.

If the *install page* (`http://<ROKU_IP>`) rejects you instead, that's usually a wrong `rokudev` password. You can reset it by entering the developer mode button sequence again. See [roku-setup.md](roku-setup.md#1-turn-on-developer-mode).

---

## Static analysis warns about `LaunchApp`. Is that a problem?

**No, not for a beta.** When you upload a package to Roku's Developer Dashboard, Roku scans it automatically. The launcher opens other apps, and that's the whole job of a launcher, so the scan flags the code that does it (`LaunchApp` in `components/Launcher.xml`).

**Why it's flagged:** Roku's tools assume most apps are self-contained. An app that opens *other* apps is unusual, so it gets a warning. A **warning** isn't an **error**, though. The beta still publishes and runs.

**Why not just trust the warning?** Automated checks are useful, but they flag what's unusual, not what's wrong. That's automation bias in miniature. The right move is to understand *why* it's flagged and then decide, not to obey the tool or ignore it blindly.

---

## Static analysis says my package is over 4 MB

**Why it happens:** Roku recommends small packages so apps load quickly. Large images, especially a full-screen background and big icons, push you over.

**It's a warning, not a blocker.** But smaller is faster, so it's worth fixing:

- **Shrink big images.** On a Mac:
  ```bash
  sips -Z 1920 images/bg.jpg
  ```
  Logos only need to be about 290×218. That's what the [logo puller](roku-setup.md#6-pull-your-app-logos) saves.
- **Remove images you don't use.** Anything in `images/` goes into the zip, even if the code never references it.
- **Use JPEG for photo-like backgrounds.** It's often far smaller than PNG. The launcher's background is already `bg.jpg`; if you add your own, keep the same name or update it in `HomeScene.xml`.
- **Keep My Channel photos around 1280×720 JPEG.** See [my-channel.md](my-channel.md#keep-it-under-4-mb).

---

## When I press Back in an app, I end up on Roku's home, not the launcher

**That's Roku, not a bug.** When you leave an app, the Roku system decides where you go, and it always goes to Roku's own home screen. A sideloaded app can't change that.

**Workarounds:**

- Put CleanYourRoku first in your Roku's app list, so it's one click away.
- Relaunch it from any computer on your Wi-Fi: `curl -d '' http://<ROKU_IP>:8060/launch/dev`
- Use the [phone remote](../scripts/rokuremote.py) with its one-tap CleanYourRoku button (work in progress: only that button works so far).

**Why I'm upfront about this:** the launcher *curates* your view. It doesn't take over the Roku, and it's better you know that before you set it up.

---

## Can I have more than one home screen? (Zip files as profiles)

**Yes, sort of.** Roku allows only one sideloaded app at a time, but you can keep **several zip files**, each a different version of the launcher, and install whichever one you want.

For example:

- `cleanyourroku-everyday.zip`: all your apps
- `cleanyourroku-kids.zip`: only kid-friendly apps
- `cleanyourroku-focus.zip`: just two or three apps, for when you don't want to browse

To switch, use the **Delete → Upload → Install** routine from [roku-setup.md](roku-setup.md#4-install-the-delete--upload--install-routine). It takes about a minute.

**Why this is useful:** different moments call for different choices, and *you* define them instead of an algorithm guessing your mood. (`.gitignore` keeps zips out of the repo, so your profiles stay yours.)

Remember: a profile **curates** what's shown. It doesn't lock anything. A kids' profile isn't a parental control.

---

## Does this uninstall apps or block anything?

**No.** The launcher only changes which apps you *see* on its screen. Everything else on your Roku stays installed and reachable from Roku's home screen.

---

## Will this break my Roku or void my warranty?

Developer mode is an official Roku feature for building apps. Nothing in this project modifies your Roku's system software. To undo everything, delete the app from the install page, and you can turn developer mode off from the same Developer Settings screen.

---

## Does it work on my Roku model?

It's been tested on one Roku streaming player. Other Roku players and Roku-built TVs *should* work, since developer mode is the same across Roku devices, but this hasn't been confirmed. If you try it, please [add your notes](../CONTRIBUTING.md). That's one of the most helpful contributions you can make.
