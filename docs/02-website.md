# Website architecture

## Overview
The site is one page, `resources/views/home.blade.php`, served by a small Laravel app (see `08-signup-server.md` to run it). There is no build step. The view uses no Blade syntax, so never put `{{` or `@word` in it. Pages are rendered by JavaScript from data arrays. Each page has its own address, so search engines can list each guide separately; `routes/web.php` serves the same file at all of them.

## Routes
| Address | Page |
|---|---|
| `/` | Home: hero, sample objection handler, example stories, calculator teaser, Visibility Autopilot box, Verified badge box, trades by category, signup (`/#signup`, `/#demo` jump to those sections) |
| `/guides` | Start-up guides index by category |
| `/roofing`, `/hvac`, `/plumbing`, `/painting`, `/handyman`, `/electrical`, `/appliance-repair`, `/drywall`, `/landscaping`, `/junk-removal`, `/hauling-transportation` (old `/moving-transportation` links redirect), `/lawn-care`, `/house-cleaning`, `/car-detailing`, `/pressure-washing` | One guide per trade |
| `/sales` | Sales hub |
| `/calculator` | Lost quotes calculator |
| `/visibility` | Visibility Autopilot: the paid listings, Google profile and website service. Linked from the footer, a box on the home page, a box near the top of every guide and step 6 of every guide. How each plan works: `01-business-plan.md`; launch to-do list: `10-visibility-autopilot.md` |
| `/badge` | Verified Business badge: a one-time $25 badge for a business's website, with an order form that emails you (`/api/badge` in `routes/api.php`). Linked from the footer, a box on the home page, the Visibility Autopilot page, a box near the top of every guide and step 6 of every guide. How it runs: `11-verified-badge.md` |
| `/verified` | The directory of businesses that passed the badge check, from `VB`. Each badge links to its business here (`/verified#acme-roofing`) |
| `/service-terms` | Service terms for paid Visibility Autopilot plans and the Verified Business badge |
| `/about` | About page |
| `/privacy`, `/terms`, `/service-terms`, `/disclaimer`, `/affiliate` | Legal pages (`/affiliate` is the affiliate disclosure) |
| `/sitemap.xml` | The list of pages for search engines |

Old `#` links (`/#roofing`, `/#home-contact`) still open the right page, so links shared before the change keep working. Trade addresses come from `T` automatically. A new page that isn't a trade needs its name added to the list in `routes/web.php`; `php artisan test` fails if a page the site links to has no address.

## Data in `home.blade.php`
- `CATS`: the three categories (Trades & repair, Outdoor & hauling, Cleaning & detailing).
- `STEPS`: the seven shared steps (LLC, EIN, bank account, insurance, pricing, first customers, objections). Edit the text once to change it on every guide.
- `T`: one entry per trade: `s` (slug), `n` (name), `c` (category index), `cost`, `season`, `fit`, `spend`, and `tips` (seven strings, one per step).
- `FULL`: the deep-dive content per slug: `lic`, `cost` (table rows), `costnote`, `plan`, `price`, `mistakes`, `obj`, `faq`, `tools`.
- `OBJ`: the three sample objections on the home page.
- `EX`: the three example stories on the home page (made up, and labeled so). Swap in real ones, with the owner's permission, as they come in.
- `LEGAL`: legal pages plus the About and Sales hub pages (they share a renderer).
- `VB`: the businesses in the `/verified` directory, one per passed badge check (how to add one: `11-verified-badge.md`).
- `CONTACT`: contact email.

## How to add a new trade
1. Add an entry to `T` with a unique slug, a category index and seven tips.
2. Add an entry to `FULL` under the same slug (copy the roofing entry and rewrite it).
3. Write its playbook: copy `playbooks/_template.md` to `playbooks/<slug>.md`, fill it in, and run `php artisan playbooks <slug>` to make the PDF (`03-content-and-sales.md`).
4. Reload. The tile, guide page and related-guide links appear automatically.

## Features
- **Checkmarks:** each step has a completion button. Progress is saved in the visitor's browser (`localStorage`, key `ft:<slug>`). It never leaves their device.
- **Related guides:** open guides in the same category in a new tab.
- **Lost quotes calculator:** at `/calculator` (`calc()` and `wireCalc()`). The visitor enters quotes a month, jobs won out of 10 and average job price, and sees what winning 1, 2 or 3 more in 10 adds per month and year.
- **Signup form:** posts the visitor's email and trade to `/api/playbook` (`routes/api.php`), which emails the visitor their trade's playbook PDF and you a note (setup in `08-signup-server.md`). `signup(t)` and `wireSignup(t)` build and send it: on a guide page `t` is that trade; without `t` (home page, calculator) the form shows a trade list built from `CATS` and `T`. `FORM_URL` holds that path. See `06-google-sheets-forms.md` to also save signups to a Google Sheet.
- **Dark mode:** colors are CSS variables and follow the visitor's system setting.

## Known limitations
- Content for non-roofing guides is shorter than roofing (4 objections vs 8, 2 FAQs vs 5).
- No state-by-state licensing data yet.
- Signups are not stored until the Sheets integration is added.
- A single large file is easy to start with but harder to maintain. Consider splitting data into JSON files later.

## Placeholders to replace
All filled on 2026-10-25 (name, address, country and governing law were left out on purpose). The test-site check fails if any of these come back: `[Your Name]`, `[Your Name / Company]`, `[address]`, `[country]`, `[country/state]`, `[date]`, `[X years]`, `[industries / roles]`, `[One sentence on a result or lesson you’re proud of.]`, `Add a photo and a short personal line here.`, and `hello@yourdomain.com`.
