# GitHub and hosting

## Create the repository (website method)
1. Create a free account at github.com and sign in.
2. Click the **+** at the top right, then **New repository**.
3. Name it (for example `followthrough`), add a description, choose **Public** (needed for free GitHub Pages), and click **Create repository**.
4. On the empty repo page, click **uploading an existing file**, drag in everything from this folder (`index.html`, `README.md`, `.gitignore`, and the `docs` folder), and click **Commit changes**.

## Create the repository (command line method)
```bash
cd followthrough-repo
git init
git add .
git commit -m "Initial commit: site and docs"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/followthrough.git
git push -u origin main
```
Create the empty repo on github.com first (without a README) so the push works.

## Host with GitHub Pages
1. In the repo, go to **Settings**, then **Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**, branch `main`, folder `/ (root)`, then **Save**.
3. After a minute the site is at `https://YOUR-USERNAME.github.io/followthrough/`.
4. In `index.html`, set `PUBLIC` to that address so "Related guides" links work.

## Use your own domain
1. Buy a domain (about $10-15 a year) from a registrar.
2. In **Settings > Pages**, enter the domain under **Custom domain**.
3. At your registrar, add the DNS records GitHub shows (see GitHub's custom domain docs for current values).
4. Tick **Enforce HTTPS** once available.
5. Update `PUBLIC` and `CONTACT` in `index.html`. Use an email address on your domain.

## Working with changes
Edit `index.html`, commit, and push. Pages redeploys automatically. Use short commit messages ("Add pressure washing guide"). Use branches for bigger changes.

## Do not commit
Lead lists, customer emails, passwords and API keys. The `.gitignore` excludes CSV files and a `leads/` folder. A public repo is visible to everyone.
