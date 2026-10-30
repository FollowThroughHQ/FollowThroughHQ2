# Customer journeys: from the click to the work

What happens to each customer from the moment they send a form or say yes, until the work is delivered and, for the monthly service, until they leave. Every email you send is here, ready to copy. Written on 2026-10-30.

Details that already live elsewhere aren't repeated, just linked: what each Autopilot plan includes (`01-business-plan.md`), the badge check (`11-verified-badge.md`), outreach and the free check (`14-first-clients.md`), payments (`12-payments.md`).

| Product | How it starts | What they pay | Journey |
|---|---|---|---|
| Free playbook | The form on a guide page, the home page or the calculator | Nothing | [1](#1-free-playbook) |
| Free 5-point check | They say yes to an outreach email | Nothing | [2](#2-free-5-point-check) |
| Verified Business badge | The form on `/badge` | $25 once, only after passing | [3](#3-verified-business-badge) |
| Visibility Autopilot | The form on `/visibility` | $99, $199 or $299 a month, first 30 days free | [4](#4-visibility-autopilot) |

**Where things are kept:** orders and customers in the Google copy of `sheets/orders-and-customers.xlsx`; one Google copy of `sheets/autopilot-customer.xlsx` per Autopilot customer; leads in the Google copy of `sheets/lead-tracker.xlsx`; listing logins in a password manager (Bitwarden is free), never in a sheet or an email.

**Payment links:** until Stripe is set up (`10-visibility-autopilot.md`, steps 1 and 4), the emails below that need a payment link can't be sent. Keep the customer warm and tell them payments open soon. Once the links exist they're listed in `12-payments.md`.

**Every email you send** ends with:

> [Your name]
> FollowThrough · followthroughguides.com

---

## 1. Free playbook

1. **The visitor sends the form.** The website emails them their trade's playbook straight away, and emails you a note "Free playbook: [trade]" (`08-signup-server.md`). Nothing to do for the playbook itself.
2. **The same day:** add them to the lead tracker. Source "Website signup", Status "Free thing sent", today's date in "Playbook sent".
3. **3 days later:** offer the free check (email below). It's the step from the free playbook towards something paid.
4. **If they reply "unsubscribe" at any time:** Status "Do not contact", and never email them again.

**The check offer, 3 days after the playbook.** Subject: your [trade] playbook

> Hi,
>
> Hope the playbook's useful. Part 4, the day 2, 5 and 12 follow-ups, is the part most people get the most out of.
>
> One more free thing, if it helps: I do a 5-point check of new [trade] businesses' Google profile and website. You get it by email within a day, with how to fix each thing. Just reply with your business name and website.
>
> To get no more emails, reply "unsubscribe".

If they say yes, it continues as journey 2.

## 2. Free 5-point check

How it's offered, done and sent is in `14-first-clients.md` ("When they say yes to the check"). It ends with one paid offer: the badge (journey 3) or Autopilot (journey 4).

For point 5 ("your details elsewhere"), look at the first rows of the Directories tab in `sheets/autopilot-customer.xlsx`: Google, Bing, Apple Maps, Yelp and BBB.

## 3. Verified Business badge

### At a glance

| When | What happens | Who |
|---|---|---|
| Day 0 | The customer sends the form on `/badge`. You get "Badge order: [business]" | Customer |
| Within 2 business days | You do the four checks and email the result | You |
| Didn't pass | They pay nothing. They can fix it and reply for a new check | You |
| Passed | The result email has the payment link | You |
| Days 3, 7, 14, then every 30 days | A reminder, until they pay or say no | You |
| They pay | Stripe emails you. Claude adds them to the directory, Emil puts it live | You, Claude, Emil |
| Once it's live | You email the badge | You |
| Once a year | A quick recheck of every business in the directory | You |

### Step by step

1. **The order arrives.** Add a row to "Badge orders": date, business, email, website, Google link. Result "Waiting".
2. **The check**, within 2 business days, as the badge page promises: the four checks in `11-verified-badge.md`. Fill in each check, where you looked, and the Result.
3. **Email the result** (templates in `11-verified-badge.md`: "Passed" with the payment link, or "Didn't pass"). Fill in "Result emailed".
4. **If they've passed but not paid:** send reminders on day 3, day 7 and day 14 after the result, then every 30 days, until they pay or say no. The sheet's "Next reminder due" turns yellow on the day. After each one, fill in "Last reminder sent" and add 1 to "Reminders sent". Every reminder offers a way to stop them; if they say no, set Result to "Passed but said no" and stop.
5. **Recheck after 90 days.** If 90 days have passed since the check, do the quick recheck before the next reminder: Google profile still verified, website still up, phone and email still match. If it no longer passes, send the "Didn't pass" email instead.
6. **They pay.** Stripe emails you. Fill in paid date, amount and payment number. Then ask Claude: "Add [business] to the verified directory: [trade], [city, state], [website], checked [date]." Fill in the directory id.
7. **Wait until Emil has put it live.** The badge links to the business's profile, so the profile has to be on the live website first, or the link leads nowhere. Ask Emil to put it live the same day if he can. Then open `followthroughguides.com/verified` and check the business is there. Fill in "Live in directory".
8. **Send the badge** (the "Your badge" template in `11-verified-badge.md`). Fill in "Badge emailed".
9. **Once a year,** for every business in the directory: search the business on Google Maps and check the profile is still verified, the website still works and the phone number still matches. If one fails, email them (below) and give them 14 days to fix it before taking the profile down.

### Reminder emails

Reply in the same thread as the "Passed" email, so they see the result again.

**Day 3.** Subject: Re: your Verified Business check

> Hi [name], a quick reminder: [business] passed the check, and your badge is ready as soon as the one-time $25 is paid: [payment link]. Any questions, just reply.
>
> If you'd rather not get the badge, reply "no thanks" and I'll stop these reminders.

**Day 7**

> Hi [name], your badge is still waiting for you. Once it's paid you get the badge for your website, with a short code to paste in, and a profile in the directory of verified businesses that links to your site: [payment link].
>
> If you'd rather not, reply "no thanks" and I won't remind you again.

**Day 14, then every 30 days**

> Hi [name], just checking in. [Business]'s check result still stands, so the badge is yours whenever you want it: $25, one time: [payment link].
>
> Reply "no thanks" and I'll stop these reminders.

**After a recheck at 90 days or more**, add this line at the start: "I checked [business] again today and it still passes."

### Emails for later

**The yearly recheck found a problem.** Subject: your Verified Business badge

> Hi [name], I recheck every business in the verified directory once a year. This time [what failed, e.g. your Google profile no longer shows as verified]. Could you fix that in the next 14 days and reply when it's done? If it's still not fixed by [date], I'll have to take your profile down, and the badge will need to come off your website.

**Taking a profile down** (after the 14 days, or if the business closed or misused the badge). First ask Claude to remove them from the directory and Emil to put it live. Then:

> Hi [name], as I mentioned on [date], [business] no longer passes the Verified Business check because [reason], so I've taken its profile out of the directory. Please remove the badge from your website. If things change, reply and I'll check again for free.

## 4. Visibility Autopilot

### At a glance

| When | What happens | Who |
|---|---|---|
| Day 0 | The form on `/visibility` arrives as "Visibility Autopilot ([plan]): [business]" | Customer |
| Within 2 business days | You reply with the next steps and the payment link | You |
| Day 1 (they sign up) | Stripe takes their card, charges nothing yet. You send the welcome email | Customer, you |
| Days 1–7 | They send their details and give you access. You do the first full check and send it | Both |
| Weeks 1–4 | Growth and Done-for-you: listings set up by hand, posts start | You |
| Day 23 | You email them: what's done, and that the first charge is on day 31 | You |
| Day 31 | Stripe charges the first month | Stripe |
| Every month | The work for their plan, and the report by the 5th working day | You |
| Done-for-you, every month | A 30-minute call on Zoom or Google Meet, after the report | Both |
| When they leave | Their last paid month runs out, you remove your access, everything stays theirs | You |

### Step 1: the inquiry arrives

The form promises a reply "usually within 2 business days". Reply to the email the website sent you (it goes straight to the customer). Pick the template for the plan they chose.

**They picked a plan.** Subject: Re: Visibility Autopilot ([plan]) for [business]

> Hi [name],
>
> Thanks for your interest in [plan] for [business]. Here's how it starts:
>
> 1. Sign up here: [payment link for the plan]. You add your card, but nothing is charged for 30 days. If you cancel by email before then, you pay nothing.
> 2. I email you a short list of what I need: your business details, a few photos and manager access to your Google profile. About 15 minutes of your time.
> 3. Within your first week, you get a full check of your Google profile, your listings and your website, with what to fix first.
>
> [Starter:] After that, every month you get a website check with the fixes ranked, a check of your listings, and a one-page report in plain numbers.
> [Growth:] After that, I set up your listings on the directories that matter most for [trade] and look after your Google profile every week, with a one-page report in plain numbers each month.
> [Done-for-you:] After that, I set up your listings, look after your Google profile every week and make the website fixes for you. Once a month we go through the report together in a 30-minute video call on Zoom or Google Meet.
>
> [Answer their question or message here, if they wrote one.]
>
> The service terms are here: followthroughguides.com/service-terms.

**They picked "Not sure yet."**

> Hi [name],
>
> Thanks for getting in touch about [business]. Three quick questions, and I'll tell you which plan fits:
>
> 1. When I find something to fix, would you rather make the change yourself, or have it done for you?
> 2. Do you have time each week for Google posts and replying to reviews, or are you out on jobs all day?
> 3. Does your website need work: slow on a phone, hard to find your number, a quote form that doesn't work?
>
> In short: Starter ($99) if you like doing it yourself and want to know what to fix first. Growth ($199) if you're busy on jobs and want your listings and Google profile looked after. Done-for-you ($299) if your website needs work too. Every plan starts with 30 days free.

When they answer, send the "picked a plan" email for the plan that fits.

**They gave a phone number and want to talk.** Everything works by email, but a short video call is fine:

> Hi [name], happy to talk it through. I work by email and video from Europe, so a 15-minute Zoom or Google Meet call works best. I'm free [two or three times, in their time zone, e.g. Tuesday or Wednesday at 8am or 4pm Eastern]. Which suits you? I'll send the link.

Use their time zone: 8–9am in their morning is 15:00–16:00 in Eastern Europe for the East Coast, later for the West. After the call, send the "picked a plan" email.

**If they don't reply:** one follow-up after 5 days ("Just checking this reached you. Happy to answer any questions."), then leave it.

### Step 2: they sign up

Stripe emails you about the new subscription (the "Business name" field tells you who it is).

1. In the customer list ("Autopilot customers"): contact details, plan, price, and today's date as the start date. "Free month ends" fills in by itself.
2. In Google Drive, open `autopilot-customer.xlsx` (the blank copy), **File** → **Make a copy**, and name it "Autopilot – [business]". Paste its link into the customer list.
3. In the copy, fill in what you already know on the Business details tab: name, plan and **trade**. The trade marks the core directories on the Listing check tab.
4. Send the welcome email (below), the same day.

**The welcome email.** Subject: welcome to Visibility Autopilot: what I need from you

> Hi [name],
>
> Welcome, and thanks for signing up for [plan]. Your free month runs until [free month ends]. Nothing is charged before then.
>
> To get started, I need a few things from you. Most owners do it in 15 minutes.
>
> **1. Your business details.** Reply with these, exactly as you want customers to see them everywhere:
> - Business name
> - Phone number customers call
> - Email for customers
> - Website
> - Address, and whether customers should see it (if you work from home, they shouldn't)
> - Hours
> - Your main services
> - The towns or ZIP codes you serve
> - License numbers, if your state requires showing them
> - The year you started
> - A few sentences about the business, in your own words
>
> **2. Your logo and 5–10 photos of your work**, attached to your reply, or a link to a folder.
>
> **3. Manager access to your Google Business Profile.** You keep ownership and can remove me at any time:
> 1. Sign in to the Google account that owns your profile, and search Google for your business name.
> 2. In the box for your profile, click the three dots (⋮), then **Business Profile settings**, then **People and access**.
> 3. Click **Add**, type [your email], choose **Manager**, and click **Invite**.
>
> **4. Access to Google Search Console**, if you have it (it's Google's free tool that shows how your website does in search):
> 1. Go to search.google.com/search-console and sign in.
> 2. Pick your website at the top left, then **Settings** (bottom left), then **Users and permissions**.
> 3. Click **Add user**, type [your email], choose **Full**, and click **Add**.
>
> If you've never set it up, just tell me which website builder you use (Wix, Squarespace, WordPress, something else) and I'll send the steps.
>
> [Done-for-you only:]
> **5. Access to your website**, so I can make the fixes:
> - **Wix:** in your dashboard, **Settings** → **Roles & Permissions** → **Invite People**, type [your email], choose **Website Manager**, and click **Send Invite**.
> - **Squarespace:** **Settings** → **Permissions & Ownership** → **Invite contributor**, type [your email], choose **Website Editor**, and click **Invite**.
> - **WordPress:** **Users** → **Add New User**, type [your email], choose **Administrator**, and click **Add New User**.
> - **Someone else built it:** forward this email to them.
>
> Menus move around sometimes. If a step doesn't match what you see, just reply and I'll help.
>
> Within a week of getting these, you'll have your first full check.

**If something's missing after 3 days,** a short nudge: "Just a reminder: I'm still waiting for [what's missing] before I can do your first check. Any questions, reply here." Fill in the access dates in the customer list as they come.

### Step 3: the first full check (within the first week)

Once you have the details and Google access:

1. Fill in the Business details tab from their reply. Every listing is copied from here, so all of them match exactly. Put the logo and photos in a Google Drive folder and link it.
2. **Listing check tab:** search every directory for the business name and phone. Mark each Correct, Wrong, Missing; add the link and what's wrong.
3. **Website check tab:** the checks listed on the sheet's Start here tab. One row per problem, with High, Medium or Low, and one sentence on how to fix it.
4. **Numbers tab:** type this month as the first month (e.g. 2026-11-01) and fill in what you can see today. This is the starting point the reports compare with.
5. Send the first check (below).

**The first check.** Subject: your first check: [business]

> Hi [name],
>
> Here's where [business] stands today. This is the starting point your monthly reports compare with.
>
> **Google profile:** [calls, website clicks and direction requests last month; reviews and average rating; what's missing, e.g. no photos, no hours].
>
> **Listings:** [X] of the [Y] directories that matter most for [trade] are correct. [Z] are wrong and [W] are missing. The biggest ones: [e.g. your Yelp listing has an old phone number; you're not on Apple Maps].
>
> **Website:** [speed score on a phone, out of 100], and the top problems:
> 1. [problem]: [how to fix it]
> 2. …
>
> [Starter:] What to do first: [the top 1–3 fixes, in order]. Here are the links to fix the wrong listings: [links].
> [Growth and Done-for-you:] What happens next: over the next few weeks I set up and correct your listings, starting with the biggest. [Done-for-you: and I start on the website fixes, starting with number 1.]
>
> Any questions, just reply.

### Step 4: the first month's setup (Growth and Done-for-you)

1. **Listings.** Set up or correct every core listing (marked Yes on the Listing check tab), the most important first. Copy everything from Business details. Use the owner's email for each account where you can, so the listings are theirs, and save each login in your password manager. Fill in "Fixed on" and "Login in password manager".
2. **Warn the owner about codes** before you start (email below). Many directories confirm a business with a code by phone, text or post.
3. **Posts.** Write the first month of weekly posts on the Posts tab and schedule them in the Google profile. Offers go out only once the owner has said yes.
4. **Reviews.** From now on, Google emails you as a manager when a review comes in (see "Every month").
5. **Done-for-you: the website.** Check a backup exists before the first change (Wix: **Site History**; WordPress: a backup plugin such as UpdraftPlus, free; Squarespace keeps no full backups, so note the old text before changing a page). Then start on the top of the Website check tab.

**Codes are on their way.** Subject: codes from directories: please pass them on

> Hi [name], this week I'm setting up your listings on [number] directories. Some of them confirm that the business is real by sending a code, by text, a phone call or a postcard to your business address. When one comes in, please forward it to me the same day (a photo of a postcard is fine): most codes expire within a few days.
>
> Some of these sites (Yelp, Yellow Pages, Angi, Thumbtack) may call to sell you ads or leads. You don't need any of it for this. Just say no thanks.

### Step 5: the free month ends (day 23)

The sheet's "Free month ends" turns yellow 7 days before. Send this, then fill in "Free-month email sent". It's honest, and US rules expect a reminder before a free trial turns into a paid plan. Stripe also sends its own reminder once that's switched on (`12-payments.md`).

Subject: your free month ends on [date]

> Hi [name],
>
> A quick update before your free month ends on [free month ends].
>
> So far: [2–4 lines, e.g. "12 listings set up or corrected, 4 Google posts published, 3 reviews replied to, your website check sent"].
>
> On [the day after], your card is charged $[price] for your first month of [plan]. You don't need to do anything to continue. If you'd rather stop, reply "cancel" before [free month ends] and you won't be charged at all.

If they cancel now: see "When they leave".

### Every month

**The report covers a calendar month** and goes out by the 5th working day of the next month, for every customer at once. A customer who started mid-month gets a short first report.

| When | All plans | Growth and Done-for-you add | Done-for-you adds |
|---|---|---|---|
| Every day you work | | Forward new-review alerts to the owner the same day. Reply within 2 working days (the Reviews tab turns yellow at 2) | |
| Every Monday | | Ask for 2–3 photos of the week's work (text below). Add the best to the profile | |
| First week of the month | Website check. Core listings check. Every 3 months: all directories | Fix anything the listing check finds. Write and schedule the month's posts | Website fixes from the top of the list |
| By the 5th working day | The report (below) | | |
| After the report | | | The 30-minute call on Zoom or Google Meet |

**The report.** Fill in the Numbers tab for the month: calls, website clicks and direction requests from the Google profile's **Performance** page; new reviews and average rating; the listing and open-problem counts from the bottom of the Report tab; the speed score from pagespeed.web.dev (mobile). The grey columns count by themselves. On the Report tab, type the month in the yellow cell, write the three notes, and send it. Subject: your [month] report: [business]

> Hi [name], here's your report for [month], with last month next to it.
>
> [Paste the Report tab, or attach it as a PDF: File → Download → PDF.]
>
> In one line: [the main thing that moved, e.g. "calls from Google went up from 10 to 14, and two more listings are now correct"].
>
> [Starter:] This month's top fixes for you: [1–3].
> [Done-for-you:] Let's go through it on our call. [Times, or "see you on [day]"].

Leave out rows that aren't in their plan (Starter has no posts or review replies).

**Review replies.** Forward each alert to the owner the same day: "New [stars]-star review from [name]: '[first line]'. Good moment to thank them." Reply in the owner's voice within 2 working days. For 1 or 2 stars, ask first:

> Hi [name], a 2-star review came in from [reviewer]: "[review]". Here's the reply I suggest: "[draft]". OK to post, or would you like to change it? Do you know what happened on that job?

**Monday photos text** (email if they prefer):

> Hi [name], any photos from this week's jobs? 2–3 is plenty, before and after is best. I'll add the best ones to your Google profile.

**Offers in posts.** Before scheduling a post with an offer: "For next week's post, I'd like to mention [offer]. OK?" Mark "Owner approved" on the Posts tab.

**Done-for-you: the monthly call.** Book it when you send the report. Use Google Meet (free with your Google account) or Zoom (free for 40 minutes), and put the link in the Calls tab:

> Hi [name], time for our monthly call: 30 minutes to go through the report, agree next month's top three fixes, and hear which jobs you want more of. I'm free [two or three times, their time zone]. Which suits you? I'll send a Google Meet link.

After the call, a short recap, and note it on the Calls tab:

> Thanks for the call. What we agreed: 1. [fix] 2. [fix] 3. [fix]. Posts this month will focus on [theme], since you want more [jobs].

### Changing plan

They can move up or down at any time by email. The new plan starts with their next monthly bill. If they move up and want the extra work to start sooner, start it then anyway, so they don't wait. (How to change the plan in Stripe gets added once Stripe is set up.)

> Hi [name], done: from your next bill on [date], you're on [new plan] at $[price] a month. [What changes, e.g. "I'll start setting up your listings this week."]

Change the plan and price in the customer list, and on the Business details tab.

### When a payment fails

Stripe retries and emails them by itself. If it still hasn't gone through after a week:

> Hi [name], your payment for [plan] didn't go through. Stripe should have emailed you a link to update your card. Could you take a look this week? If anything's changed, or you'd like to pause, just reply.

If it's still not fixed after another week, the service terms let you stop the service. Send one last email saying when it stops, then follow "When they leave".

### When they leave

They can cancel any time by email, for free. The month they've paid for runs to its end and isn't refunded. During the free month, they pay nothing.

1. **Confirm the same day:**

> Hi [name], sorry to see you go, and thanks for trying Visibility Autopilot. Your plan is cancelled: [during the free month: "you won't be charged anything"] [after it: "you won't be charged again, and I'll keep working until the end of your paid month on [date]"].
>
> Everything stays yours: your Google profile, your listings and everything posted. Before I go, I'll send you a list of your listings with their links, and remove my access.
>
> If you have a minute: what would have made it worth keeping? One line is plenty.

2. **Cancel in Stripe** (`12-payments.md`, "Day to day"): straight away during the free month, at the end of the period after it. Fill in "Asked to cancel" and "Service ends" in the customer list.
3. **On the last day:** delete any posts scheduled after it. Send the final list of listings (from the Listing check tab: directory, link, which email the account is under). Send a last report if the month is mostly done.
4. **Remove your access:** in their Google profile, **Business Profile settings** → **People and access** → the three dots next to your name → **Remove**. Do the same in Search Console (**Settings** → **Users and permissions**) and, on Done-for-you, on their website. If any of these won't let you remove yourself, ask the owner to remove you. Fill in "My access removed".
5. **Tidy up:** delete their logins from your password manager. Move their workbook to a "Former customers" folder in Google Drive. Keep the customer list row (it's your record of payments).

**If you have to end the service** (other than for a failed payment or a dishonest request), the service terms promise 30 days' notice by email:

> Hi [name], I'm writing to let you know that I'll stop providing Visibility Autopilot on [date, at least 30 days away]. Until then, everything carries on as normal, and you won't be charged after [date]. Everything stays yours, and before I go I'll send you a list of your listings and remove my access.
