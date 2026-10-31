# About

## Who I am

I'm **Damien Pressley**, also known as **UX Dreamer**. I'm a graduate student in Human Systems Engineering at Arizona State University, where I study how people and technology work together, and where that partnership breaks down. I live in Mesa, Arizona, and I'm originally from Philadelphia.

GitHub: [@dlpressl](https://github.com/dlpressl)

---

## Why this exists

When [cleanyourtv](https://github.com/Gathin23/cleanyourtv) went viral, people were using Claude Code to strip the ads and clutter off their Android and Google TVs. The comments on TikTok kept asking the same question:

> "How can you do this for Roku?"

Nobody had an answer. Every project in the trend relied on Android's developer tools, and Roku works completely differently. I had a Roku, and I had the same frustration everyone in those comments had, so I went looking for the answer myself.

CleanYourRoku is what I found: a privacy guide that anyone can follow without code, and a custom home screen, the **CleanYourRoku launcher**, for anyone who wants to go further.

Why it matters to me: recommender systems decide a lot of what we watch, buy and see, and they're designed to serve the company first. I don't think the answer is to avoid AI. I think the answer is to keep your agency: know what the system is doing, question it, and keep the final decision for yourself.

---

## The human agency story

This project was built with AI. It was also shaped by the moments I disagreed with it.

**When the AI said it couldn't be done.** At one point the AI told me that publishing the launcher as a Roku beta wasn't possible. I didn't take that as the final word. I kept digging, tried it anyway, and it worked. The beta got published.

**When the AI got it wrong.** I caught bugs along the way myself, including a doubled paste and a menu that looped instead of doing what it should. AI moves fast, and moving fast makes mistakes easy to miss if nobody is checking the work.

That's the whole idea in practice: **AI is a partner, not a decision-maker.** It sped up the work. Human judgment got it over the line.

---

## How I worked with AI

**Talk first, plan together, then build.**

1. **Talk first.** Before writing any code, I talked through the problem: what I wanted, why the existing projects didn't cover Roku, and what Roku does and doesn't allow.
2. **Plan together.** We worked out the approach step by step, and I made the decisions about what went on the screen and what didn't.
3. **Then build.** Code came last, in small pieces I could test on the TV and check myself.

This is different from the "vibe coding" habit of prompting for results as fast as possible and accepting whatever comes back. That approach can feel productive, but it hands your judgment to the tool. Slowing down to talk and plan meant I understood what I was building, caught problems early, and kept the decisions mine.

If you use this repo with Claude Code or any other AI tool, I'd encourage the same approach. Ask it to explain before it acts, and read what a script does before you run it on your TV.

---

## Research

This project is also the smart TV case study in my HSE 524 paper on recommender systems and human agency. More in [docs/research.md](docs/research.md).
