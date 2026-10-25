# Running the app and the signup emails

The site is a small Laravel app. It serves the page, and it has one other job: the "Send me the playbook" form posts to `/api/playbook`, and the app emails the request to you. You reply to that email with the playbook. No login, no database.

It only ever emails you (`MAIL_TO`), never the address a visitor types, so nobody can use it to spam other people. Each visitor can send 5 requests a minute.

## Try it on your Mac

The first time only:

```bash
composer install
cp .env.example .env
php artisan key:generate
```

Then:

```bash
php artisan serve
```

Open `http://127.0.0.1:8000` and submit the form. While `MAIL_MAILER=log`, the email is written to `storage/logs/laravel.log` instead of being sent.

## Send real emails

Sign up with an SMTP provider, verify the sender address it asks for, then fill in `.env`:

```ini
MAIL_MAILER=smtp
MAIL_HOST=smtp-relay.brevo.com
MAIL_PORT=587
MAIL_USERNAME=your-smtp-login
MAIL_PASSWORD=your-smtp-key
MAIL_FROM_ADDRESS="hello@yourdomain.com"   # must be a sender your provider has verified
MAIL_TO="you@yourdomain.com"               # your inbox
```

| Provider | MAIL_HOST | MAIL_PORT | MAIL_USERNAME / MAIL_PASSWORD |
|---|---|---|---|
| Brevo | `smtp-relay.brevo.com` | 587 | SMTP login and SMTP key (Settings > SMTP & API) |
| Mailjet | `in-v3.mailjet.com` | 587 | API key and secret key |
| SMTP2GO | `mail.smtp2go.com` | 2525 | An SMTP user you create in the dashboard, and its password |

## Put it online

Any host that runs PHP 8.3+ works. Point the web root at `public/`. Set the same variables in the host's settings (never commit `.env`), plus:

```ini
APP_ENV=production
APP_DEBUG=false
APP_KEY=   # run `php artisan key:generate --show` and paste the result
```

The page and the form are served from the same address, so nothing else needs to change.

### The live site: https://ft.emil-kirilov.eu

It runs on the home TrueNAS, in the `heimdall` jail (nginx and PHP 8.3.1, which can't be updated there). To put changes live, merge them into `main` on GitHub, then run `./deploy.sh` on the Mac. It deploys GitHub's `main`, whatever branch you're on, and never local edits. To try a branch on the live site first: `./deploy.sh origin/<branch>`.

- `composer.json` pins PHP 8.3.1 (`config.platform.php`), so `composer update` only picks packages that run on the server. Keep it until the server's PHP changes.
- The server's own settings are in `/usr/local/www/followthrough/.env` inside the jail (on the NAS: `/mnt/raid/iocage/jails/heimdall/root/usr/local/www/followthrough/.env`). The deploy never touches it or `storage/`. After editing it, nothing needs restarting.
- Logs: `storage/logs/laravel-<date>.log` in the same folder, kept 14 days.
- Server side (nginx, the Caddy proxy, DNS): `NETWORK.md` in the truenas-home notes.

## Test

```bash
php artisan test
```
