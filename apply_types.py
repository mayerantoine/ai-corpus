#!/usr/bin/env python3
"""Write the contribution-type fields into papers.json and links.json.

Adds `type` and `type_secondary` (nullable) per paper. See paper_types.md for
the taxonomy, the rubric for each type, and the two-type cap.

    uv run apply_types.py --dry-run     # show what would change
    uv run apply_types.py               # apply

Every assignment below was made by reading the paper's ABSTRACT, not its title:
titles mislead about contribution type often enough that title-based rules are
not usable (paper_types.md leads with seven worked examples). The `why` string
on each row is the abstract phrase the assignment rests on, so an assignment can
be audited without re-reading the paper.

Entries are keyed by versionless arXiv id where one exists, else by filename for
the eight documents with no arXiv record -- those eight are classified from the
document itself and are the weakest evidence here.
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

VALID = {"method", "survey", "benchmark", "evaluation", "empirical",
         "tech-report", "system", "practitioner"}

# arXiv id -> (type, type_secondary | None, abstract evidence)
BY_ARXIV = {
    "1407.7502":  ("survey", None, "book-length treatment of random forests theory and practice"),
    "1701.06538": ("method", None, "we introduce a Sparsely-Gated Mixture-of-Experts layer"),
    "1706.05098": ("survey", None, "overview of multi-task learning in deep neural networks"),
    "1805.12471": ("benchmark", "evaluation", "we introduce CoLA, 10,657 labeled sentences; as baselines we train several RNNs"),
    "2106.09685": ("method", None, "we propose Low-Rank Adaptation"),
    "2110.07602": ("method", None, "P-Tuning v2 can be comparable to fine-tuning"),
    "2201.11903": ("method", None, "chain-of-thought prompting improves reasoning ability"),
    "2203.08442": ("empirical", None, "we find Seq2Seq pretraining is a double-edged sword"),
    "2203.11171": ("method", None, "we propose a new decoding strategy, self-consistency"),
    "2205.10625": ("method", None, "we propose least-to-most prompting"),
    "2205.11916": ("method", None, "LLMs are decent zero-shot reasoners by adding 'Let's think step by step'"),
    "2208.02813": ("empirical", None, "we formally study how the MoE layer improves learning and why it will not collapse"),
    "2210.03493": ("method", None, "we propose Auto-CoT, which automatically constructs demonstrations"),
    "2210.11610": ("method", None, "we use a pre-trained LLM to generate high-confidence rationale-augmented answers"),
    "2211.01910": ("method", None, "we propose Automatic Prompt Engineer (APE)"),
    "2302.01107": ("survey", None, "survey of efficient training of transformers"),
    "2302.13971": ("tech-report", None, "we introduce LLaMA, a collection of foundation language models"),
    "2303.08774": ("tech-report", None, "we report the development of GPT-4"),
    "2305.10601": ("method", None, "we introduce Tree of Thoughts, a new framework for LM inference"),
    "2305.14314": ("method", None, "we present QLoRA, an efficient finetuning approach"),
    "2307.09288": ("tech-report", None, "we develop and release Llama 2"),
    "2310.03714": ("method", None, "we introduce DSPy, a programming model abstracting LM pipelines"),
    "2310.06825": ("tech-report", None, "we introduce Mistral 7B"),
    "2310.12931": ("method", None, "we introduce EUREKA, a human-level reward design algorithm"),
    "2402.01135": ("method", None, "we propose a multi-agent conversational recommender system"),
    "2404.13501": ("survey", None, "we propose a comprehensive survey of the memory mechanism"),
    "2407.21075": ("tech-report", None, "we present the foundation language models for Apple Intelligence"),
    "2407.21783": ("tech-report", None, "we present a new set of foundation models, Llama 3"),
    "2409.13740": ("evaluation", None, "we developed a rigorous human-AI comparison methodology to evaluate agents"),
    "2410.21333": ("empirical", None, "we identify characteristics of tasks where CoT reduces performance"),
    "2411.19710": ("benchmark", None, "dataset taxonomy and generation strategies for evaluating RAG"),
    "2412.15249": ("method", None, "we introduce a novel two-step search strategy and a prompting-based re-ranking mechanism"),
    "2503.21460": ("survey", None, "this survey covers methodology, applications and challenges"),
    "2505.16349": ("method", None, "a modular pipeline for scientific literature summarization"),
    "2506.18096": ("survey", None, "a systematic examination and roadmap of deep research agents"),
    "2506.23485": ("method", None, "thought-augmented planning for interactive recommender agents"),
    "2507.13334": ("survey", None, "a survey of context engineering, with a taxonomy"),
    "2507.19457": ("method", None, "we propose GEPA, a prompt optimizer that outperforms GRPO"),
    "2509.19125": ("method", None, "LLM-guided multi-aspect clustering for taxonomy generation"),
    "2510.04618": ("method", None, "we propose ACE, a framework for evolving contexts"),
    "2512.13564": ("survey", None, "survey of memory in the age of AI agents"),
    "2601.01743": ("survey", None, "architectures, applications, and evaluation of AI agent systems"),
    "2601.04879": ("method", None, "we propose Mind2Report, a cognitive deep research agent"),
    "2601.11868": ("benchmark", None, "we present Terminal-Bench 2.0, a curated hard benchmark of 89 tasks"),
    "2601.20048": ("system", None, "an LLM-based multi-agent system for data insights"),
    "2601.22984": ("benchmark", "evaluation", "we introduce the PING Taxonomy and curate DeepHalluBench; six systems show reliability gaps"),
    "2601.23265": ("method", None, "automating academic illustration for AI scientists"),
    "2602.11988": ("evaluation", None, "we evaluate coding agents' task completion; context files do not generally improve success rates"),
    "2602.12430": ("survey", None, "this survey provides a comprehensive treatment of the agent skills landscape"),
    "2602.20867": ("survey", None, "this paper maps the skill layer and introduces two complementary taxonomies"),
    "2602.23368": ("evaluation", None, "we question how much value vector databases bring; systematic comparison"),
    "2603.20576": ("benchmark", None, "a benchmark for data agents"),
    "2603.22327": ("benchmark", "evaluation", "we introduce AgentSLR, an evaluation harness plus an expert-annotated dataset of 16,248 articles"),
    "2603.25158": ("method", None, "distill trajectory-local lessons into transferable agent skills"),
    "2603.28052": ("method", None, "end-to-end optimization of model harnesses"),
    "2604.08224": ("survey", None, "a unified review of memory, skills, protocols and harness engineering"),
    "2604.16911": ("system", None, "a package manager and registry, implemented as a TypeScript CLI with a registry backend"),
    "2605.05242": ("method", None, "we study direct corpus interaction, searching the raw corpus with terminal tools"),
    "2605.23904": ("method", None, "treats a skill file as a trainable parameter outside a frozen model"),
    "2606.08610": ("system", None, "a harness framework for agentic robot reinforcement learning"),
    "2606.10662": ("method", None, "decentralized multi-agent systems with shared context"),
    "2606.11435": ("survey", None, "in this survey, we systematically examine the landscape of skill evolution"),
    "2606.24775": ("evaluation", None, "we evaluate 12 representative memory systems and two baselines across 11 datasets"),
    "2608.10906": ("benchmark", None, "3.8M SKILL.md files from 282k repos, shipped as one searchable SQLite file"),
    "2608.11888": ("evaluation", None, "differential analysis framework instantiated on existing SkillsBench, yielding 307 failures"),
    "2608.14036": ("evaluation", None, "when do skills help, why do they work, where do they fail; controlled contrastive study"),
    "2609.04298": ("benchmark", "evaluation", "Harbor Adapters port 80+ benchmarks; large-scale evaluation of 8 models across 54 benchmarks"),
}

# filename -> (type, type_secondary | None, evidence). No arXiv record; these are
# classified from the document itself and are the weakest evidence in this file.
BY_FILENAME = {
    "15791445.pdf": ("method", None, "techniques to improve RNN translation performance"),
    "2020-01-0737.pdf": ("method", None, "RL and simulation to develop autonomous vehicle control strategies"),
    "2022-AI-Index-Report_Master.pdf": ("practitioner", None, "annual industry index report"),
    "2022.emnlp-main.388.pdf": ("method", None, "AdaMix: mixture-of-adaptations for parameter-efficient tuning"),
    "Day_1_v3 (1).pdf": ("practitioner", None, "slide deck on the SDLC with vibe coding"),
    "The-Complete-Guide-to-Building-Skill-for-Claude.pdf": ("practitioner", None, "how-to guide"),
    "hermes-kanban-v1-spec (1).pdf": ("practitioner", None, "internal product spec"),
    "the-agentic-sdlc.pdf": ("practitioner", None, "practitioner overview of the agentic SDLC"),
}

ABS = re.compile(r"arxiv\.org/abs/(.+)$")


def key_for(url):
    m = ABS.search(url or "")
    if not m:
        return None
    aid = m.group(1)
    return aid.split("v")[0] if re.match(r"^\d{4}\.", aid) else aid


def lookup(paper):
    """(type, secondary, evidence) for a paper entry, or None."""
    k = key_for(paper.get("url"))
    if k and k in BY_ARXIV:
        return BY_ARXIV[k]
    fn = paper.get("filename")
    if fn and fn in BY_FILENAME:
        return BY_FILENAME[fn]
    return None


def validate():
    """Fail loudly on a typo'd type or a violated two-type cap."""
    for src in (BY_ARXIV, BY_FILENAME):
        for k, (t, s, _) in src.items():
            if t not in VALID:
                sys.exit(f"error: {k}: unknown type {t!r}")
            if s is not None and s not in VALID:
                sys.exit(f"error: {k}: unknown secondary type {s!r}")
            if s == t:
                sys.exit(f"error: {k}: secondary type duplicates primary ({t!r})")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--papers", default="papers.json")
    ap.add_argument("--links", default="links.json")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    validate()
    counts, missing, wrote = Counter(), [], {}

    for path_s in (args.papers, args.links):
        path = Path(path_s)
        if not path.exists():
            print(f"warning: {path} not found, skipping", file=sys.stderr)
            continue
        data = json.loads(path.read_text())
        changed = 0
        for p in data["papers"]:
            hit = lookup(p)
            if not hit:
                missing.append(p.get("filename") or p.get("id") or p.get("title", "?"))
                continue
            t, s, why = hit
            if (p.get("type"), p.get("type_secondary"), p.get("type_evidence")) != (t, s, why):
                p["type"] = t
                p["type_secondary"] = s
                p["type_evidence"] = why
                changed += 1
            counts[t] += 1
        wrote[path] = (data, changed)

    print("\nprimary type counts (per file entry, duplicates included):", file=sys.stderr)
    for t, n in counts.most_common():
        print(f"  {t:13} {n}", file=sys.stderr)
    print(f"  {'TOTAL':13} {sum(counts.values())}", file=sys.stderr)
    sec = sum(1 for src in (BY_ARXIV, BY_FILENAME) for v in src.values() if v[1])
    print(f"\nentries with a secondary type: {sec}", file=sys.stderr)
    if missing:
        print(f"\nNO TYPE ASSIGNED ({len(missing)}):", file=sys.stderr)
        for m in missing:
            print(f"  {m}", file=sys.stderr)

    if args.dry_run:
        print("\n--dry-run: nothing written", file=sys.stderr)
        return
    for path, (data, changed) in wrote.items():
        if changed:
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
            print(f"Wrote {path} ({changed} entries updated)", file=sys.stderr)
        else:
            print(f"{path} already in sync", file=sys.stderr)


if __name__ == "__main__":
    main()
