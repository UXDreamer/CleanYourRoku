# Research: recommender systems and human agency

This project is the smart TV case study in my Human Systems Engineering paper (HSE 524, Arizona State University) on recommender systems and human agency.

📄 **Paper: "From Audience to Main Character" (link coming soon).**

---

## The short version

Recommender systems are everywhere: in what we **buy**, what we **watch**, and what we **see**. The answer isn't to avoid AI. It's to work with it while keeping **human agency**:

1. **Know** what the system is doing.
2. **Question** it.
3. **Keep the final decision** for yourself.

---

## Recommender systems

A recommender system predicts what you'll want and puts it in front of you. Netflix rows, Amazon's "Customers also bought," TikTok's For You feed and the rows on Roku's home screen are all recommender systems.

**Personalization isn't simply bad.** The catch is *who it's optimized for*. These systems are tuned for the company's goals: watch time, purchases, ad revenue. When the company's goals and yours line up, it feels like help. When they don't, you mostly see what pays them.

On Roku, that's literal. The [home screen](roku-privacy-settings.md#the-problem-your-apps-come-last) puts about seven rows of recommendations above the apps you chose, next to an ad panel you can't turn off.

---

## Filter bubbles

The term comes from Eli Pariser (*The Filter Bubble*, 2011). When a system shows you more of what you've already engaged with, your world quietly narrows, and from the inside it doesn't feel like narrowing. It feels like the system "knows you."

That feeling is exactly why filter bubbles are hard to notice. The more convenient the recommendations, the less you notice what you're *not* being shown.

---

## Automation and human agency

From human factors research:

- **Automation bias:** the tendency to accept an automated system's output without enough scrutiny, even when other information suggests it's wrong. Recommendations work partly because accepting them is easier than searching.
- **Levels of automation** (Parasuraman, Sheridan & Wickens, 2000): automation isn't all-or-nothing. A system can suggest options, narrow them, pick one for you, or act without telling you. Most recommender systems have quietly moved up those levels, from *suggesting* toward *deciding*.

**The trade-off:** automation gives you convenience in exchange for control, and here also for tracking. That trade can be worth it, but only if it's a choice you actually made.

This project applies the same principle to building with AI. I used AI heavily, but as a partner: it suggested, I questioned, and I decided. When it said publishing a Roku beta was impossible, I tried anyway, and it worked. See [ABOUT.md](../ABOUT.md).

---

## Defaults and buried settings

Most people never change defaults, so **the default *is* the decision** for most users.

- **Roku:** tracking and personalized ads are on by default. The off switches exist but are spread across menus. See [Step 0](roku-privacy-settings.md).
- **Vizio:** "Viewing Data" (automatic content recognition) is on by default. In 2017, Vizio paid $2.2 million to settle FTC and New Jersey charges over collecting viewing data without consent. See [vizio.md](vizio.md).

When the privacy-protecting option exists but is buried, agency is technically available but practically taken. That's not real consent.

**Equity risk:** when a clean, ad-free experience costs extra, control becomes a luxury. People who can't pay, or can't code their own home screen, get the default.

---

## Control should be the default

Most people can't, and shouldn't have to, build their own home screen. The fix belongs in the product:

- **A clear yes/no choice at setup** for tracking and personalized ads, not a pre-checked box.
- **Tracking off unless you turn it on.**
- **A "my apps only" home screen mode**, built in, for anyone who wants it.

CleanYourRoku is a working demonstration that this is possible. If one person can build it on a Roku with AI's help, the company that makes the Roku can ship it as a setting.

---

## Further reading

A starting list. Full references will be in the paper.

- Eli Pariser, *The Filter Bubble: What the Internet Is Hiding from You* (2011)
- Parasuraman, Sheridan & Wickens, "A Model for Types and Levels of Human Interaction with Automation," *IEEE Transactions on Systems, Man, and Cybernetics* (2000)
- Federal Trade Commission, *Vizio settlement over collection of viewing data* (2017)
- [Gathin23/cleanyourtv](https://github.com/Gathin23/cleanyourtv), the project that inspired this one
