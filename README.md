# FollowThrough

A website and small business that helps new US service businesses (HVAC, roofing, plumbing and more) start up and win more jobs, with step-by-step start-up guides, sales scripts and objection handlers.

**Status:** early validation. See `docs/01-business-plan.md`.

## What's in this repo

A small Laravel app. It serves one page and emails signup-form requests to you. No database.

| Path | What it is |
|---|---|
| `resources/views/home.blade.php` | The entire website (one page: HTML, CSS and JavaScript) |
| `routes/web.php` | Serves the page at `/`, and at `/v2` a comparison copy with every guide deepened by the niche-guide skill (`home-v2.blade.php`) |
| `routes/api.php` | `/api/playbook`: the signup form posts here and the request is emailed to you |
| `docs/01-business-plan.md` | The idea, offer ladder, validation plan, Europe-to-US logistics, outreach rules |
| `docs/02-website.md` | How the site is built and how to edit it |
| `docs/03-content-and-sales.md` | Guide structure, trade list, sales hub, objection method |
| `docs/04-legal-checklist.md` | Legal pages, placeholders to fill, compliance notes |
| `docs/05-github-and-hosting.md` | Creating the repo and custom domain (its GitHub Pages hosting is outdated) |
| `docs/06-google-sheets-forms.md` | Saving email signups to Google Sheets |
| `docs/07-roadmap.md` | What to build next, in order |
| `docs/08-signup-server.md` | Running the app, sending real emails, putting it online |

Everything else (`app/`, `config/`, `public/`...) is standard Laravel.

## Quick start

1. Run the site locally (see `docs/08-signup-server.md`): `php artisan serve`, then open `http://127.0.0.1:8000`.
2. Replace the placeholders (search `resources/views/home.blade.php` for `[Your Name]`, `[address]`, `[country]`, `[date]`, `[X years]`, `hello@yourdomain.com`).
3. Host it on any PHP host (see `docs/08-signup-server.md`).
4. To also save signups in a Google Sheet, see `docs/06-google-sheets-forms.md`.

## Important

- The live site is https://ft.emil-kirilov.eu, on the home server. Merge into `main`, then run `./deploy.sh` to update it (see `docs/08-signup-server.md`).
- Content is general education, not legal, tax or financial advice. Costs and rules are estimates. Verify before publishing.
