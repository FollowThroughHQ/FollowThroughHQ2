---
name: test-site
description: Tests the FollowThrough website end to end. Opens the site in headless Chrome at phone width, clicks every link on every page (home, guides, each trade, sales, about, legal) and checks it lands on a real page without JavaScript errors; tests the signup form, step checkmarks and objection tabs; flags placeholder text, layout that runs off a phone screen, hard-to-read text in light and dark mode, and missing titles, headings, descriptions or alt text; fetches every external link, mailto and resource; takes phone screenshots. Runs against / locally, or any URL such as the live site, which it also compares with this computer's copy. Use when the user wants to test the site, check for broken links, check it before publishing or after an edit, or says /test-site.
argument-hint: [base URL, default http://127.0.0.1:8000] [paths, default /]
---

# Test the site

Target: **$ARGUMENTS**. If empty, test the local app at `http://127.0.0.1:8000`, path `/`.

## Step 1: Make sure the site is up

For a local target, run `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/`. If it isn't 200, start the app with `php artisan serve` in the background (if `php` isn't on PATH, use `~/.config/herd-lite/bin/php artisan serve`) and stop it again when you're done. The app serves whatever branch is checked out, so say which branch you tested.

## Step 2: Run the check

```bash
python3 .claude/skills/test-site/check.py [base-url] [path ...]
```

It needs only the Mac's built-in Python, `sips` and Google Chrome, nothing to install. It takes about 15 seconds. Add `--compare` to compare a local server with `resources/views/home.blade.php` (a site that isn't on this computer is always compared). What it does:

1. Fetches each path from the server and fails if it isn't status 200.
2. Opens the page in headless Chrome inside a 375px-wide frame, the width of a phone (Chrome's own window can't be narrower than 500px). It works on a temporary copy with two helper scripts added, never the real file: one records JavaScript errors, one walks the site.
3. Starting at `/`, it visits every page it can reach. On each page it clicks every link, one at a time, the way a visitor would. A `/` link passes if it lands on a real page (a trade in `T`, a page in `LEGAL`, `/guides`, `/calculator`, `/`) with the right title, real content and no JavaScript error; `/#signup` and `/#demo` must also scroll to the signup form and the sample objection. Any other `/` link fails, because the site's script quietly shows the home page for names it doesn't know. A link that opens a new tab only has to name a real page. A link to an old `#` address fails. Every page a link reaches is also fetched from the server, so it opens when its address is typed in or shared, not only when clicked.
4. On each page: fails if anything runs off the side of the phone screen, or if placeholder text from `docs/02-website.md` (`[Your Name]`, `[address]`, `[date]`, `hello@yourdomain.com`...) is still there, hidden FAQ answers included. Warns on text with too little contrast to read easily (WCAG AA: 4.5, or 3 for large text), in light and in dark mode; on a page without exactly one main heading (`h1`); on pages sharing a title; on images without alt text; and once if the site has no `<meta name="description">`.
5. Clicks each objection tab on the home page and checks it is selected and shows its objection. Ticks step 1 on the first guide, reloads the page, checks it's still ticked, then unticks it.
6. Signup form: checks the browser refuses to send it with the consent box unticked or a bad email, and that the server answers 422 to both. For a local target it then sends a real test signup to a private copy of the app it starts itself (`php -S` on a free port, with `MAIL_MAILER=log`), so no email goes out; it checks the visitor sees the thank-you message and that the email was written to that copy's log. On any other site it never sends a signup.
7. Fetches every link that leaves the page (external sites, other server paths) and every stylesheet, script and image, and fails on errors or status 400 and up. Checks mailto addresses are well formed.
8. Saves a full-length phone-width screenshot of every page in `storage/app/site-check/` (not part of the project's saved files), replacing the last run's.
9. When comparing, names the parts where the site differs from this computer's copy of the page: a setting such as `CONTACT`, a function, a guide (`FULL.roofing`), the guide list `T`, or the styles. A difference is expected while changes haven't been put live yet.

It exits 0 when nothing is broken, 1 otherwise. `FAIL` lines are broken. `WARN` lines work but need attention before publishing.

## Step 3: Report

Explain each FAIL in plain English: what (the link's text, the tab, the form), on which page, what a visitor sees, and the likely fix with the file and function (links are built in `resources/views/home.blade.php`; routing is `go()` and `render()`). Group duplicates: a broken header or footer link shows on every page but is one bug. List the WARNs separately. Tell the user where the screenshots are and offer to open one. Don't fix anything unless the user asks.

## Limits

- An external link that returns a 200 login or "not found" page counts as working.
- Layout is checked at phone width only. Dark mode is switched on with `data-theme="dark"`; the matching `prefers-color-scheme` rule in the CSS isn't checked separately.
- Contrast is checked against solid background colours; text over images or gradients isn't judged.
- On a site other than this computer, the signup form is checked only for refusing bad input.
