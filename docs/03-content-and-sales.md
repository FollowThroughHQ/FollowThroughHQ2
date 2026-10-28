# Content and sales

## Trades and categories
- **Trades & repair:** HVAC, Plumbing, Roofing, Painting, Handyman, Electrical Services, Appliance Repair, Drywall Installation & Repair
- **Outdoor & hauling:** Landscaping, Junk Removal, Hauling & Transportation, Lawn Care
- **Cleaning & detailing:** House Cleaning, Car Detailing, Pressure Washing

## Guide structure (every trade)
1. Facts: start-up cost, busy season, is it a good fit, where the money goes.
2. Seven steps, each with a "what to look for" tip and a completion checkmark: form the LLC, get an EIN, open a business bank account, get insurance, set prices, find first customers, handle objections.
3. Deep dive: licensing and rules, itemized costs, first 90 days, pricing example, mistakes to avoid, objection library, FAQ, tools.
4. Email signup for the free playbook.
5. Related guides (same category, open in a new tab).

Roofing is the model guide (fullest). Other trades are shorter and can be expanded to match.

## Playbooks (the free download)
Every trade has a two-page playbook, the one the signup form promises: what to say from the first call to the review. Each follows `playbooks/_template.md`, in this order:
1. The first call or message: questions that size up the job, two lines to say.
2. Presenting the quote: what to show and itemize for this trade.
3. The 7 objections and what to say: seven of the eight in the guide's objection library, word for word, so the playbook and the website agree.
4. Follow up on day 2, day 5 and day 12, as texts.
5. Asking for the review and the referral.
6. Three rules that keep you out of trouble, from the guide's mistakes and licensing notes.

The text lives in `playbooks/<slug>.md`. After any change, run `php artisan playbooks` (or `php artisan playbooks roofing` for one) to remake the PDFs in `public/playbooks/`; it uses Google Chrome on the Mac. Check that each still fits on two pages. Once live, each PDF is at `followthroughguides.com/playbooks/<slug>.pdf`. They make the same claims as the guides, so they need the same checks before promoting.

## Sales hub topics
1. Answering the first call or message
2. Presenting a quote
3. Following up on quotes (day 2, day 5, day 12)
4. Closing
5. Handling objections (method below)
6. Asking for reviews and referrals
7. Handling a "no"

## Objection method
Acknowledge it, ask a question, answer honestly, suggest a next step.

## Style rules for content
- Honest and low-pressure. No guarantees of income.
- Never advise waiving insurance deductibles (illegal in many states).
- Say that rules vary by state and tell people to check their state board.
- Put costs in ranges and label them estimates.

## Verify before promoting
Start-up costs, seasons, licensing notes and pricing examples are estimates from general knowledge. Check them against current sources and local quotes.
