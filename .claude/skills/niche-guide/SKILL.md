---
name: niche-guide
description: Creates a new FollowThrough niche guide (a trade like pressure washing or pest control) at the same depth as the roofing guide, or deepens an existing thin one (HVAC, plumbing...). Interviews the user about the niche first, then writes the matching T and FULL entries into index.html. Use when the user wants to add a niche or trade, expand a guide to roofing's depth, or says /niche-guide.
argument-hint: <niche, e.g. "pressure washing">
---

# Niche guide

Niche: **$ARGUMENTS**. If empty, ask which niche, and offer the "More trades" list in `docs/07-roadmap.md` plus any existing guide that `check.js` reports as thin.

Read before writing: the roofing entries in `index.html` (`{s:"roofing"` in `T`, `FULL={roofing:` in `FULL`). They are the gold standard. Also read the style rules in `docs/03-content-and-sales.md`.

## Why roofing is deep (the bar)

The other guides were written to a short generic template: LLC, insurance, tools, "follow up on quotes". Roofing is deep because every section answers a question **only someone who knows roofing could answer**: price per square, workers' comp as the biggest cost, deposits funding materials, storm-chasing rules, the deductible-waiver trap, OSHA fall protection, aerial measurement reports. Generic advice that fits any trade does not count toward depth.

So before writing anything, work out these twelve things for the niche:

1. **Ramp**: the low-risk starter job and the core money job (roofing: repairs, then full replacements).
2. **Pricing unit**: how the trade quotes (per square, per visit, per truckload, per room, flat-rate book).
3. **Biggest cost driver**: the line that surprises new owners (workers' comp).
4. **Cash-flow pattern**: who pays when, and what the owner fronts (materials before the customer pays).
5. **Licensing map**: 2–3 named states that license it, 1 that doesn't, what licensing takes, how long.
6. **Legal trap**: the rule new owners break without knowing (waiving deductibles, storm solicitation).
7. **Safety, employment or environment rule** that applies once they hire or operate (OSHA falls, EPA, runoff).
8. **Lead channels** specific to the niche (storms, realtors, property managers).
9. **Trust worries** buyers have (will you be around for the warranty, why a deposit).
10. **Seasonality and ops** (storm season, rescheduling for weather).
11. **Who to position against** (big roofers) and how small owners win.
12. **Niche tools**, named products (EagleView, Hover).

## Step 1: Draft silently

Draft the twelve answers from your own knowledge. Mark each one as either confident or a guess or judgment call. Don't show the draft yet.

## Step 2: Interview the user

Use AskUserQuestion. Ask at most 2 rounds of up to 4 questions. Put the option you recommend first, labelled "(Recommended)" and taken from your draft, so the user can accept it quickly. Don't ask anything you can know or look up yourself, such as the EIN being free or how to form an LLC.

**Round 1: scope (always ask)**
- **Category**: the existing `CATS` entries, plus "New category". Deepening an existing guide keeps its category, so skip this question then.
- **Starting scenarios**: the two set-ups that become `costnote` and the ends of `T.cost`. For example: "Solo, own truck, repairs only" and "Crew-ready with equipment". Give options that fit the niche.
- **Customer mix**: residential, commercial or both. This changes the objections, lead channels and FAQ.
- **Research**: "Verify licensing, costs and rates on the web (Recommended)" or "General knowledge only".

**Round 2: built from your draft.** Choose the 2–3 dimensions that were guesses or judgment calls and turn each one into a question with options specific to the niche. Common ones are the pricing unit and the example job, which legal trap to stress, and which tempting but risky revenue source the FAQ should cover. Always add one more question: "Have you heard real objections or customer phrases from [niche] owners?" Give it the options "No, use your draft (Recommended)" and "Skip". The user types their own material through Other. Real phrases from the field beat your draft, because the business plan says to use customers' exact words.

If research is on and WebSearch is available, run it now. Check which states license the niche, typical insurance and equipment costs, and typical rates for the pricing unit. Sources go in your final report, not on the site.

## Step 3: Write the entries

**`T` entry.** Put it after the last entry in the same category, because order within a category sets the tile order. Fields: `s` kebab slug, `n` name, `c` category index, `full:1` (marks a guide at roofing depth), and these:
- `cost`: an overall range whose ends match the two `costnote` scenarios.
- `season`: when the work is busy and what spikes demand, in 1–2 sentences.
- `fit`: who the niche suits, plus the hard truth about it (barrier, cost, risk).
- `spend`: a comma list of where the money goes.
- `tips`: exactly 7, one per `STEPS` item in order: LLC, EIN, bank, insurance, prices, first customers, objections. Tip 2 is always "Free at irs.gov." Every other tip must be specific to the niche.

**`FULL` entry.** For a new niche, add it to the `Object.assign(FULL,{...})` block and quote any key that has a hyphen. For an existing guide, rewrite it in place and keep anything already accurate. Each field needs the following, and none may have fewer items than roofing has:

| Field | Count | What each item must do |
|---|---|---|
| `lic` | 5 | (1) How rules vary by state, naming states that do and don't license it, ending "Confirm with your state licensing board." (2) What licensing takes (experience, exam, insurance, bond) and how long, "so start early". (3) Permits, plus local rules on how the niche sells (door-to-door, solicitation). (4) The legal trap, said plainly. (5) The safety, employment or environment rule. |
| `cost` | 8 rows `[item, range]` | Setup (LLC, license, bond). Liability insurance "per year". The niche's big insurance or compliance cost. Safety gear or certification. Tools and equipment. Vehicle "if you don't already own one". Software, website and marketing. Working capital for materials or supplies until customers pay. A row can say something qualitative ("Depends on payroll and state") when a range would mislead. |
| `costnote` | 1 | "Bare minimum (assumptions in parentheses) is roughly $X–$Y. A [full set-up] start is closer to $X–$Y. These are estimates, so get real quotes." |
| `plan` | 4 `[phase, text]` | Use exactly the phases Weeks 1–2, Weeks 3–4, Month 2 and Month 3. Give concrete counts ("Do 5–10 small repairs", "Introduce yourself to 10 local realtors"). Ramp from the starter job to the core money job. Month 3 includes following up on quotes "within 48 hours and again at 5 days" and checking which lead sources paid off. |
| `price` | 1 | A worked example in the niche's pricing unit. Define the unit, use a realistic job size, multiply cost per unit to get a subtotal, add the niche's extras (waste, dump fees, permits), then add an overhead and profit % to reach a final range. List what to itemize. End with "Your own costs will differ, so treat this as an example." **Do the arithmetic yourself and check every number.** In the roofing example, 28 × $330 = $9,240, plus $600 is $9,840, and adding 25–35% gives about $12,300–$13,300. |
| `mistakes` | 6 | Each one is a mistake plus its consequence or fix. Cover cash flow, insurance, contract or scope gaps, underpricing (with the concrete fix, such as roofing's per-sheet clause for hidden damage), regulation, and letting quotes go cold. |
| `obj` | 8 `[“objection”, “answer”]` | Adapt roofing's set to the niche: a competitor's price is lower; "I need more quotes"; "I need to talk to my spouse" (a manager or owner for commercial work); "Can you do it cheaper?"; the niche's alternative payer or alternative (insurance, DIY, renting a dumpster); delay, with what waiting costs; "will you be around?" or trust; payment terms or the deposit. Every answer follows the method: acknowledge, ask a question, answer honestly, give a concrete next step (a day, a one-page summary, photos). |
| `faq` | 5 `[q, a]` | "Can I start with just [starter job]?". A requirement question ("Do I need X if I work alone?"). "How do I get paid?" (payment structure, plus checking the state's limits). "Should I do [tempting but risky revenue source]?". "How do I compete with big [niche] companies?" |
| `tools` | 4 | Quoting and invoicing (name the products, plus "a simple spreadsheet to start"). The niche's estimating or measuring tool (name it). Reviews (Google Business Profile plus a text link after every job). Scheduling plus one niche ops helper (roofing uses a weather app). |

**Style (the site will break or drift without these):**
- Plain US English, short sentences, second person. Honest and low-pressure. No income promises. Never suggest anything illegal.
- Rules vary by state, so say so. Costs are always ranges and always labelled as estimates.
- Use curly quotes “ ”, the curly apostrophe ’ and the en dash – in ranges. No em dashes. Never put a straight quote that matches the string's delimiter inside the string. No `<` or `>`, because strings are injected as HTML.
- Match the quote style of the block you're editing: double quotes in `T` and in the roofing block, single quotes inside `Object.assign`.

**A new niche also needs these:**
- In the `home()` text, change "for ten trades" to the new count in words.
- Add the route to the routes table in `docs/02-website.md` and to the trades list in `docs/03-content-and-sales.md`.
- A new category is appended to `CATS`. Never reorder `CATS`, because `c` is an index into it.

## Step 4: Check

Run `node .claude/skills/niche-guide/check.js <slug>`. It must print `OK` and exit with code 0. It checks the field counts against roofing, the 7 tips, the row shapes, the style rules and the home-page count, and it also catches syntax errors in the data. Then tell the user to open `index.html` and go to `#<slug>` to look at the page.

## Step 5: Report

Keep the report short:
- What was added.
- Which claims came from research, with source links, and which came from general knowledge and still need checking before publishing.
- Any interview answer that changed the content.
