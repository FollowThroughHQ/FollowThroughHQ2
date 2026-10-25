---
name: test-site
description: Tests the FollowThrough website end to end. Opens the site in headless Chrome, clicks every link on every page (home, guides, each trade, sales, about, legal) and checks it lands on a real page without JavaScript errors, then fetches every external link, mailto and resource. Runs against / and /v2 locally, or any URL such as the live site. Use when the user wants to test the site, check for broken links, check it before publishing or after an edit, or says /test-site.
argument-hint: [base URL, default http://127.0.0.1:8000] [paths, default / /v2]
---

# Test the site

Target: **$ARGUMENTS**. If empty, test the local app at `http://127.0.0.1:8000`, paths `/` and `/v2`.

## Step 1: Make sure the site is up

For a local target, run `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/`. If it isn't 200, start the app with `php artisan serve` in the background (if `php` isn't on PATH, use `~/.config/herd-lite/bin/php artisan serve`) and stop it again when you're done. The app serves whatever branch is checked out, so say which branch you tested.

## Step 2: Run the check

```bash
python3 .claude/skills/test-site/check.py [base-url] [path ...]
```

It needs only the Mac's built-in Python and Google Chrome, nothing to install. It takes about 15 seconds. What it does:

1. Fetches each path from the server and fails if it isn't status 200.
2. Opens the page in headless Chrome with two helper scripts added (in a temporary copy, never the real file): one that records JavaScript errors, one that walks the site.
3. Starting at `#home`, it visits every page it can reach. On each page it clicks every link, one at a time, the way a visitor would. A `#` link passes if it lands on a real page (a trade in `T`, a page in `LEGAL`, `#guides`, `#home`, `#home-contact`) with the right title, real content and no JavaScript error. Any other `#` link fails, because the site's router quietly shows the home page for names it doesn't know, so a visitor sees the page jump instead of an error.
4. Fetches every link that leaves the page (external sites, other server paths) and every stylesheet, script and image, and fails on errors or status 400 and up.
5. Checks mailto addresses are well formed, and warns while they're still the `hello@yourdomain.com` placeholder.

It exits 0 when nothing is broken, 1 otherwise. `FAIL` lines are broken links. `WARN` lines work but need attention before publishing.

## Step 3: Report

Explain each FAIL in plain English: which link (its text), on which page, what a visitor sees when they click it, and the likely fix with the file and function (links are built in `resources/views/home.blade.php`; routing is `go()` and `render()`). Group duplicates: a broken header or footer link shows on every page but is one bug. List the WARNs separately. Don't fix anything unless the user asks.

## Limits

- It clicks links, not buttons. The step checkmarks, objection tabs and signup form aren't tested.
- An external link that returns a 200 login or "not found" page counts as working.
- It tests one window size and the default color scheme.
