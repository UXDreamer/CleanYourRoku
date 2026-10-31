# AI ad muter (optional, experimental)

> ⚠️ **Experimental.** This is a working prototype from my own setup, not a polished tool. It sometimes guesses wrong, it costs a little money per use, and it listens to your room. Read the whole page before you decide to use it.
>
> *Code coming to `scripts/`.*

## What it does

The ad muter listens to your TV, figures out when a commercial starts, and mutes the TV until the show comes back.

1. When you start it, it asks **what you're watching**, for example "Thursday Night Football."
2. Your Mac's microphone records the TV audio in short clips, about 8 seconds each.
3. [faster-whisper](https://github.com/SYSTRAN/faster-whisper) turns each clip into text **on your Mac**.
4. The text, plus what you said you're watching and a few recent lines from the show, goes to **Claude** (Haiku, Anthropic's fastest model), which answers one word: **AD** or **SHOW**.
5. After **two ADs in a row**, it mutes the TV through [pyvizio](vizio.md#3-control-the-tv-from-your-mac-with-pyvizio).
6. While muted, it **peeks** every 20 seconds, unmuting for about 6 seconds to listen. When Claude hears the show again, it stays unmuted.
7. **Safety limit:** it never stays muted longer than 3 minutes. Press Control-C to stop, and the sound comes back on.

Built with: Python, faster-whisper, sounddevice, the Claude API and pyvizio. Tested on a Vizio TV with a Mac.

## Why it exists

Commercials are the purest form of the problem this project is about: content picked for you, optimized for someone else, played whether you want it or not. Muting them is a small way of saying *my attention is mine*.

It's also a deliberate example of **AI as a partner, not a decision-maker**:

- **You set the context.** It asks what you're watching instead of guessing.
- **It leans toward not muting.** Claude is told "if unsure, answer SHOW," and it needs two AD answers in a row before muting. A missed ad is better than muting the game-winning play.
- **You stay in control.** It peeks, has a 3-minute limit, and Control-C always gives the sound back.

## What I learned trying a local model

I also tried a local model ([Ollama](https://ollama.com) with llama3.2) so nothing would leave my Mac. It kept **mistaking show dialogue for ads**, muting in the middle of scenes. Claude Haiku was much better at telling them apart, especially with the "what are you watching" context. That's a real trade-off: **privacy vs. accuracy**. I chose accuracy for this prototype, and you might choose differently.

## Before you use it: privacy

Be clear about what this does, so the decision is yours:

- **It listens to your room, not just the TV.** The microphone hears everything, including conversations. Clips are turned into text on your Mac, and **the text is sent to Anthropic's API** to classify. The audio itself isn't sent.
- **Don't run it when people are talking about private things nearby.** Stop it with Control-C.
- Each check is an API call to Claude, so it **costs a small amount** per use on your Anthropic account.

## Setup (when the code lands)

You'll need:

- A Vizio TV paired with pyvizio. See [vizio.md](vizio.md). Your TV IP and auth token go in environment variables, never in the code.
- An [Anthropic API key](https://console.anthropic.com) in an environment variable:
  ```bash
  export ANTHROPIC_API_KEY="<YOUR_API_KEY>"
  ```
  Never paste your key into the script or commit it. See [SECURITY.md](../SECURITY.md).
- Python packages:
  ```bash
  pip3 install faster-whisper sounddevice anthropic pyvizio
  ```
- Your Mac's microphone within earshot of the TV. macOS will ask Terminal for microphone permission the first time.

## Known limits

- **It guesses wrong sometimes.** Promos for other shows, ads that sound like the program, and quiet scenes are all hard.
- **Short ads slip through.** It needs two clips in a row (about 16 seconds) before muting, by design.
- **Vizio only, for now.** It mutes through pyvizio. A Roku version could use Roku's network control instead. Contributions welcome.
- **Experimental.** Treat it as a demo of what's possible, not a finished product.
