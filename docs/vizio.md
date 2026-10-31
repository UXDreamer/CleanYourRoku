# Vizio TVs

Vizio is a different kind of problem from Roku. Roku is **semi-open**: it has an official developer mode, so you can install your own home screen. Vizio is **locked down**: no developer mode, and a home screen you can't replace.

So on Vizio, taking control back means three things:

1. **Turn off the tracking** in settings (no code).
2. **Control the TV yourself** over Wi-Fi from a Mac, with [pyvizio](https://github.com/vkorn/pyvizio).
3. **Skip Vizio's home screen entirely** with an Apple TV (no code).

Tested on one Vizio TV. Menu names vary by model and software version, so look for the closest match.

---

## 1. Turn off Viewing Data (no code needed)

**Path:** Menu → **Admin & Privacy** → **Viewing Data** → **Off**

**Why:** Viewing Data is Vizio's name for **automatic content recognition (ACR)**. The TV identifies what's on screen, including from your cable box, game console or streaming stick, and that data can be used for advertising. In 2017, Vizio paid $2.2 million to settle charges from the FTC and the New Jersey Attorney General that it collected viewing data from millions of TVs without consent. The setting exists now, but it's on by default, and that's the problem this project is about: agency taken by default, returned only if you go looking.

---

## 2. Limit Ad Tracking (no code needed)

**Path:** Menu → **Admin & Privacy** → **Advertisements** → **Limit Ad Tracking** → **On**

**Why:** this tells Vizio not to use your viewing to personalize ads. You'll still see ads, just not ones built from a profile of you. Like Roku's version, it's a request apps are supposed to honor, not a wall.

While you're in **Admin & Privacy**, look through the other options. Vizio sometimes adds new data-sharing settings in updates.

---

## 3. Control the TV from your Mac with pyvizio

[pyvizio](https://github.com/vkorn/pyvizio) is an open-source Python tool that talks to Vizio SmartCast TVs over your local network. Once paired, you can turn the TV on, switch inputs, change the volume and open apps from Terminal, or from a phone remote you build on top of it.

**Why bother:** Vizio decides what its remote and home screen show you. Talking to the TV directly means you choose what one tap does, like "go straight to my Apple TV," without passing through Vizio's home screen and its recommendations.

### Install

```bash
pip3 install pyvizio
```

If Terminal then says `pyvizio: command not found`, pip installed it in a folder that isn't on your PATH. On a Mac that's usually `~/Library/Python/3.x/bin`. Add that folder to your PATH, or run pyvizio with its full path.

### Find your TV

```bash
pyvizio discover
```

Note your TV's IP address. Below it's written as `<TV_IP>`. You can also find it in the TV's network settings.

### Pair (one time)

Turn the TV on, then:

```bash
pyvizio --ip=<TV_IP> --device_type=tv pair
```

A PIN appears on the TV, and Terminal prints a **challenge token**. Finish pairing with both:

```bash
pyvizio --ip=<TV_IP> --device_type=tv pair-finish --token=<CHALLENGE_TOKEN> --pin=<PIN_ON_TV>
```

This prints your **auth token**. If pairing doesn't respond, try adding the port: `--ip=<TV_IP>:7345`.

> **Keep the auth token private.** Anyone on your Wi-Fi with it can control your TV. Don't paste it into code you share, issues or screenshots, and never commit it. See [SECURITY.md](../SECURITY.md).

**Store it safely.** Put the IP and token in environment variables instead of in your scripts. Add these lines to `~/.zshrc`:

```bash
export VIZIO_IP="<TV_IP>"
export VIZIO_AUTH="<YOUR_AUTH_TOKEN>"
```

Then open a new Terminal window.

### Commands

```bash
V="pyvizio --ip=$VIZIO_IP --device_type=tv --auth=$VIZIO_AUTH"

$V power toggle          # on/off
$V input HDMI-2          # jump straight to an input (e.g., your Apple TV)
$V next-input            # cycle inputs
$V volume up             # volume
$V mute toggle           # mute
$V launch-app YouTube    # open an app by name
$V key-press OK          # remote buttons: UP, DOWN, LEFT, RIGHT, OK, BACK, MENU
```

Your HDMI input number may differ. Check which port your devices are plugged into.

---

## 4. Skip Vizio's home screen with an Apple TV (no code)

If you have an Apple TV, or any streaming box with HDMI-CEC, you can make the Vizio home screen something you almost never see.

1. **On the Vizio:** Menu → **System** → **CEC** → **Enable**.
2. **On the Apple TV:** Settings → **Remotes and Devices** → **Control TVs and Receivers** → **On**.

Now pressing a button on the Apple TV remote wakes the TV and switches it straight to the Apple TV. You land on a home screen *you* arranged instead of Vizio's.

**Why this counts:** sometimes the best fix isn't code. You can't change Vizio's home screen, but you can decide you don't have to go through it. CEC is a standard feature that's already in your TV, just not set up to put you first.

*Screenshot coming: Apple TV home screen after waking the Vizio over CEC.*

---

## Bonus: a phone remote

I built a small phone remote on top of pyvizio: a web page served from my Mac, opened on my iPhone, with big buttons for the apps and inputs I actually use, in the order I want. It runs pyvizio commands like the ones above. *Code coming to `scripts/`, with the IP and token read from environment variables.*

There's also an optional [ad muter](ad-muter.md) that uses pyvizio to mute commercials. It's experimental.

---

## Honest limits

- **You can't replace Vizio's home screen.** There's no developer mode, so no CleanYourRoku launcher on Vizio. The Apple TV workaround is the closest you can get.
- **Settings can change with updates.** Check the Admin & Privacy menu again after a big software update.
- **Tested on one Vizio TV.** If yours is different, please [add your notes](../CONTRIBUTING.md).
