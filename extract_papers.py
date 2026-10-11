#!/usr/bin/env python3
"""Extract title/authors from every PDF in papers/ and render a topic-grouped README.

    uv run extract_papers.py all

The JSON is the durable artifact and is meant to be hand-edited: fix an entry,
set "manually_edited": true, and later runs will leave it alone.
"""

# Warning suppression must happen before pdfplumber is imported: pdfminer and
# fontTools otherwise emit CFF/XObject noise that drowns the progress output.
import logging
import warnings

warnings.filterwarnings("ignore")
for _name in (
    "pdfminer",
    "pdfminer.pdffont",
    "pdfminer.pdfinterp",
    "pdfminer.converter",
    "fontTools",
    "fontTools.ttLib",
    "fontTools.subset",
    "pdfplumber",
):
    logging.getLogger(_name).setLevel(logging.ERROR)

import argparse
import hashlib
import json
import re
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus

import pdfplumber

# --------------------------------------------------------------------------
# Topic rules -- edit freely. Score = weight * (3 if the keyword appears in the
# title else 1), summed; highest score wins, ties broken by the order here.
# --------------------------------------------------------------------------
TOPIC_RULES = {
    "Mixture-of-Experts": (2.5, ["mixture-of-experts", "mixture of experts", "sparsely-gated", "moe"]),
    "Fine-tuning & PEFT": (2.0, ["lora", "qlora", "adapter", "parameter-efficient", "fine-tuning",
                                 "finetuning", "prefix-tuning", "p-tuning", "quantized"]),
    "Context Engineering": (2.0, ["context engineering", "context window", "long context",
                                  "context management", "shared context"]),
    "Deep Research & Literature Review": (2.0, ["deep research", "literature review",
                                                "systematic literature", "systematic review",
                                                "systematic examination"]),
    "Data Agents": (2.0, ["data agent", "data analysis", "text-to-sql", "data insight",
                          "data question"]),
    "RAG & Retrieval": (1.5, ["retrieval-augmented", "rag", "retriever", "retrieval",
                              "dense retrieval", "vector database", "keyword search"]),
    "Prompting & Reasoning": (1.5, ["chain-of-thought", "chain of thought", "prompting",
                                    "reasoning", "self-consistency", "least-to-most",
                                    "tree of thoughts", "prompt engineer", "zero-shot"]),
    "Memory": (1.5, ["memory", "episodic", "long-term memory"]),
    "Foundation Models": (1.5, ["llama", "gpt-4", "mistral", "foundation model",
                                "technical report", "apple intelligence"]),
    "Evaluation & Benchmarks": (1.5, ["benchmark", "evaluation", "evaluating", "hallucination"]),
    "Software Engineering with AI": (1.5, ["software engineering", "sdlc", "code generation",
                                           "vibe coding", "kanban", "developer", "skills for claude"]),
    # Must outrank the generic agent rule below: these titles all contain "agent".
    # Keywords are matched with (?<![a-z])kw(?![a-z]), so a singular form will
    # NOT match its plural -- list both where the plural is the common usage.
    "Agent Skills": (2.0, ["agent skill", "agent skills", "agentic skill", "agentic skills",
                           "skill.md", "skill library", "skill libraries",
                           "skill registry", "skill package", "skill packages",
                           "skill evolution", "skill-induced", "procedural knowledge"]),
    "Agents & Multi-Agent Systems": (1.0, ["agent", "multi-agent", "agentic", "tool use",
                                           "autonomous"]),
    "Surveys": (1.0, ["survey", "taxonomy", "roadmap", "overview of"]),
}
UNCATEGORIZED = "Other / Uncategorized"

# --------------------------------------------------------------------------
# Patterns
# --------------------------------------------------------------------------
VENUE_HEADER = re.compile(
    r"^(published|accepted|under review|preprint|to appear|proceedings|arxiv:|vixra|"
    r"workshop|see discussions|©|copyright|\d{4}-\d|this (paper|work) )",
    re.I,
)
# Reversed/rotated arXiv stamp fragments that survive the upright filter.
STAMP = re.compile(r"^(\d{4}|\[[a-z.]+\]|\]?[a-zA-Z.]+\[|[a-zA-Z]{3}|\d+v\d+:\w+)$")
AFFIL = re.compile(
    r"(@|\buniversity\b|\binstitute\b|\blabs?\b|\bresearch\b|\binc\.|\bcollege\b|"
    r"\bcorporation\b|\bschool\b|\bacademy\b|\bdepartment\b)",
    re.I,
)
SECTION = re.compile(r"^\s*(abstract|introduction|a\s?b\s?s\s?t\s?r\s?a\s?c\s?t)\s*$", re.I)
# ResearchGate/journal cover-page furniture that sits where authors would be.
PUBLICATION_META = re.compile(
    r"^\s*(thesis|article|conference paper|chapter|book|preprint|technical report|"
    r"doi|citations?|reads?|all content|some of the authors|learn more|"
    r"january|february|march|april|may|june|july|august|september|october|"
    r"november|december)\b",
    re.I,
)
AUTHORS_LABEL = re.compile(r"^authors?\s*:\s*", re.I)
# Substring (not word-boundary) match: extraction often glues words together.
AFFIL_WORD = re.compile(
    r"(universit|institut|laborator|research|college|school|academy|department|"
    r"centre|center|corporation|technolog|foundation|hospital|ministry)",
    re.I,
)
MARKERS = "∗*†‡§¶⋆•"
NAME_STOPWORDS = {
    "university", "institute", "research", "labs", "lab", "abstract", "college",
    "school", "department", "academy", "corporation", "inc", "technology", "sciences",
    "science", "engineering", "computing", "center", "centre", "group", "team",
    "and", "the", "of", "for", "with", "equal", "contribution", "contributions",
}

MAX_TITLE_LINES = 4
MAX_TITLE_CHARS = 250
MAX_AUTHORS = 30


LIGATURES = {
    "ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "st", "ﬆ": "st",
    "œ": "oe", "æ": "ae",
}


def signature(s: str) -> str:
    """Normalized key for matching a text line against a char row.

    Ligatures are expanded because a PDF stores a single 'ﬃ' glyph where
    extract_text() may emit 'ffi' (or vice versa); without this, titles
    containing 'Efficient' silently fail to match their char row.
    """
    s = s.lower()
    for lig, plain in LIGATURES.items():
        s = s.replace(lig, plain)
    return re.sub(r"[^a-z0-9]", "", s)


# --------------------------------------------------------------------------
# Geometry
# --------------------------------------------------------------------------
def build_rows(page, merge_tol=6.0):
    """Group upright chars into visual lines.

    Vertically-adjacent buckets are merged so that LaTeX \\textsc titles -- whose
    large capitals and small capitals sit at different sizes *and* different tops
    -- rejoin into one row. Without this merge the rows do not align 1:1 with
    extract_text() lines and exact matching fails.
    """
    chars = [c for c in page.chars if c.get("upright", True)]
    buckets = defaultdict(list)
    for c in chars:
        buckets[round(c["top"])].append(c)

    rows = []
    for top in sorted(buckets):
        size = max(c["size"] for c in buckets[top])
        # Scale the tolerance with type size so display-sized decks merge too.
        tol = max(merge_tol, 0.45 * size)
        if rows and top - rows[-1]["top"] <= tol:
            rows[-1]["chars"].extend(buckets[top])
            rows[-1]["top"] = top
        else:
            rows.append({"top": top, "chars": list(buckets[top])})

    for r in rows:
        cs = sorted(r["chars"], key=lambda c: c["x0"])
        r["text"] = "".join(c["text"] for c in cs)
        r["sig"] = signature(r["text"])
        r["size"] = round(max(c["size"] for c in r["chars"]), 1)
        del r["chars"]
    return rows


def align_sizes(text_lines, rows, window=20):
    """Assign each leading text line a font size.

    Sequential two-pointer walk with *exact* signature equality. A loose
    substring match drags author and abstract lines up to title size; the
    forward-only pointer and the capped lookahead keep a line from reaching
    deep into the page to find a same-size body row.
    """
    out = []
    ri = 0
    for line in text_lines[:window]:
        key = signature(line)
        if not key:
            out.append((line, None))
            continue
        size = None
        for j in range(ri, min(ri + 3, len(rows))):
            row = rows[j]
            if row["sig"] == key:
                size = row["size"]
                ri = j + 1
                break
            # A row that begins with this line holds several columns' text
            # (side-by-side text boxes). Take its size but do not consume it,
            # since a following line may match its remainder.
            if len(key) >= 3 and row["sig"].startswith(key):
                size = row["size"]
                break
        out.append((line, size))
    return out


def looks_like_authors(line: str) -> bool:
    if AUTHORS_LABEL.match(line):
        return True
    if AFFIL.search(line):
        return True
    if sum(line.count(m) for m in MARKERS) >= 2:
        return True
    # "Zhang1, Hu2" -- digits glued to words are affiliation markers.
    return bool(re.search(r"[A-Za-z]\d[,\s∗*†]", line))


def join_title(parts):
    title = ""
    for p in parts:
        if title.endswith("-"):
            title = title[:-1] + p
        else:
            title = (title + " " + p).strip()
    return re.sub(r"\s+", " ", title).strip()


def extract_title(text_lines, rows):
    """Return (title, source). Title is the leading run of max-size lines."""
    sized = align_sizes(text_lines, rows)
    cand = [
        (l, s)
        for l, s in sized
        if l and not VENUE_HEADER.match(l) and not STAMP.match(l)
    ]
    if not any(s is not None for _, s in cand):
        for l in text_lines:
            if l and 10 <= len(l) <= MAX_TITLE_CHARS and not VENUE_HEADER.match(l):
                return l, "fallback"
        return "", "none"

    max_size = max(s for _, s in cand[:12] if s is not None)
    picked = []
    pending = []  # unmatched lines held back until the run continues
    for line, size in cand:
        if size is None:
            # A line whose char row we could not match (e.g. split across text
            # boxes). Keep it only if the run resumes at title size after it.
            if picked:
                pending.append(line)
            continue
        if size >= max_size - 0.6:
            if picked and (looks_like_authors(line) or SECTION.match(line)):
                break
            picked.extend(pending)
            pending = []
            picked.append(line)
            if len(picked) >= MAX_TITLE_LINES or len(join_title(picked)) > MAX_TITLE_CHARS:
                break
        elif picked:
            break

    if not picked:
        return "", "none"
    return join_title(picked), "font-size"


# --------------------------------------------------------------------------
# Authors
# --------------------------------------------------------------------------
def clean_name(raw: str) -> str:
    name = raw
    for m in MARKERS:
        name = name.replace(m, "")
    name = re.sub(r"\S+@\S+", "", name)          # emails
    name = re.sub(r"\([^)]*\)", "", name)        # parentheticals
    name = re.sub(r"\d+", "", name)              # affiliation digits
    # EdwardHu -> Edward Hu; also "AAgrawal" -> "A Agrawal" (initial glued to a
    # surname) and "Teixeirade" -> "Teixeira de" (lowercase particle glued on).
    name = re.sub(r"(?<=[a-z.])(?=[A-Z])", " ", name)
    name = re.sub(r"\b([A-Z])([A-Z][a-z])", r"\1 \2", name)
    name = re.sub(r"(?<=[a-z])(de|van|von|der|del|da|di)\b", r" \1", name)
    name = re.sub(r"\s+", " ", name).strip(" ,.;-")
    return name


def is_name(name: str) -> bool:
    if not (2 <= len(name) <= 60):
        return False
    if sum(ch.isalpha() for ch in name) < 2:
        return False
    if any(ch.isdigit() for ch in name):
        return False
    words = [w for w in re.split(r"[\s.]+", name.lower()) if w]
    if not words or all(w in NAME_STOPWORDS for w in words):
        return False
    # Reject affiliations that merged into a "name" (NUIGalway, Centrefor Data
    # Analytics) -- substring test, since PDF extraction drops word boundaries.
    if AFFIL_WORD.search(name):
        return False
    if len(words) > 5:
        return False
    # Personal names are capitalised throughout ("Rui Meng", "Albert Q. Jiang");
    # prose fragments ("A durable", "profile-aware work") are not.
    tokens = [t for t in re.split(r"[\s.]+", name) if t]
    particles = {"de", "van", "von", "der", "del", "da", "di", "la", "le", "bin", "al"}
    if any(not (t[0].isupper() or t.lower() in particles) for t in tokens):
        return False
    return bool(re.match(r"^[A-Z]", name))


def split_authors(line: str):
    line = AUTHORS_LABEL.sub("", line)
    line = re.sub(r"\band\b", ",", line, flags=re.I)
    if "," in line:
        parts = line.split(",")
    else:
        # Space-separated CamelCase style: "JasonWei XuezhiWang DaleSchuurmans"
        parts = re.split(r"\s{1,}", line) if len(line.split()) > 1 else [line]
    return [p for p in (clean_name(p) for p in parts) if p]


def extract_authors(text_lines, title_text):
    """Lines after the title, up to Abstract/affiliations, parsed into names."""
    tail = signature(title_text)
    start = 0
    acc = ""
    for i, line in enumerate(text_lines):
        if not signature(line):
            continue
        acc += signature(line)
        if tail and acc.endswith(tail):
            start = i + 1
            break
    else:
        start = 0

    authors = []
    for line in text_lines[start : start + 6]:
        line = line.strip()
        if not line:
            if authors:
                break
            continue
        if SECTION.match(line) or AFFIL.search(line) or PUBLICATION_META.search(line):
            break
        names = [n for n in split_authors(line) if is_name(n)]
        # A real author line is mostly multi-word personal names; a subtitle
        # ("Multi-Agent Profile Collaboration") splits into single words.
        if names and sum(" " in n for n in names) * 2 < len(names):
            names = []
        if not names:
            if authors:
                break
            continue
        authors.extend(names)
        if len(authors) >= MAX_AUTHORS:
            break

    # De-duplicate, preserve order.
    seen = set()
    out = []
    for a in authors[:MAX_AUTHORS]:
        if a.lower() not in seen:
            seen.add(a.lower())
            out.append(a)
    return out


# --------------------------------------------------------------------------
# Topic + confidence
# --------------------------------------------------------------------------
def classify(title, body):
    title_l = (title or "").lower()
    body_l = (body or "")[:3000].lower()
    best, best_score = UNCATEGORIZED, 0.0
    for topic, (weight, keywords) in TOPIC_RULES.items():
        score = 0.0
        for kw in keywords:
            pat = r"(?<![a-z])" + re.escape(kw) + r"(?![a-z])"
            if re.search(pat, title_l):
                score += weight * 3
            elif re.search(pat, body_l):
                score += weight
        if score > best_score:
            best, best_score = topic, score
    return best, round(best_score, 2)


def assess(title, authors, body, source, error):
    flags = []
    if error:
        flags.append("error")
    if not title:
        flags.append("no-title")
    else:
        if len(title) < 10:
            flags.append("title-too-short")
        if " " not in title:
            flags.append("title-single-word")
        if SECTION.match(title):
            flags.append("title-is-section-heading")
        if len(title) > 120 and title.rstrip().endswith("."):
            flags.append("title-looks-like-body-text")
        words = title.split()
        if words and sum(len(w) == 1 for w in words) / len(words) > 0.3:
            flags.append("title-collapsed")
        # Only flag titles that are genuinely author-shaped: an email, or a run
        # of comma-separated capitalised names. Marker glyphs and the word
        # "Research" appear in plenty of real titles.
        if "@" in title or len(re.findall(r"[A-Z][a-z]+[A-Z]", title)) >= 2:
            flags.append("title-looks-like-authors")
    if source == "fallback":
        flags.append("fallback-title")
    if not authors and "abstract" in (body or "").lower():
        flags.append("no-authors")

    confidence = "high" if not flags else ("medium" if len(flags) == 1 else "low")
    return confidence, flags


# --------------------------------------------------------------------------
# Extraction driver
# --------------------------------------------------------------------------
def extract_one(path: Path):
    rec = {
        "filename": path.name,
        "path": str(path.parent.name + "/" + path.name),
        "content_hash": hashlib.md5(path.read_bytes()).hexdigest(),
        "title": "",
        "title_source": "none",
        "authors": [],
        "topic": UNCATEGORIZED,
        "topic_score": 0.0,
        "num_pages": 0,
        "confidence": "low",
        "needs_review": True,
        "flags": [],
        "manually_edited": False,
        "error": None,
        "extracted_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    body = ""
    try:
        with pdfplumber.open(path) as pdf:
            rec["num_pages"] = len(pdf.pages)
            page = pdf.pages[0]
            body = page.extract_text() or ""
            text_lines = [l.strip() for l in body.split("\n")]
            rows = build_rows(page)

        title, source = extract_title(text_lines, rows)

        # Metadata fast path: only when it clearly beats a failed text parse.
        if not title:
            meta_title = (getattr(pdfplumber.open(path), "metadata", {}) or {}).get("Title", "")
            if isinstance(meta_title, str) and 8 <= len(meta_title.strip()) <= 250:
                if " " in meta_title and not re.match(r"^(microsoft word|untitled)", meta_title, re.I):
                    title, source = meta_title.strip(), "metadata"

        rec["title"] = title
        rec["title_source"] = source
        rec["authors"] = extract_authors(text_lines, title) if title else []
    except Exception as e:  # one bad PDF must never abort the run
        rec["error"] = f"{type(e).__name__}: {e}"

    rec["topic"], rec["topic_score"] = classify(rec["title"], body)
    rec["confidence"], rec["flags"] = assess(
        rec["title"], rec["authors"], body, rec["title_source"], rec["error"]
    )
    rec["needs_review"] = bool(rec["flags"])
    return rec


def cmd_extract(args):
    papers_dir = Path(args.papers_dir)
    if not papers_dir.is_dir():
        sys.exit(f"error: papers directory not found: {papers_dir}")

    pdfs = sorted(papers_dir.glob("*.pdf"))
    if args.limit:
        pdfs = pdfs[: args.limit]
    if not pdfs:
        sys.exit(f"error: no PDFs found in {papers_dir}")

    out_path = Path(args.out)
    previous = {}
    if out_path.exists() and not args.force:
        try:
            old = json.loads(out_path.read_text())
            previous = {p["filename"]: p for p in old.get("papers", [])}
        except (json.JSONDecodeError, KeyError):
            pass

    total = len(pdfs)
    started = time.time()
    records = []
    log = (lambda *a: None) if args.quiet else (lambda *a: print(*a, file=sys.stderr, flush=True))

    log(f"Scanning {total} PDFs in {papers_dir}/\n")
    for i, pdf in enumerate(pdfs, 1):
        kept = previous.get(pdf.name)
        if kept and kept.get("manually_edited") and not args.force:
            log(f"[{i}/{total}] Skipping (manually edited): {pdf.name}")
            records.append(kept)
            continue

        if args.quiet:
            print(f"\r[{i}/{total}] {pdf.name[:50]:<50}", end="", file=sys.stderr, flush=True)
        else:
            log(f"[{i}/{total}] Processing: {pdf.name}")

        rec = extract_one(pdf)
        records.append(rec)

        if not args.quiet:
            title = rec["title"] or "(none)"
            log(f"        title:   {title[:88]}")
            names = rec["authors"]
            shown = ", ".join(names[:3]) + (f", +{len(names) - 3}" if len(names) > 3 else "")
            log(f"        authors: {shown or '(none)'}")
            log(f"        topic:   {rec['topic']}  [{rec['confidence']}]")
            if args.verbose and rec["flags"]:
                log(f"        flags:   {', '.join(rec['flags'])}")
            if rec["error"]:
                log(f"        ERROR:   {rec['error']}")

    if args.quiet:
        print("", file=sys.stderr)

    by_topic = defaultdict(int)
    for r in records:
        by_topic[r["topic"]] += 1
    unique = len({r["content_hash"] for r in records})
    flagged = [r for r in records if r["needs_review"]]
    errors = [r for r in records if r["error"]]

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "papers_dir": str(papers_dir),
        "counts": {
            "files": len(records),
            "unique": unique,
            "needs_review": len(flagged),
            "errors": len(errors),
            "by_topic": dict(sorted(by_topic.items(), key=lambda kv: -kv[1])),
        },
        "papers": records,
    }
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")

    elapsed = time.time() - started
    log(f"\n{'=' * 62}")
    log(f"Wrote {out_path}  ({len(records)} files, {unique} unique papers)")
    log(f"Elapsed: {elapsed:.1f}s")
    log("\nBy topic:")
    for topic, n in payload["counts"]["by_topic"].items():
        log(f"  {n:3}  {topic}")
    if flagged:
        log(f"\nNeeds review ({len(flagged)}):")
        for r in flagged:
            log(f"  - {r['filename']}: {', '.join(r['flags'])}")
    if errors:
        log(f"\nErrors ({len(errors)}):")
        for r in errors:
            log(f"  - {r['filename']}: {r['error']}")
    return payload


# --------------------------------------------------------------------------
# README
# --------------------------------------------------------------------------
ARXIV_NEW = re.compile(r"^(\d{4}\.\d{4,5})(?:v\d+)?$")
ARXIV_OLD = re.compile(r"^([a-z-]+(?:\.[A-Z]{2})?/\d{7})(?:v\d+)?$")


def paper_link(paper: dict) -> tuple[str, str]:
    """(url, label) for a paper entry.

    Prefers the verified ``url`` recorded in papers.json. Falls back to a title
    search for the handful of entries with no public canonical URL (slide decks,
    internal specs) rather than inventing one.
    """
    url = paper.get("url")
    if url:
        if "arxiv.org" in url:
            return url, "arxiv"
        if "doi.org" in url:
            return url, "doi"
        return url, "link"
    title = paper.get("title") or Path(paper["filenames"][0]).stem
    return f"https://www.semanticscholar.org/search?q={quote_plus(title)}", "search"


def anchor(topic: str) -> str:
    return re.sub(r"[^a-z0-9\s-]", "", topic.lower()).strip().replace(" ", "-")


def load_links(links_path="links.json"):
    """Curated entries for papers with no local PDF.

    Hand-maintained and never written by the extractor, which rebuilds its
    records from papers/*.pdf alone and would otherwise drop them. A missing or
    malformed file is not fatal -- the README still renders from papers.json.
    """
    path = Path(links_path)
    if not path.exists():
        return []
    try:
        entries = json.loads(path.read_text()).get("papers", [])
    except (json.JSONDecodeError, AttributeError):
        print(f"warning: ignoring unreadable {path}", file=sys.stderr)
        return []
    # filenames=[] keeps these off paper_link's title-search fallback; every
    # curated entry carries a verified url.
    return [dict(e, filenames=[], needs_review=False) for e in entries]


def generate_readme(json_path="papers.json", readme_path="README.md",
                    links_path="links.json", quiet=False):
    data = json.loads(Path(json_path).read_text())
    papers = data["papers"]

    # Collapse byte-identical duplicates into one entry.
    groups = {}
    for p in papers:
        g = groups.setdefault(p["content_hash"], dict(p, filenames=[]))
        g["filenames"].append(p["filename"])

    by_topic = defaultdict(list)
    for g in groups.values():
        by_topic[g["topic"]].append(g)

    links = load_links(links_path)
    for e in links:
        by_topic[e["topic"]].append(e)

    order = sorted(by_topic, key=lambda t: (t == UNCATEGORIZED, -len(by_topic[t]), t))

    lines = [
        "# AI Corpus",
        "",
        f"{len(groups) + len(links)} papers \u2014 {len(groups)} indexed from PDFs, "
        f"{len(links)} curated links. Links only; no PDFs are stored in this repo.",
        f"Generated {data['generated_at'][:10]} by "
        "[`extract_papers.py`](extract_papers.py) from [`papers.json`](papers.json)"
        " and [`links.json`](links.json).",
        "",
        "Each entry shows its contribution `type` — see "
        "[`paper_types.md`](paper_types.md) for the taxonomy and rubrics.",
        "",
        "## Contents",
        "",
    ]
    for topic in order:
        lines.append(f"- [{topic}](#{anchor(topic)}) ({len(by_topic[topic])})")
    lines.append("")

    for topic in order:
        lines += [f"## {topic}", ""]
        for g in sorted(by_topic[topic], key=lambda x: (x["title"] or "~").lower()):
            title = g["title"] or f"_(title not extracted)_ `{g['filenames'][0]}`"
            names = g["authors"]
            who = ", ".join(names[:3]) + (f", +{len(names) - 3} more" if len(names) > 3 else "")
            flag = " ⚠️" if g["needs_review"] else ""
            link, host = paper_link(g)
            # Contribution type (see paper_types.md) -- a second axis beside topic.
            kind = g.get("type") or ""
            if kind and g.get("type_secondary"):
                kind += f"+{g['type_secondary']}"
            kind = f"`{kind}` · " if kind else ""
            lines.append(f"- **{title}**{flag}")
            lines.append(f"  {kind}{who or '_authors not detected_'} — [{host}]({link})")
            if g.get("note"):
                lines.append(f"  {g['note']}")
        lines.append("")

    flagged = [g for g in groups.values() if g["needs_review"]]
    if flagged:
        lines += [
            "## Needs Review",
            "",
            "Heuristic extraction was uncertain for these. Fix the entry in "
            "`papers.json`, set `\"manually_edited\": true` so it is preserved on "
            "re-run, then regenerate this file.",
            "",
            "| File | Extracted title | Flags |",
            "| --- | --- | --- |",
        ]
        for g in sorted(flagged, key=lambda x: x["filenames"][0].lower()):
            t = (g["title"] or "—").replace("|", "\\|")[:70]
            lines.append(f"| `{g['filenames'][0]}` | {t} | {', '.join(g['flags'])} |")
        lines.append("")

    Path(readme_path).write_text("\n".join(lines))
    if not quiet:
        print(f"Wrote {readme_path} ({len(groups)} from PDFs + {len(links)} curated "
              f"links, {len(order)} topics)", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")

    def add_extract_args(p):
        p.add_argument("--papers-dir", default="papers")
        p.add_argument("-o", "--out", default="papers.json")
        p.add_argument("--force", action="store_true",
                       help="re-extract even records marked manually_edited")
        p.add_argument("--limit", type=int, help="only process the first N PDFs")
        p.add_argument("--quiet", action="store_true")
        p.add_argument("--verbose", action="store_true")

    p_ex = sub.add_parser("extract", help="PDFs -> papers.json")
    add_extract_args(p_ex)

    p_rd = sub.add_parser("readme", help="papers.json + links.json -> README.md")
    p_rd.add_argument("-i", "--input", default="papers.json")
    p_rd.add_argument("--readme", default="README.md")
    p_rd.add_argument("--links", default="links.json")
    p_rd.add_argument("--quiet", action="store_true")

    p_all = sub.add_parser("all", help="extract then readme")
    add_extract_args(p_all)
    p_all.add_argument("--readme", default="README.md")
    p_all.add_argument("--links", default="links.json")

    args = ap.parse_args()
    if args.cmd in (None, "all"):
        if args.cmd is None:  # bare invocation == all, with defaults
            args = ap.parse_args(["all"])
        cmd_extract(args)
        generate_readme(args.out, args.readme, args.links, args.quiet)
    elif args.cmd == "extract":
        cmd_extract(args)
    elif args.cmd == "readme":
        generate_readme(args.input, args.readme, args.links, args.quiet)


if __name__ == "__main__":
    main()
