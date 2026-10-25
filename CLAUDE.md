# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

FollowThrough: a website (plus business docs) selling start-up guides to new US service businesses. It is a small Laravel app with no database. The entire site is one page, `resources/views/home.blade.php` — HTML, CSS and vanilla JS, served at `/` by `routes/web.php`. The view contains no Blade syntax on purpose (`tests/Feature/HomeTest.php` checks it renders byte-for-byte); keep `{{` and `@word` out of it. The only other route is the signup endpoint in `routes/api.php`.

**Run/preview:** `php artisan serve`, then `http://127.0.0.1:8000`. **Test:** `php artisan test`. First-time setup is in `docs/08-signup-server.md`.

## Architecture of the page

Pages are rendered client-side from data arrays and switched with URL hash routes (`#home`, `#guides`, `#sales`, `#roofing` and other trade slugs, `#about`, `#privacy`...). `go()` handles `hashchange`, `render()` dispatches to a page builder, page builders assemble HTML strings from the data arrays near the top of the script:

- `CATS` — the three trade categories.
- `STEPS` — seven start-up steps shared by every guide; edit once, changes everywhere.
- `T` — one entry per trade (slug, name, category index, cost/season/fit/spend, seven tips).
- `FULL` — per-slug deep-dive content (licensing, cost table, 90-day plan, objections, FAQ, tools).
- `OBJ`, `LEGAL` — home-page objections; legal/About/Sales pages (shared renderer).
- `CONTACT`, `PUBLIC` — contact email and the site's public URL. `PUBLIC` is the base for "Related guides" links; it is empty, so they open on the current page and address (works on any domain, and on `/v2`).
- `FORM_URL` — where the signup form posts: `/api/playbook` on the same app (`routes/api.php`, emails the request to `MAIL_TO`).

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

Emil Kirilov asked for these rules on 2026-10-25, copied and trimmed from the ones his Kreston Bulmar projects use.

### Plain English

Explain things in plain English first: what happens, step by step, in everyday words. File names, line numbers and code terms come after, as supporting detail, not instead of the explanation.

### Stay on the session's goal

A session opens with a goal. Work toward it, and don't dilute the session with things outside it: every extra item costs the user a context switch.
- A **task** is something the user asked for or agreed to. Only tasks go on the status list.
- Things you notice along the way aren't tasks. Bugs go into the report's `## Bugs` section. Connected work goes into `## Want me to?` as a question, asked once. If the user says yes, it becomes a task; if not, don't bring it up again.
- When the user asks "are we done?", answer with the 🟢/🔴 line and the status list.

### Branches and pull requests

Emil asked for this on 2026-10-25.

- Every branch gets a pull request. As soon as a branch has its first commit, push it and open one, as a draft while the work isn't finished. Never leave a branch without a pull request.
- Always give the pull request's link: in `## Branches`, and in any status line or decision about that branch.
- Merging is the user's decision. Ask, and wait for a yes.

### The report at the end of every turn

The user reads only the last message of each turn, not the messages between tool calls. Put everything they need in it, even what you already said earlier in the turn. Then make it as short as it can be without losing anything new:
- **Never cut a change.** Everything that changed since your last report goes in: what you did, what you found, what was decided. Most of all, say when something turned out different from what you or the docs said before, such as a wrong assumption, a changed plan or a failing test. Name what it replaces: "Correction: …", "Plan changed: …".
- **Cut only repetition and filler.** Something unchanged since your last report gets one line saying so, not a second full explanation. Don't restate the question, and don't list what you didn't touch.

**Start the message with one line that says whether the session is done**: 🟢 `Done` when every task is ✅ or 🚫, otherwise 🔴 `Not done` and what's left in a few words, for example "🔴 Not done: 3 tasks open, 1 waits for you".

**Then the heading `## In short`, then the status list**: one line per task of the session (not only this turn's), each starting with its emoji. Keep an open task on it until it's done, so the user can see nothing got lost. Show a ✅ or 🚫 line only in the answer where the task got there, then leave it out: the user has seen it. When the user says to stop tracking something, leave it out too.

| Emoji | Status | When |
|---|---|---|
| ⏳ | Waiting | It needs an answer or a decision. Say from whom: "⏳ You: …". |
| 👀 | Ready for your check | Your part is done. The user reviews, merges, publishes or tries it. Link its pull request. |
| 🔄 | In progress | Started but not finished, or running in the background. |
| ⏩ | Up next | Agreed, not started. |
| ✅ | Done | Finished. One short line, shown once. |
| 🚫 | Dropped | Given up on purpose. Give the reason, shown once. |

Order the lines by status as in the table: what needs the user first, done last. Under them, give the answer, or what you did, in at most three lines: "In short" is what the user reads at a glance. Everything else goes under `## In detail`, in plain English, split in two: `### Needs your decision`, one point per decision the user has to make, with the context to make it (the options, what each leads to, which you recommend), and `### For your information`, what they only need to know: explanations, findings, reasons, tests and corrections. Leave out an empty part, and the whole section when there's nothing more to say.

End with these sections, each only when it has something in it:
- `## Bugs`: bugs you found outside the task, one plain sentence each, with the file and the fix.
- `## Branches`: from the session's first edit until it ends, every branch you worked on: what's on it, and whether it's committed, pushed and merged, with the pull request's link. Start each line with its state: 🟡 pull request open, 🟢 merged, or ⚪ for a branch someone else made that has no pull request (say so). A branch with no change since your last report gets one line.
- `## Commands for you`: each command in the order to run it, saying where: the terminal and folder (for example "Your Mac, in `~/Projects/FollowThroughHQ2`"), or the website page and button (for example GitHub's Settings > Pages). Don't hand the user a command that only looks at something: run it yourself.
- `## Want me to?`: connected work that isn't part of the session's goal, one question per line. Ask each one once.

**Make questions quick to answer.** Each ⏳ line makes the user switch into this session. Where you can, ask a yes/no question, or give lettered options with the one you recommend first ("A (recommended): …, B: …"), so that one word answers it. If the choice is easy to undo and has a sensible default, take the default, say which one you took and why, and don't wait. This never covers steps that are hard to undo or that publish something, such as pushing to `main`.
