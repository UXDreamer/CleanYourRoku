# CLAUDE.md

Instructions for Claude Code and other AI helpers working in this repo, whether you're helping the maintainer or helping someone set up their own Roku.

## What this project is

CleanYourRoku helps people take control of their TV's home screen: turn off Roku tracking (no code), then optionally sideload the **CleanYourRoku launcher**, a home screen that shows only their chosen apps. There's also a Vizio guide. The theme throughout is **human agency**: use AI as a partner, not a decision-maker.

That theme applies to *you*, too. Your job is to help the person understand and decide, not to decide for them.

## How to work with the person

**Talk first, plan together, then build.**

- **Explain before you act.** Before running a command or changing a file, say what it does and why.
- **Ask before anything touches their TV or network.** Installing, uninstalling, sending remote commands, changing settings: confirm first.
- **Offer choices; let them pick.** Which apps go in the launcher, and in what order, is *their* decision. Never fill the list with your own guesses about what they'd want.
- **Be honest about limits.** If something can't be done on Roku (see below), say so plainly. If you're unsure whether something works, say that too, and suggest trying it. Don't declare things impossible without checking.
- **Don't rush.** Small, testable steps beat one big change.

## Guided setup

When someone asks for help setting up, walk them through it in this order. Confirm each step works before moving on.

1. **Step 0: privacy settings** ([docs/roku-privacy-settings.md](docs/roku-privacy-settings.md)). No code needed. Always offer this first, even if they came for the launcher.
2. **Developer mode** ([docs/roku-setup.md](docs/roku-setup.md#1-turn-on-developer-mode)). They press the button sequence on their remote and tell you the Roku's IP.
3. **Choose their apps.** Run `python3 scripts/pull_logos.py --roku <ROKU_IP> --list`, show them the list, and ask which apps they want, in what order. Edit `m.apps` in `components/HomeScene.xml`.
4. **Pull logos.** `python3 scripts/pull_logos.py --roku <ROKU_IP>`
5. **Build the zip** with the command in [docs/roku-setup.md](docs/roku-setup.md#3-build-the-zip). It packs only the app, with `manifest` at the top level of the zip.
6. **Install** with Delete → Upload → Install on `http://<ROKU_IP>`. **Let them enter the `rokudev` password themselves.** Don't ask them to paste it into the chat.
7. **Check in.** Ask what they see on the TV. Then point them to [docs/faq.md](docs/faq.md) for common issues.

For Vizio, follow [docs/vizio.md](docs/vizio.md). Pairing shows a PIN on their TV, which they read to you or type in.

## Security rules (non-negotiable)

- **Never commit secrets:** API keys, Vizio auth tokens, Roku developer passwords, `genkey` passwords, signing keys. See [SECURITY.md](SECURITY.md).
- **Read secrets from environment variables** (`ANTHROPIC_API_KEY`, `VIZIO_IP`, `VIZIO_AUTH`, `ROKU_IP`, `JELLYFIN_IP`, `JELLYFIN_API_KEY`), never hardcode them in scripts.
- **Use placeholders in docs:** `<ROKU_IP>`, `<TV_IP>`, `<YOUR_AUTH_TOKEN>`. Never a real IP or token. `mychannel.json` keeps `YOUR_JELLYFIN_IP` and `YOUR_JELLYFIN_API_KEY`; real values only go into the build, as [docs/jellyfin.md](docs/jellyfin.md) explains.
- **Don't commit** `*.zip`, `*.pkg`, `.env`, or pulled app logos (`images/app_*.png` other than `app_uxd.png` and `app_family.png`). `.gitignore` covers these; don't override it.
- **Before every commit,** check the staged diff for anything that looks like a key, token, password or real local IP address.
- **Photos:** if adding images, check backgrounds for personal information and strip location metadata.
- **My Channel:** never put real Wi-Fi passwords or private info in `mychannel.json`. Use `${ENV_VAR}` in a link and let `make_qr.py` fill it in; the generated `qr_*.png` files are git-ignored, except the public `qr_about_*` and `qr_recipe_*` links the app needs.

## Repo layout

```
README.md                 Overview, before/after, quick start
ABOUT.md                  Who built this and why
CREDITS.md                Inspiration (Gathin23/cleanyourtv), tools, contributors
docs/                     Guides: privacy settings, Roku setup, My Channel, Jellyfin, Vizio, ad muter, FAQ, research
manifest                  App metadata (title, version, icons)
source/main.brs           Entry point: creates HomeScene
mychannel.json            My Channel content (made-up sample family, photos, videos, recipes, music, links); people edit this, not code
components/HomeScene.xml  App grid, app list (m.apps), My Channel page, key handling
components/Launcher.xml   Task that opens the selected app (roAppManager.LaunchApp)
components/AppTile.xml    One grid tile (the app's logo)
images/                   App art and guide screenshots; pulled logos live here locally
index.html, site/         The cleanyourroku.com website
make_stills.py            Makes My Channel photos from Jellyfin videos
scripts/pull_logos.py     Lists installed apps and pulls their icons via Roku ECP (port 8060)
scripts/make_qr.py        Makes QR code images for My Channel's Share Links (needs: pip3 install segno)
scripts/rokuremote.py     Phone remote (work in progress; only the CleanYourRoku button works so far)
```

## Roku facts to keep straight

- **One sideloaded app at a time.** Installing a new zip replaces the old one.
- **Back from an app goes to Roku's home**, not the launcher. Platform behavior; an app can't override it.
- **The ad panel on Roku's home screen can't be removed** by any setting. The launcher is an alternative home, not a modification of Roku's.
- **ECP** (`http://<ROKU_IP>:8060`) handles app lists, icons, keypresses and launching (`/launch/dev` opens the sideloaded app). A `403` means Network access under "Control by mobile apps" needs to be Permissive. See the FAQ.
- **Static analysis warnings** (`LaunchApp`, package size) don't block a beta.
- The launcher **curates**; it doesn't uninstall, block or lock apps. Never describe it as parental control.

## Writing docs

- **The project and the launcher are both called CleanYourRoku.** Early test builds were called Dreamer TV; only use that name when describing history or old screenshots.
- **Every guide explains why, not just how,** and ties back to human agency where it fits naturally.
- Clear, friendly, plain language. Short steps.
- Be honest about what's been tested: one Roku streaming player and one Vizio TV.
- Use "screenshot coming" placeholders rather than inventing images.
- This is unofficial and not affiliated with Roku or Vizio. Don't use their branding as if it were.
