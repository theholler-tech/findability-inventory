# GCLG findability handoff

Paused: 2026-09-22, about 5:45 PM Central.
Resume at **Step 6**. Do not restart Google, Bing, or WordPress login.

## Already done

| Door | State |
|---|---|
| Google Cloud | Billing on. Budget `GCLG stop-spend` at $1, alerts at 50/90/100%. Project **My First Project**, ID `optimum-airfoil-478923-h2`. |
| Search Console robot | `gclg-gsc-reader@optimum-airfoil-478923-h2.iam.gserviceaccount.com` has **Full** on `gclawgroup.com`. Owner login is `greencountrylawgroup@gmail.com`. |
| GSC secret | GitHub Actions secret `GSC_SA_JSON` only. Local JSON file was deleted. |
| GSC sync | Works. Weekly Monday 8:00 AM Central. Snapshot in `data/gsc/SUMMARY.md`. |
| Bing | Property `https://gclawgroup.com/` verified. Sitemap listed. |
| Bing secret | GitHub Actions secret `BING_API_KEY` only. Do not paste the key into chat. |
| Bing sync | Works. Weekly Monday 9:00 AM Central. Snapshot in `data/bing/SUMMARY.md`. |
| Repo | Private `theholler-tech/findability-inventory`. No secrets in files. |
| WordPress | Logged in as **Marketing Agent** on WP Engine. Yoast SEO and Yoast SEO Premium are active. |
| llms.txt | Turned **on** in Yoast → Settings → General → Site features → llms.txt. Public file is live: https://gclawgroup.com/llms.txt |

## Do not touch

- Do not click **update now** on Elementor or Elementor Pro.
- Do not click Yoast **First-time configuration** or **Install Site Kit by Google**.
- Do not turn on **Yoast AI**.
- Do not turn on **Schema aggregation endpoint** yet.
- Do not generate a new Bing API key. Do not delete the current one.
- Family-law expansion stays held. Wayne reviews copy before it is published.

## What the data says

Google (last 28 days ending ~2026-09-19): `tax attorney` ~6,269 impressions, 2 clicks, position ~8.8. `estate planning lawyer` was near position 2.7 with 0 clicks in the earlier export. Top clicked page is still `/who-gets-the-house-in-an-oklahoma-divorce/`.

Bing: mostly the firm name. Homepage and tribal-law page carry the impressions. Tax, estate, and probate are thin.

Public site before this pause:

- `robots.txt` allows Google, Bing, and AI retrieval bots. It sets `crawl-delay: 10` (slows Bing). Sitemap: `https://gclawgroup.com/sitemap_index.xml`.
- Homepage title was `Green Country Law Group | Your Trusted Legal Advocates`.
- Phone on the homepage: (918) 456-6113.

`llms.txt` now lists a few existing pages, including estate planning, plus car wrecks and criminal defense. Leave that file alone until the homepage title is reviewed.

## Step 6 — resume here

WordPress is already open. Yoast → **Settings** → **Site features** is where you left off.

1. On the left Yoast menu, click **Content types**.
2. Click **Homepage**.
3. Stop. Do not type. Do not click **Save**.
4. Send a screenshot of that Homepage screen.

After that screenshot, the next decision is the homepage SEO title. Do not change it until the exact replacement text is written here.

## After Step 6

1. Set the homepage SEO title (text supplied in chat, then one save).
2. Yoast → **Site representation**: confirm Organization / legal name, phone, and the four offices. Do not invent a schema type.
3. Remove `crawl-delay: 10` from `robots.txt` only after we see whether Yoast or a real file owns it.
4. Wayne packet for the estate-planning page (Google ranks the query and gets no clicks).
5. Wayne packet for the tax page (thousands of Google impressions, almost no clicks).
6. Google Business Profile and Wikidata later. Not this session.
