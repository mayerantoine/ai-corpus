#!/usr/bin/env python3
"""Sync titles and authors in papers.json from the arXiv API.

Heuristic PDF extraction truncates titles at punctuation ("Why Your Deep
Research Agent Fails?" lost its subtitle) and misses author blocks entirely.
Every entry with an arxiv.org/abs/ url has a canonical record upstream, so
prefer that.

    uv run sync_arxiv.py --dry-run     # show what would change
    uv run sync_arxiv.py               # apply

Two deliberate rules:

* A stored title is kept when it strictly contains the API title (ignoring
  case and punctuation). Local titles sometimes carry a subtitle the API
  record omits -- e.g. "Memory in the Age of AI Agents: A Survey". Syncing
  those would lose information.
* Author lists are capped at MAX_AUTHORS, matching the extractor's own
  convention, with the true total recorded in author_count. The README
  renders the first three names plus "+N more" computed from author_count,
  so storing more than three buys nothing -- and technical reports list
  hundreds (Llama 3: 561).

Entries with "manually_edited": true are skipped unless --force.
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

from extract_papers import MAX_AUTHORS

NS = {"a": "http://www.w3.org/2005/Atom"}
API = "http://export.arxiv.org/api/query"
ABS = re.compile(r"arxiv\.org/abs/(.+)$")
BATCH = 25


def base_id(aid: str) -> str:
    """Drop the version suffix from a modern arXiv id (2507.19457v2 -> 2507.19457)."""
    return aid.split("v")[0] if re.match(r"^\d{4}\.", aid) else aid


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def fetch(ids, quiet=False):
    """Canonical metadata keyed by versionless arXiv id."""
    out = {}
    for i in range(0, len(ids), BATCH):
        chunk = ids[i : i + BATCH]
        url = f"{API}?id_list={','.join(chunk)}&max_results={len(chunk)}"
        try:
            raw = urllib.request.urlopen(url, timeout=60).read()
        except (urllib.error.URLError, TimeoutError) as e:
            sys.exit(f"error: arXiv API request failed: {e}")
        for e in ET.fromstring(raw).findall("a:entry", NS):
            node = e.find("a:id", NS)
            if node is None:
                continue
            m = re.search(r"/abs/(.+)$", node.text or "")
            if not m:
                continue
            title = e.find("a:title", NS)
            pub = e.find("a:published", NS)
            out[base_id(m.group(1))] = {
                "title": " ".join((title.text or "").split()),
                "authors": [
                    " ".join((a.find("a:name", NS).text or "").split())
                    for a in e.findall("a:author", NS)
                ],
                "published": (pub.text or "")[:10] if pub is not None else "",
            }
        if not quiet:
            print(f"  fetched {len(out)}/{len(ids)}", file=sys.stderr)
        if i + BATCH < len(ids):
            time.sleep(1)  # be polite to the API
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-i", "--input", default="papers.json")
    ap.add_argument("--dry-run", action="store_true", help="report changes, write nothing")
    ap.add_argument("--force", action="store_true", help="also update manually_edited entries")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    path = Path(args.input)
    data = json.loads(path.read_text())
    papers = data["papers"]

    ids = sorted({base_id(ABS.search(p["url"]).group(1))
                  for p in papers if p.get("url") and ABS.search(p["url"])})
    if not ids:
        sys.exit("error: no arxiv.org/abs/ urls found")
    if not args.quiet:
        print(f"Fetching {len(ids)} arXiv records...", file=sys.stderr)
    meta = fetch(ids, args.quiet)

    changed = {"title": 0, "authors": 0, "flags": 0}
    kept_local, skipped, no_record = [], [], []

    for p in papers:
        m_url = ABS.search(p.get("url") or "")
        if not m_url:
            continue
        rec = meta.get(base_id(m_url.group(1)))
        if not rec:
            no_record.append(p["filename"])
            continue
        if p.get("manually_edited") and not args.force:
            skipped.append(p["filename"])
            continue

        # Title: adopt the API's unless the local one already contains it and
        # is longer -- that extra text is a subtitle worth keeping.
        new_t, old_t = rec["title"], p.get("title") or ""
        if norm(new_t) != norm(old_t):
            if norm(new_t) and norm(new_t) in norm(old_t) and len(old_t) > len(new_t):
                kept_local.append((p["filename"], old_t, new_t))
            else:
                p["title"] = new_t
                p["title_source"] = "arxiv-api"
                changed["title"] += 1

        # Authors: cap to the extractor's convention, record the true total.
        names = rec["authors"]
        if names and (p.get("authors") != names[:MAX_AUTHORS]
                      or p.get("author_count") != len(names)):
            p["authors"] = names[:MAX_AUTHORS]
            p["author_count"] = len(names)
            changed["authors"] += 1

        if rec["published"]:
            p.setdefault("published", rec["published"])

        # Clear flags the API just resolved: they were raised by the PDF text
        # parse, and leaving them would keep a complete entry in Needs Review.
        if p.get("flags"):
            resolved = set()
            if p["authors"]:
                resolved |= {"no-authors"}
            if p.get("title_source") == "arxiv-api":
                resolved |= {"fallback-title", "title-looks-like-authors"}
            kept = [f for f in p["flags"] if f not in resolved]
            if kept != p["flags"]:
                p["flags"] = kept
                p["needs_review"] = bool(kept)
                p["confidence"] = "high" if not kept else (
                    "medium" if len(kept) == 1 else "low")
                changed["flags"] += 1

    print(f"\ntitles updated:  {changed['title']}", file=sys.stderr)
    print(f"authors updated: {changed['authors']}", file=sys.stderr)
    print(f"flags cleared:   {changed['flags']}", file=sys.stderr)
    if kept_local:
        print(f"\nkept local title (more informative than arXiv's) — {len(kept_local)}:",
              file=sys.stderr)
        for fn, old, new in kept_local:
            print(f"  {fn}\n    kept: {old}\n    api:  {new}", file=sys.stderr)
    if skipped:
        print(f"\nskipped (manually_edited, use --force): {len(skipped)}", file=sys.stderr)
        for fn in skipped:
            print(f"  {fn}", file=sys.stderr)
    if no_record:
        print(f"\nno arXiv record returned: {len(no_record)}", file=sys.stderr)
        for fn in no_record:
            print(f"  {fn}", file=sys.stderr)

    if args.dry_run:
        print("\n--dry-run: nothing written", file=sys.stderr)
        return
    if not any(changed.values()):
        print("\nAlready in sync; nothing written.", file=sys.stderr)
        return
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"\nWrote {path}. Re-run generate_readme.py to refresh the README.",
          file=sys.stderr)


if __name__ == "__main__":
    main()
