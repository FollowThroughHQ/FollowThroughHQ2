# Running the app and the signup emails

The site is a small Laravel app. It serves the page, and it has one other job: the "Send me the playbook" form posts to `/api/playbook`, and the app emails the request to you. You reply to that email with the playbook. No login, no database.

It only ever emails you (at `MAIL_FROM_ADDRESS`, or `MAIL_TO` if you set it), never the address a visitor types, so nobody can use it to spam other people. Each visitor can send 5 requests a minute.

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

Emails go out through Brevo (free: 300 a day). Brevo's server and port are already set in `.env`. Fill in the rest:

1. In Brevo, add and verify the address you send from (Senders, Domains & Dedicated IPs > Senders).
2. In Brevo, open Settings > SMTP & API > SMTP. Copy the SMTP login and generate an SMTP key.
3. In `.env`:

```ini
MAIL_MAILER=smtp
MAIL_USERNAME=your-brevo-smtp-login
MAIL_PASSWORD=your-brevo-smtp-key
MAIL_FROM_ADDRESS="peter@followthroughguides.com"   # the sender you verified in step 1
MAIL_TO=                                             # optional: another inbox for signups
```

Restart `php artisan serve` after changing `.env`.

## Put it online

Any host that runs PHP 8.3+ works. Point the web root at `public/`. Set the same variables in the host's settings (never commit `.env`), plus:

```ini
APP_ENV=production
APP_DEBUG=false
APP_KEY=   # run `php artisan key:generate --show` and paste the result
```

The page and the form are served from the same address, so nothing else needs to change.

## Test

```bash
php artisan test
```
