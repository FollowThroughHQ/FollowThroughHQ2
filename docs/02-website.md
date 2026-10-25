# Website architecture

## Overview
The site is one page, `resources/views/home.blade.php`, served by a small Laravel app at `/` (see `08-signup-server.md` to run it). There is no build step. The view uses no Blade syntax, so never put `{{` or `@word` in it. Pages are rendered by JavaScript from data arrays and switched with URL hash routes.

## Routes
| URL hash | Page |
|---|---|
| `#home` | Home: hero, sample objection handler, trades by category, signup |
| `#guides` | Start-up guides index by category |
| `#roofing`, `#hvac`, `#plumbing`, `#painting`, `#handyman`, `#landscaping`, `#junk-removal`, `#hauling-transportation` (old `#moving-transportation` links redirect), `#house-cleaning`, `#car-detailing` | One guide per trade |
| `#sales` | Sales hub |
| `#about` | About page |
| `#privacy`, `#terms`, `#disclaimer`, `#affiliate` | Legal pages (`#affiliate` is the affiliate disclosure) |

## Data in `home.blade.php`
- `CATS`: the three categories (Trades & repair, Outdoor & hauling, Cleaning & detailing).
- `STEPS`: the seven shared steps (LLC, EIN, bank account, insurance, pricing, first customers, objections). Edit the text once to change it on every guide.
- `T`: one entry per trade: `s` (slug), `n` (name), `c` (category index), `cost`, `season`, `fit`, `spend`, and `tips` (seven strings, one per step).
- `FULL`: the deep-dive content per slug: `lic`, `cost` (table rows), `costnote`, `plan`, `price`, `mistakes`, `obj`, `faq`, `tools`.
- `OBJ`: the three sample objections on the home page.
- `LEGAL`: legal pages plus the About and Sales hub pages (they share a renderer).
- `CONTACT` and `PUBLIC`: contact email and the public URL of the site.

## How to add a new trade
1. Add an entry to `T` with a unique slug, a category index and seven tips.
2. Add an entry to `FULL` under the same slug (copy the roofing entry and rewrite it).
3. Reload. The tile, guide page and related-guide links appear automatically.

## Features
- **Checkmarks:** each step has a completion button. Progress is saved in the visitor's browser (`localStorage`, key `ft:<slug>`). It never leaves their device.
- **Related guides:** open guides in the same category in a new tab, using `PUBLIC` as the base address.
- **Signup form:** posts the visitor's email to `/api/playbook` (`routes/api.php`), which emails the request to you (setup in `08-signup-server.md`). `FORM_URL` holds that path. See `06-google-sheets-forms.md` to also save signups to a Google Sheet.
- **Dark mode:** colors are CSS variables and follow the visitor's system setting.

## Known limitations
- Content for non-roofing guides is shorter than roofing (4 objections vs 8, 2 FAQs vs 5).
- No state-by-state licensing data yet.
- Signups are not stored until the Sheets integration is added.
- A single large file is easy to start with but harder to maintain. Consider splitting data into JSON files later.

## Placeholders to replace
All filled on 2026-10-25 (name, address, country and governing law were left out on purpose). The test-site check fails if any of these come back: `[Your Name]`, `[Your Name / Company]`, `[address]`, `[country]`, `[country/state]`, `[date]`, `[X years]`, `[industries / roles]`, `[One sentence on a result or lesson you’re proud of.]`, `Add a photo and a short personal line here.`, and `hello@yourdomain.com`.
