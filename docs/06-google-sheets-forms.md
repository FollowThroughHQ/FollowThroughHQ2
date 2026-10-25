# Saving signups to Google Sheets

Important: the signup form can only send data to Google once the site is hosted on your own address (for example GitHub Pages). The preview on claude.ai blocks requests to other sites, so the form there only opens the visitor's email app.

## Option A: no code (easiest)
Use **Tally**, **Google Forms**, **Typeform** or **Formspree**. Create a form with email and trade, connect it to Google Sheets in the form's settings or integrations, and point the signup button at the form link. Good for a first test.

## Option B: your own form saves to a sheet (Google Apps Script)

### 1. Create the sheet
Create a Google Sheet named `FollowThrough Leads`. Rename the first tab `Leads`. Add headers in row 1: `Timestamp`, `Email`, `Trade`, `Consent`, `Page`.

### 2. Add the script
In the sheet, open **Extensions > Apps Script**, replace the code with:

```javascript
function doPost(e) {
  var d = e.parameter;
  if (d.hp) return ContentService.createTextOutput('ok'); // spam trap
  if (!d.email || d.email.indexOf('@') < 1) {
    return ContentService.createTextOutput('bad email');
  }
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Leads');
  sheet.appendRow([new Date(), d.email, d.trade || '', d.consent || '', d.page || '']);
  // Optional: email the playbook link automatically
  // MailApp.sendEmail(d.email, 'Your free playbook', 'Here it is: https://YOUR-LINK');
  return ContentService.createTextOutput('ok');
}
```

### 3. Deploy it
1. Click **Deploy > New deployment**, choose type **Web app**.
2. Set **Execute as: Me** and **Who has access: Anyone**.
3. Click **Deploy** and approve the permissions.
4. Copy the **Web app URL** (ends in `/exec`).

### 4. Connect the site
In `resources/views/home.blade.php`, replace the `wireSignup` function with the code below, and add the `SHEET_URL` line at the top of the script:

```javascript
var SHEET_URL = "PASTE-YOUR-WEB-APP-URL-HERE";
function wireSignup(label) {
  var f = document.getElementById("f");
  if (!f) return;
  f.onsubmit = function (e) {
    e.preventDefault();
    var body = new URLSearchParams({
      email: document.getElementById("em").value,
      trade: label,
      consent: "yes " + new Date().toISOString(),
      page: location.pathname,
      hp: ""
    });
    fetch(SHEET_URL, { method: "POST", mode: "no-cors", body: body })
      .then(function () { f.innerHTML = "<p>Thanks! Your playbook is on its way.</p>"; })
      .catch(function () { f.innerHTML = "<p>Something went wrong. Please email " + CONTACT + ".</p>"; });
  };
}
```

### 5. Test
Submit the form on the hosted site. A new row should appear within seconds. If you edit the script later, create a **new deployment** (or manage the existing one and pick a new version).

## Notes
- **Delivery:** the form saves the email. You can send the playbook manually, with the optional `MailApp` line (free accounts have a daily send limit), or with a newsletter tool such as MailerLite or Mailchimp.
- **Privacy:** keep the sheet private and do not share the link. Update the privacy policy to say signups are stored in Google Sheets. Keep the consent timestamp. Delete rows when someone asks.
- **Spam:** the hidden `hp` field is a simple trap. Add reCAPTCHA or Cloudflare Turnstile if spam appears.
- **Limits:** Apps Script is fine for hundreds of signups. For thousands, move to a newsletter tool.
