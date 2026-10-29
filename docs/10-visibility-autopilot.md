# Visibility Autopilot: the plans and what's left to launch

The paid service on `/visibility`: directory listings, Google Business Profile care and website fixes for local service businesses, on one monthly bill. Its rules for customers are on `/service-terms`. Why it exists and how it's pitched are in `09-value-propositions.md`; where it sits among the offers is in `01-business-plan.md`.

## The plans

| Plan | Price | What's included |
|---|---|---|
| Starter | $99/month | A monthly website check with the fixes ranked, a listing check across 40+ directories, a monthly report. The owner makes the fixes. |
| Growth | $199/month | Starter, plus listings submitted and managed, and the Google profile looked after: weekly posts, review replies, photo updates, new-review alerts. |
| Done-for-you | $299/month | Growth, plus the website fixes made for them and a monthly strategy call. |

Every plan starts with 30 days free (once per business): the card is taken at signup and first charged on day 31, and cancelling before then costs nothing. After that it's month to month: no setup fee, no contract, free cancellation by email. The month already paid for runs to its end and isn't refunded. Prices and the free month set on 2026-10-28.

## How each plan works

Step by step, in `01-business-plan.md` (onboarding, then Starter, Growth and Done-for-you). Everything runs by hand with free tools and three Google Sheets: the website check, the listing check and the monthly report.

## To do before selling

Until Stripe is set up, nobody can pay on the site: the plan buttons on `/visibility` and the badge order form on `/badge` send you an email with the visitor's details and question, and you reply by hand (since 2026-10-29).

1. **Decide whose name the Stripe account is in.** Waiting for Emil (asked 2026-10-29): can the account be opened under Lexis? If yes, open it as Lexis. If not, register your own company first and open it under that. Either way, Stripe asks for the company's details, its bank account and a check of who runs it, and the company decides who invoices the customers, so tell the accountant (step 6) which one it is.
2. Write the list of 40+ directories for local US service businesses, and check each is still running and free to list on. The site promises 40+, so the list has to hold at least that many.
3. Make the three Google Sheets: the website check, the listing check and the monthly report template.
4. Set up Stripe, in the name chosen in step 1: the account, the $99, $199 and $299 monthly payment links, each with a 30-day free trial (`12-payments.md`). Stripe is already named on the Privacy page and the service terms. Products and links are made in the sandbox (Stripe's practice area). A check on 2026-10-28 found the prices right ($99, $199, $299 a month, in USD) and these fixes still to do, all at dashboard.stripe.com with the sandbox switched on (top left):
   1. **Fix the typo:** **Product catalog** → "Visibility Autopliot Done-for-you" → the **pencil** next to the name → change it to "Autopilot" → **Save**.
   2. **Archive the $0 prices:** **Product catalog** → open each plan → under **Pricing**, click **⋯** next to the $0.00 price → **Archive price**. The links don't use them, and Stripe doesn't make free months that way.
   3. **Add the free trial and the business name:** **Payment links** → click a plan's link → **Edit**. Under **Options**, tick **Include a free trial** and type 30. Click **Add custom field**, choose **Text** and name it "Business name". Click **Update link**. Do this for all three plans: none has the trial yet, though the website promises it.
   4. **Badge in dollars:** it's priced at €25, but the website says $25. **Product catalog** → "Verified Business badge" → **Add another price** → $25.00, **USD**, **One-off** → **Add price**. Then **Payment links** → **New**, choose the badge at the dollar price, add the "Business name" field and create the link. On the old euro link, click **⋯** → **Deactivate**.
   5. **Sales tax:** "Collect tax automatically" is on for all four links. It costs about 0.5% per payment and needs your tax registrations set up in Stripe. Decide whether to keep it (recommended: turn it off until the accountant in step 6 says otherwise). To turn it off: on each link, **Edit** → untick **Collect tax automatically** → **Update link**.
   6. **Emails:** **Settings** → **Billing** → **Subscriptions and emails**: switch on the email that reminds customers before their free trial ends. Then **Settings** → **Customer emails**: switch on **Successful payments** and **Failed payments**. (Not checked: the read-only key can't see these.)
   7. **Real account:** when the sandbox is right, switch off the sandbox (top left). Finish **Activate payments** if Stripe still asks for it, then make the same products and links there. Make a read-only key in the real account and ask Claude to check it again.
   8. **Delete the key:** **Developers** → **API keys** → **⋯** next to "Claude check" → **Delete**.
5. Check whether Google still lets businesses answer questions (Q&A) on their profile. It was left off the page because Google seemed to be switching it off in late 2025.
6. Have a lawyer read the service terms and the Privacy page's Visibility Autopilot section (see `04-legal-checklist.md`), and ask an accountant how to invoice US customers and whether VAT applies.
7. Upload the customer list to Google Sheets: the "Autopilot customers" tab of `sheets/orders-and-customers.xlsx` (how: `12-payments.md` and the sheet's "Start here" tab).
8. Ask Emil to put the changes live.

## To do once customers come

1. Time each plan for a month, so you know $99, $199 and $299 cover your hours, including the free first month.
2. Decide how to submit listings for Growth: by hand, or a paid listing service charged per customer.
3. Use real results in the page and outreach (with the customer's permission). Never invent them: US rules (the FTC) ban fake testimonials.
4. Decide whether a self-serve Starter tool is worth building.
