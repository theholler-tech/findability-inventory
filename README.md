# findability-inventory

Private GCLG findability data mirror for Grok.

Grok cannot log into Google Search Console, Bing Webmaster, or Google Business Profile.
This repo is the standing source of truth: a human export or a GitHub Action writes
sanitized snapshots here. Later chats read `data/` instead of guessing rankings.

Do not commit API keys, service-account JSON, or Bing keys.

## What lives here

| Path | Purpose |
|---|---|
| `data/SUMMARY.md` | Human-readable snapshot Grok should read first |
| `data/gsc/` | Search Console last-28 (queries, pages) |
| `data/bing/` | Bing Webmaster (after API key) |
| `data/public/` | robots.txt, llms.txt status, NAP scan |
| `.github/workflows/` | Nightly sync (added after secrets exist) |

## Secrets (Actions only, never in files)

| Name | When |
|---|---|
| `GSC_SA_JSON` | After Google Cloud service account exists |
| `BING_API_KEY` | After Bing API key exists |

Same pattern as `theholler-tech/network-inventory` / `UNIFI_API_KEY`.
