# Verified Business badge: how it runs and what's left to launch

A one-time $49 badge for a business's website that tells visitors "this business is real, reachable and trustworthy". It's sold on `/badge`, and each badge links to the business's profile in the directory at `/verified`. The rules for customers are in the badge section of `/service-terms`, and the Privacy page has a matching section.

There's one level for now: **Verified Business**, meaning identity, registration, website address and contact details confirmed.

## Who it's for

New service businesses with no reviews, no name people know and no track record. A first-time visitor can't tell them from a fly-by-night outfit. The badge gives that visitor an independent reason to trust them, which can mean more contact form fills and sales. The directory profile also gives the business one more listing and a link to its website.

## How an order comes in

1. The customer fills in the form at the bottom of `/badge`: business name, website, Google profile link (optional) and email.
2. It arrives in your inbox with the subject "Badge order: [business name]". Hit Reply to answer the customer.
3. You check the business (below), usually within 2 business days, as the page promises.
4. **Passes:** reply with the payment link (template below). **Doesn't pass:** reply with what was missing. They pay nothing.
5. Once they've paid: add them to the directory, then email the badge (template below).

The customer pays only after passing, so there are no refunds to handle.

## The check

Every order gets all four checks (the owner decided this on 2026-10-27). The main check is the Google profile. The other three take a few minutes and are what lets the badge say "identity, registration, website address and contact details confirmed" (see "Why the check has four parts" below).

1. **Google Business Profile is verified.** Search the business name on Google Maps. A profile the owner hasn't verified shows "Own this business?" or "Claim this business". A verified one doesn't. If you're unsure, ask the owner for a screenshot of their Business Profile dashboard showing it as verified.
2. **Registered.** Search the business in its state's business register: search for "[state] business entity search", which is the Secretary of State's free lookup. A sole owner trading under their own name may not be registered there. Then look for a DBA ("doing business as") filing with the county, or a city business license.
3. **Website is theirs.** The website on the Google profile is the same as the one in the order, which is where the badge goes.
4. **Reachable.** The phone number and email on their website match the Google profile, and they answer your email.

Write down for each order: the date, the result of each check and where you looked. If a customer or visitor ever asks how a business was checked, you can show it.

## Adding a business to the directory

Ask Claude: "Add [business] to the verified directory: [trade], [city, state], [website], checked [date]." It goes in the `VB` list in `resources/views/home.blade.php`, for example:

```js
var VB=[{id:"acme-roofing",n:"Acme Roofing",trade:"Roofing",at:"Austin, TX",web:"https://acmeroofing.com",d:"November 3, 2026"}];
```

`id` is the end of the business's badge link: `https://followthroughguides.com/verified#acme-roofing`. Keep it short, lowercase, with dashes, and never change it once the badge is sent, or the badge stops leading to the profile. Then Emil puts the change live.

To take a business down (it closed, lost its Google verification or misuses the badge), remove its entry and email them to remove the badge.

## Email templates

**Passed, here's the payment link:**

> Hi [name], good news: [business] passed the Verified Business check. Your Google profile is verified, your registration is on record, and your website and contact details match. To get your badge, pay the one-time $49 here: [payment link]. Your badge and directory profile follow as soon as it's paid.

**Didn't pass:**

> Hi [name], thanks for ordering the Verified Business badge. [Business] didn't pass yet because [what was missing, e.g. your Google profile isn't verified]. You haven't been charged. Once that's fixed, reply to this email and I'll check again.

**Your badge** (replace `acme-roofing` with the business's `id`):

> Hi [name], here's your Verified Business badge. Paste the code below into your website where you'd like the badge to show, for example in the footer or next to your contact form. On Wix, Squarespace and WordPress, use an "Embed" or "Custom HTML" block. Or forward this email to whoever runs your website. Your profile is here: https://followthroughguides.com/verified#acme-roofing
>
> ```html
> <a href="https://followthroughguides.com/verified#acme-roofing"><img src="https://followthroughguides.com/badge.svg" alt="Verified Business, checked by FollowThrough" width="260" height="72"></a>
> ```

The badge image is `public/badge.svg`.

## Why the check has four parts

The original idea was "a verified Google page means verified". But the badge tells visitors that identity, registration, website and contact details were confirmed, and Google verification alone doesn't show registration or that the website is theirs. A seal that claims more than was checked can be deceptive under US rules (the FTC has acted against trust seals before). So every order gets all four checks. If they're ever cut back to Google only, the badge's wording on `/badge`, `/verified`, the service terms and this doc has to change to "Google-verified business profile" first.

## To do before selling

1. Choose a payment provider (the same one as Visibility Autopilot, step 3 in `10-visibility-autopilot.md`) and make a one-time $49 payment link to paste into the "Passed" email. Then add the provider's name to the Privacy page and the service terms.
2. Have a lawyer read the badge section of the service terms and the Privacy page (see `04-legal-checklist.md`).
3. Make a simple order sheet (a Google Sheet): business, date ordered, each check's result and where you looked, paid date, `id`, removed date.
4. Ask Emil to put the changes live.
