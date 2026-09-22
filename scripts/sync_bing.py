#!/usr/bin/env python3
"""Pull Bing Webmaster stats into data/bing/. Never writes the API key."""
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://ssl.bing.com/webmaster/api.svc/json/"
SITES = [
    "https://gclawgroup.com/",
    "https://gclawgroup.com",
    "http://gclawgroup.com/",
]
OUT = Path("data/bing")


def main() -> None:
    key = os.environ.get("BING_API_KEY", "").strip()
    if not key:
        raise SystemExit("BING_API_KEY secret is empty")
    site = None
    traffic = None
    last_error = "no site matched"
    for candidate in SITES:
        try:
            traffic = call(key, "GetRankAndTrafficStats", candidate)
            site = candidate
            break
        except RuntimeError as exc:
            last_error = str(exc)
            print(f"skip {candidate}: {exc}")
    if site is None:
        raise SystemExit(last_error)
    queries = call(key, "GetQueryStats", site)
    pages = call(key, "GetPageStats", site)
    OUT.mkdir(parents=True, exist_ok=True)
    payload = {
        "site": site,
        "pulled": datetime.now(timezone.utc).isoformat(),
        "traffic": slim(traffic),
        "queries": rollup(queries, "Query"),
        "pages": rollup(pages, "Query"),
    }
    (OUT / "last.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (OUT / "SUMMARY.md").write_text(render(payload), encoding="utf-8")
    print(
        f"wrote {site} days={len(payload['traffic'])} "
        f"queries={len(payload['queries'])} pages={len(payload['pages'])}"
    )


def call(key: str, method: str, site: str):
    query = urllib.parse.urlencode({"siteUrl": site, "apikey": key})
    url = f"{BASE}{method}?{query}"
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:300]
        raise RuntimeError(f"{method} HTTP {exc.code} {detail}") from exc
    return body.get("d", body)


def slim(rows):
    out = []
    for row in rows or []:
        out.append(
            {
                "date": ms_date(row.get("Date")),
                "clicks": row.get("Clicks", 0),
                "impressions": row.get("Impressions", 0),
            }
        )
    out.sort(key=lambda row: row["date"])
    return out[-28:]


def rollup(rows, field):
    bucket = defaultdict(lambda: {"clicks": 0, "impressions": 0, "pos_w": 0.0})
    for row in rows or []:
        name = row.get(field) or row.get("Query") or ""
        clicks = row.get("Clicks") or 0
        impressions = row.get("Impressions") or 0
        position = row.get("AvgImpressionPosition") or 0
        item = bucket[name]
        item["clicks"] += clicks
        item["impressions"] += impressions
        item["pos_w"] += position * impressions
    ranked = []
    for name, item in bucket.items():
        impressions = item["impressions"] or 0
        ranked.append(
            {
                "name": name,
                "clicks": item["clicks"],
                "impressions": impressions,
                "position": round(item["pos_w"] / impressions, 2) if impressions else 0,
            }
        )
    ranked.sort(key=lambda row: row["impressions"], reverse=True)
    return ranked[:40]


def ms_date(value) -> str:
    if not value or "Date(" not in str(value):
        return ""
    millis = int(str(value).split("Date(")[1].split("-")[0].split(")")[0].split("+")[0])
    return datetime.fromtimestamp(millis / 1000, timezone.utc).date().isoformat()


def render(payload) -> str:
    traffic = payload["traffic"]
    clicks = sum(row["clicks"] for row in traffic)
    impressions = sum(row["impressions"] for row in traffic)
    lines = [
        "# Bing Webmaster",
        "",
        f"Site: `{payload['site']}`",
        f"Pulled: {payload['pulled']}",
        f"Last {len(traffic)} days in the feed: {clicks} clicks, {impressions} impressions.",
        "",
        "## Top queries",
        "",
        "| Query | Clicks | Impressions | Position |",
        "|---|---:|---:|---:|",
    ]
    for row in payload["queries"][:25]:
        lines.append(
            f"| {row['name']} | {row['clicks']} | {row['impressions']} | {row['position']} |"
        )
    lines += ["", "## Top pages", "", "| Page | Clicks | Impressions | Position |", "|---|---:|---:|---:|"]
    for row in payload["pages"][:15]:
        lines.append(
            f"| {row['name']} | {row['clicks']} | {row['impressions']} | {row['position']} |"
        )
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
