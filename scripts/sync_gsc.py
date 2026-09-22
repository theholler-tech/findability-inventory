#!/usr/bin/env python3
"""Pull Search Console search analytics into data/gsc/. No secrets written."""
import json
import os
from datetime import date, timedelta
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
CANDIDATES = [
    "sc-domain:gclawgroup.com",
    "https://gclawgroup.com/",
    "https://gclawgroup.com",
]
OUT = Path("data/gsc")


def main() -> None:
    raw = os.environ.get("GSC_SA_JSON", "").strip()
    if not raw:
        raise SystemExit("GSC_SA_JSON secret is empty")
    info = json.loads(raw)
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    service = build("searchconsole", "v1", credentials=creds, cache_discovery=False)

    end = date.today() - timedelta(days=3)
    start = end - timedelta(days=27)
    site = pick_site(service)
    OUT.mkdir(parents=True, exist_ok=True)

    queries = fetch(service, site, start, end, ["query"])
    pages = fetch(service, site, start, end, ["page"])
    devices = fetch(service, site, start, end, ["device"])

    payload = {
        "site": site,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "queries": queries,
        "pages": pages,
        "devices": devices,
    }
    (OUT / "last28.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (OUT / "SUMMARY.md").write_text(render(payload), encoding="utf-8")
    print(f"wrote {site} {start}..{end} queries={len(queries)} pages={len(pages)}")


def pick_site(service) -> str:
    listed = service.sites().list().execute().get("siteEntry", [])
    urls = [row.get("siteUrl") for row in listed]
    print("sites visible to robot:", urls)
    for candidate in CANDIDATES:
        if candidate in urls:
            return candidate
    if urls:
        return urls[0]
    raise SystemExit("robot can see no Search Console properties")


def fetch(service, site, start, end, dimensions):
    body = {
        "startDate": start.isoformat(),
        "endDate": end.isoformat(),
        "dimensions": dimensions,
        "rowLimit": 250,
        "dataState": "final",
    }
    rows = (
        service.searchanalytics()
        .query(siteUrl=site, body=body)
        .execute()
        .get("rows", [])
    )
    key = dimensions[0]
    out = []
    for row in rows:
        out.append(
            {
                key: row["keys"][0],
                "clicks": row.get("clicks", 0),
                "impressions": row.get("impressions", 0),
                "ctr": round(row.get("ctr", 0), 4),
                "position": round(row.get("position", 0), 2),
            }
        )
    return out


def render(payload) -> str:
    lines = [
        "# GSC last 28 days",
        "",
        f"Site: `{payload['site']}`",
        f"Range: {payload['start']} to {payload['end']} (ends 3 days ago; Search Console lags).",
        "",
        "## Top queries by impressions",
        "",
        "| Query | Clicks | Impressions | CTR | Position |",
        "|---|---:|---:|---:|---:|",
    ]
    queries = sorted(payload["queries"], key=lambda r: r["impressions"], reverse=True)[:25]
    for row in queries:
        lines.append(
            f"| {row['query']} | {row['clicks']} | {row['impressions']} | {row['ctr']} | {row['position']} |"
        )
    lines += ["", "## Top pages by clicks", "", "| Page | Clicks | Impressions | Position |", "|---|---:|---:|---:|"]
    pages = sorted(payload["pages"], key=lambda r: r["clicks"], reverse=True)[:15]
    for row in pages:
        lines.append(
            f"| {row['page']} | {row['clicks']} | {row['impressions']} | {row['position']} |"
        )
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
