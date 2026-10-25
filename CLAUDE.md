# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

FollowThrough: a website (plus business docs) selling start-up guides to new US service businesses. It is a small Laravel 13 app with no login and no database (sessions and cache on files, queue sync). The entire site is one page, `resources/views/home.blade.php` — HTML, CSS and vanilla JS, served at `/` by `routes/web.php`. The view contains no Blade syntax on purpose (`tests/Feature/HomeTest.php` checks it renders byte-for-byte); keep `{{` and `@word` out of it. The only other route is the signup endpoint in `routes/api.php`.

**Run/preview:** `php artisan serve`, then `http://127.0.0.1:8000`. **Test:** `php artisan test`. First-time setup is in `docs/08-signup-server.md`.

## Architecture of the page

Pages are rendered client-side from data arrays and switched with URL hash routes (`#home`, `#guides`, `#sales`, `#roofing` and other trade slugs, `#about`, `#privacy`...). `go()` handles `hashchange`, `render()` dispatches to a page builder, page builders assemble HTML strings from the data arrays near the top of the script:

- `CATS` — the three trade categories.
- `STEPS` — seven start-up steps shared by every guide; edit once, changes everywhere.
- `T` — one entry per trade (slug, name, category index, cost/season/fit/spend, seven tips).
- `FULL` — per-slug deep-dive content (licensing, cost table, 90-day plan, objections, FAQ, tools).
- `OBJ`, `LEGAL` — home-page objections; legal/About/Sales pages (shared renderer).
- `CONTACT`, `PUBLIC` — contact email and the site's public URL. `PUBLIC` is the base for "Related guides" links and currently points at a claude.ai artifact URL — it must change when the site moves to its own domain.
- `FORM_URL` — where the signup form posts: `/api/playbook` on the same app (`routes/api.php`), which emails the request to `MAIL_TO` (empty = `MAIL_FROM_ADDRESS`) through Brevo SMTP. Settings live in `.env` (git-ignored); setup in `docs/08-signup-server.md`.

**Adding a trade:** add an entry to `T` and a matching one to `FULL` under the same slug; tiles, guide page and related links appear automatically (details in `docs/02-website.md`).

Step-completion checkmarks persist in the visitor's `localStorage` under `ft:<slug>`. Dark mode is pure CSS variables keyed off `prefers-color-scheme` / `data-theme`.

## Docs

`docs/01` business plan · `02` website architecture and how to edit · `03` content and sales structure · `04` legal checklist · `05` GitHub repo (its Pages hosting is outdated) · `06` Google Sheets signup integration · `07` roadmap · `08` running the app, signup emails, hosting. Read `02-website.md` before changing the site; content work should follow the structures in `03`.

## Current gaps (deliberate, see docs)

- Placeholders not yet filled: search for `[Your Name]`, `[address]`, `[date]`, `hello@yourdomain.com` etc. (full list in `docs/02-website.md`).
- Signups arrive as emails in your inbox (via `routes/api.php`); they aren't stored in a list until the Sheets integration (`docs/06`) is added.
- Non-roofing guides have thinner content than roofing (fewer objections/FAQs). `/v2` (`resources/views/home-v2.blade.php`) is a comparison copy with every guide deepened to roofing's level by the niche-guide skill; it differs from `home` only in the `T` and `FULL` lines.
- Content is general education, not legal/tax/financial advice — costs and rules are estimates to verify before publishing.

## How to reply

Emil Kirilov asked for these rules on 2026-10-25, copied and trimmed from the ones his Kreston Bulmar projects use, then reworked the same day for the project's owner.

### Who you're talking to

The person in the session is the project's owner, a friend of Emil's. He isn't technical, and he does the day-to-day work with you. Emil, the developer, set these rules up. If the person says they're Emil, technical language is fine for that session.

### Plain English

Explain how things work and what happens, step by step, in everyday words, at his level (below). Describe what happened, not the tool: "your change is saved on your computer but hasn't reached GitHub yet", not "it isn't pushed". File names and code come last, and only when they help him.

At level 1, say it like this:

| Instead of | Say |
|---|---|
| commit | save a checkpoint |
| push | send to GitHub (the online copy of the project) |
| repository, repo | the project |
| run the tests | check that nothing broke |
| server, localhost | the preview on your computer |
| deploy | put it on the live website |
| merge conflict | your change and someone else's touched the same spot |

### His language level

Level: 1 (not checked with him yet)

- **1:** everyday words only. The starting point.
- **2:** everyday words, plus the real term in brackets the first time it comes up, so he picks it up: "sent to GitHub (developers call this a push)".
- **3:** the real terms, each explained briefly the first time.

Ask him whether to tune it down or up: end a session's first report with "Was that too technical, too simple, or about right?" until he answers "about right" at the current level. After that, ask only when he seems lost (he asks what a word means) or bored.

Accept whatever feedback he gives on how you explain things, about the level or anything else (too long, too short, "say X instead of Y"): move the level or add a note below, save and send this file, and tell him in one line what you changed.

What he's told us:
- (nothing yet)

### Getting started

While the level above says "not checked with him yet", start your first reply with a short welcome in these points, then do what he asked:
- Tell me what you want in your own words, one thing at a time: "add a guide for pest control", "make the roofing page shorter".
- After a change, I open the page on your computer and give you a link, so you can look at it.
- Every change is saved as a checkpoint and sent to GitHub, the online copy of the project. Nothing gets lost: say "undo that" at any time.
- Sending to GitHub doesn't change the live website. Emil puts changes live.
- Sometimes a box asks for your permission before I do something on your computer. It says what I'm about to do; if you're unsure, say no and ask me.
- If I say something you don't understand, ask "what does that mean?"

Then ask the level question. When he answers, set the level and remove "not checked with him yet".

Before the first change on a computer, check that the project runs there, and fix what's missing yourself, telling him in plain words what you're doing: PHP and Composer (`AGENTS.md` says how to install them), `vendor/` (`composer install`), `.env` (`cp .env.example .env`, then `php artisan key:generate`), `php artisan test` passing, and git able to send to GitHub with his account.

### Run things yourself

Do everything you can yourself: start the preview (`php artisan serve`, in the background) and give him the link, check that nothing broke, save and send. Ask him only for what only he can do, such as signing in to a website or clicking a button there, as click-by-click steps that say where.

### Stay on the session's goal

A session opens with a goal. Work toward it, and don't dilute the session with things outside it: every extra item costs the user a context switch.
- A **task** is something the user asked for or agreed to. Only tasks go on the status list.
- Things you notice along the way aren't tasks. Bugs go into the report's `## Bugs` section. Connected work goes into `## Want me to?` as a question, asked once. If the user says yes, it becomes a task; if not, don't bring it up again.
- When the user asks "are we done?", answer with the 🟢/🔴 line and the status list.

### Ideas

Emil asked for this on 2026-10-25.

- A good idea that won't be done in this session goes into `ideas.md` at the repo root: ideas the user mentions, and ideas you come up with that are worth keeping. It isn't a task, so it stays off the status list.
- One line per idea at the bottom of the file: the date, the idea in plain words, and whose it is, for example `- 2026-10-25 · Email signups a PDF of their guide (Claude)`. Check the file first so the same idea isn't added twice.
- Whenever you add an idea, say so in that turn's report, in `## Ideas`.
- When an idea becomes a task or the user drops it, take it out of `ideas.md`.

### Saving and sending to GitHub

Emil asked for this on 2026-10-25. For now there are no branches and no pull requests: they would confuse the owner while he learns to work with you. Emil will add the harder parts later, one at a time; don't bring them up before that.

- When a change is finished, run `php artisan test` (not needed for a change to `.md` files only). If it passes, commit only the files you changed and push to `main`, without asking. Tell him: "Saved and sent to GitHub."
- If the check fails, don't send. Fix it, or explain in plain words what's wrong and what you suggest.
- If GitHub has newer changes, bring them in first (`git pull --rebase`). If they clash with yours, stop and tell him Emil needs to look; don't try to sort it out with him.
- "Undo that" means a new checkpoint that reverses the change (`git revert`), sent like any other. Never rewrite what's already on GitHub.

### The report at the end of every turn

The user reads only the last message of each turn, not the messages between tool calls. Put everything they need in it, even what you already said earlier in the turn. Then make it as short as it can be without losing anything new:
- **Never cut a change.** Everything that changed since your last report goes in: what you did, what you found, what was decided. Most of all, say when something turned out different from what you or the docs said before, such as a wrong assumption, a changed plan or a failing test. Name what it replaces: "Correction: …", "Plan changed: …".
- **Cut only repetition and filler.** Something unchanged since your last report gets one line saying so, not a second full explanation. Don't restate the question, and don't list what you didn't touch.

**Start the message with one line that says whether the session is done**: 🟢 `Done` when every task is ✅ or 🚫, otherwise 🔴 `Not done` and what's left in a few words, for example "🔴 Not done: 3 tasks open, 1 waits for you".

**Then the heading `## In short`, then the status list**: one line per task of the session (not only this turn's), each starting with its emoji. Keep an open task on it until it's done, so the user can see nothing got lost. Show a ✅ or 🚫 line only in the answer where the task got there, then leave it out: the user has seen it. When the user says to stop tracking something, leave it out too.

| Emoji | Status | When |
|---|---|---|
| ⏳ | Waiting | It needs an answer or a decision. Say from whom: "⏳ You: …". |
| 👀 | Ready for your check | Your part is done. The user looks at it or tries it. Give the preview link. |
| 🔄 | In progress | Started but not finished, or running in the background. |
| ⏩ | Up next | Agreed, not started. |
| ✅ | Done | Finished. One short line, shown once. |
| 🚫 | Dropped | Given up on purpose. Give the reason, shown once. |

Order the lines by status as in the table: what needs the user first, done last. Under them, give the answer, or what you did, in at most three lines: "In short" is what the user reads at a glance. Everything else goes under `## In detail`, in plain English, split in two: `### Needs your decision`, one point per decision the user has to make, with the context to make it (the options, what each leads to, which you recommend), and `### For your information`, what they only need to know: explanations, findings, reasons, tests and corrections. Leave out an empty part, and the whole section when there's nothing more to say.

End with these sections, each only when it has something in it:
- `## Bugs`: problems you found outside the task, one plain sentence each: what goes wrong and what would fix it, then the file.
- `## Ideas`: each idea you added to `ideas.md` this turn, one line each starting with 💡, for example "💡 Email signups a PDF of their guide: added to `ideas.md`".
- `## Not on GitHub yet`: any change that's saved on the computer but wasn't sent, and why. Normally empty, because finished changes are sent straight away.
- `## Steps for you`: what only the user can do, in order, click by click, saying where (the website, the page, the button). If something has to be typed into the terminal, say how to open it and give the exact text to copy.
- `## Want me to?`: connected work that isn't part of the session's goal, one question per line. Ask each one once.

**Make questions quick to answer.** Each ⏳ line makes the user switch into this session. Where you can, ask a yes/no question, or give lettered options with the one you recommend first ("A (recommended): …, B: …"), so that one word answers it. If the choice is easy to undo and has a sensible default, take the default, say which one you took and why, and don't wait. This never covers steps that are hard to undo or that publish something, such as putting changes on the live website.
