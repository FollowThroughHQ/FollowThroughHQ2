# Running the app and the signup emails

The site is a small Laravel app. It serves the page, and it has two other jobs: the "Send me the playbook" form posts to `/api/playbook`, and the badge order form to `/api/badge`. No login, no database.

When someone asks for a playbook, the app sends two emails at once: the visitor gets an email with their trade's PDF from `public/playbooks/` attached and a link to the guide, and you get a short note saying who asked for which trade. On a guide page the trade is that guide's; on the home page and the calculator the visitor picks it from a list. If the visitor replies, the reply comes to you (`MAIL_TO`, or `MAIL_FROM_ADDRESS` if that's empty).

To stop anyone using the form to flood someone else's inbox, each email address gets at most one playbook a day, and each visitor can send 5 requests a minute. A second request the same day only sends you the note, which says so; reply to it if you want to send the second playbook by hand. The visitor's email says how to unsubscribe (reply "unsubscribe"), so remove those people from any list you keep.

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

1. In Brevo, authenticate the domain you send from (Senders, Domains & Dedicated IPs > Domains > Add a domain). Add the DNS records Brevo shows at your DNS provider, then click Authenticate in Brevo. The domain must be registered: Brevo silently drops mail from a domain that doesn't exist.
2. In Brevo, open Settings > SMTP & API > SMTP. Copy the SMTP login and generate an SMTP key.
3. In `.env`:

```ini
MAIL_MAILER=smtp
MAIL_USERNAME=your-brevo-smtp-login
MAIL_PASSWORD=your-brevo-smtp-key
MAIL_FROM_ADDRESS="peter@yourpathguide.com"   # any address on the domain from step 1
MAIL_TO=                                       # optional: another inbox for signups
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
