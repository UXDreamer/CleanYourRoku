# Security

This project talks to your TV over your home network, so a little care goes a long way.

## Never commit secrets

Do **not** commit any of these to this repo or include them in issues, pull requests or screenshots:

- **API keys**, for example a Claude API key used by the optional ad muter
- **Auth tokens**, for example the pairing token for a Vizio TV
- **Roku developer passwords**, the password you set when turning on developer mode
- **Signing keys**, the key Roku generates when you package an app for publishing

**Why:** once a secret is pushed to GitHub, assume it's public. It stays in the Git history even if you delete the file later, and bots scan public repos for keys within minutes. Someone with your Roku dev password on your network could install apps on your TV. Someone with your API key could run up charges on your account. Someone with your signing key could publish updates in your name.

**How to keep them out:**

- Keep secrets in environment variables or a local config file, and make sure that file is listed in [`.gitignore`](.gitignore).
- Before you commit, run `git diff --staged` and read what's going in.
- Blur IP addresses, tokens and passwords in screenshots.

**If you accidentally committed one:** revoke or change it right away (a new API key, a new dev password, re-pair the TV). Deleting the file isn't enough, because the old value is still in the history.

---

## Reporting a problem privately

If you find a security issue, like a script that exposes something it shouldn't or a secret that slipped into the repo, please **don't open a public issue.**

Instead, report it privately through the repo's **Security** tab:

**[Report a vulnerability](https://github.com/uxdreamer/CleanYourRoku/security/advisories/new)**

Include what you found, where, and how to reproduce it if you can. I'll respond as soon as I can and credit you in [CREDITS.md](CREDITS.md) once it's fixed, if you'd like.

---

## Run code with care

Fake copies of popular TV-debloat repos circulate. Only use code from this repo or the original projects credited in [CREDITS.md](CREDITS.md), and **read what a script does before you run it on your TV.** You can ask Claude or another AI tool to explain a script line by line first. That's exactly the kind of partnership this project is about.
