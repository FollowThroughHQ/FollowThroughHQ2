# Taking payments with Stripe

How customers pay for the Verified Business badge and Visibility Autopilot, and how to set it up. Chosen on 2026-10-28.

## Why Stripe

- It works from Europe and charges US customers in dollars by card, Apple Pay and Google Pay.
- It handles both kinds of payment we need: a one-time $25 for the badge and monthly plans that renew by themselves.
- Payment links need no change to the website: you paste a link into an email and the customer pays on Stripe's page.
- Lemon Squeezy and other merchant-of-record platforms were ruled out: Lemon Squeezy's rules ban selling services of any kind (marketing, consulting and similar), and both of our offers are services. PayPal works too, but its monthly billing is clumsier.

Fees: Stripe takes a few percent of each payment, more for US cards on a European account and when dollars are converted to your currency. Monthly plans add about 0.7%. Stripe's pricing page shows the exact numbers for your country.

## How customers pay

| Offer | How | When |
|---|---|---|
| Verified Business badge, $25 once | Badge payment link | In the "Passed" email, after the check (`11-verified-badge.md`) |
| Starter, $99/month | Starter payment link | In the reply to their email asking for the plan (`01-business-plan.md`, "How every plan starts") |
| Growth, $199/month | Growth payment link | Same |
| Done-for-you, $299/month | Done-for-you payment link | Same |

Each plan link starts with a 30-day free trial: the customer adds their card, nothing is charged for 30 days, and Stripe charges the first month on day 31 unless they cancel first. Stripe emails them a reminder before the trial ends (step 5 below).

The site never shows the links: they go out by email, after the check or the first conversation.

## The links

Paste them here once they're made, so they're easy to find.

- Badge ($25 once):
- Starter ($99/month, 30 days free):
- Growth ($199/month, 30 days free):
- Done-for-you ($299/month, 30 days free):

## Setting it up (once)

1. Go to stripe.com and click **Start now**. Sign up with your email and choose your country. Confirm your email.
2. In the Stripe dashboard, click **Activate payments** (or **Complete your profile**). Choose **Individual / sole proprietor** unless you've registered a company, fill in your details, add the bank account for payouts and confirm your identity. Where it asks for the name customers see on their card statement, use **FOLLOWTHROUGH**.
3. Make the badge link: **Product catalog** → **Add product**. Name: "Verified Business badge". Price: $25.00 USD, **One-off**. Save. Then **Payment links** → **New**, choose the badge, and under **Options** click **Add custom field**: a text field called "Business name", so you can tell who paid. Create the link and copy it.
4. Make the plan links: **Add product** "Visibility Autopilot Starter", $99.00 USD, **Recurring**, **Monthly**. Make a payment link for it the same way, with the "Business name" field, and under **Options** tick **Include a free trial** and enter 30 days. Repeat for "Visibility Autopilot Growth" at $199.00 and "Visibility Autopilot Done-for-you" at $299.00.
5. Turn on emails: **Settings** → **Customer emails**, and switch on **Successful payments** (receipts) and **Failed payments**. Under **Settings** → **Subscriptions and emails** (**Manage failed payments**), turn on retries and the email that asks the customer to update a failed card. On the same page, switch on the email that reminds customers their free trial is ending (US rules expect a reminder before a free trial turns into a paid plan).
6. Send the four links to Claude to add above.
7. Test it: pay the badge link with your own card, check the receipt email, then refund it under **Payments** → the payment → **Refund**.

## The order and customer sheet

`sheets/orders-and-customers.xlsx` is a blank sheet with four tabs: "Start here" (how to fill it in), "Badge orders", "Autopilot customers" and "Summary" (counts and income, worked out by itself). To use it in Google Sheets:

1. Go to drive.google.com, signed in with the account you use for the business.
2. Click **New** → **File upload** and choose `orders-and-customers.xlsx` from the project's `docs/sheets` folder.
3. Right-click the uploaded file → **Open with** → **Google Sheets**, then **File** → **Save as Google Sheets**. Use that copy from now on and delete the uploaded `.xlsx`.

Real customer details stay in Google Sheets and never go into the project. If you want new columns, ask Claude to change the blank copy too.

## Day to day

- **A payment comes in:** Stripe emails you. Fill in the paid date, amount and payment number (it starts with `pi_` or `py_`, on the payment's page in Stripe) in the sheet (`sheets/orders-and-customers.xlsx`, uploaded to Google Sheets).
- **A customer cancels during the free month:** **Customers** → the customer → their subscription → **Cancel subscription** → **Immediately**. They're never charged.
- **A customer cancels by email:** **Customers** → the customer → their subscription → **Cancel subscription** → **At the end of the current period**. They keep the month they've paid for and aren't charged again, as the service terms promise. Fill in the dates in the sheet.
- **A payment fails:** Stripe retries and emails the customer. If it still fails, the service terms let you stop the service; email them first.

## Still to check

- Ask the accountant (step 5 in `10-visibility-autopilot.md`) whether you need to charge VAT or US sales tax, and how to record Stripe payouts. Stripe Tax can add tax automatically for about 0.5% per payment if it's needed.
- Have the lawyer read the Stripe wording on the Privacy page and the service terms with the rest (`04-legal-checklist.md`).
