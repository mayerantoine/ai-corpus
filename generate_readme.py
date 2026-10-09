#!/usr/bin/env python3
"""Render README.md from papers.json (grouped by topic).

Thin shim over extract_papers.generate_readme so the README can be regenerated
after hand-editing papers.json, without re-parsing any PDFs.

    uv run generate_readme.py
"""

import argparse

from extract_papers import generate_readme

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-i", "--input", default="papers.json")
    ap.add_argument("--readme", default="README.md")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    generate_readme(args.input, args.readme, args.quiet)
