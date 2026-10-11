# Paper Types

A classification of **what kind of claim a paper makes** — orthogonal to the
subject-matter topics in [`papers.json`](papers.json), which classify *what a paper is
about*. GEPA is a **method** paper about prompting; a survey of prompt optimizers would
share its topic but not its type.

Why bother: the type tells you how a paper can fail, and therefore how to read it.
A method paper fails if its baselines were weak. An empirical paper fails if its
measurement was confounded. A benchmark fails if its tasks don't represent the real
distribution. Knowing the type tells you where to aim your skepticism.

## The types

Ordered by how often they appear in this corpus.

| Type | One-line test | Count here |
| --- | --- | --- |
| [`method`](#method) | Could I implement the thing it proposes? | 32 |
| [`survey`](#survey) | Does it organize others' work rather than add its own? | 12 |
| [`benchmark`](#benchmark) | Does it ship something others will measure against? | 9 |
| [`empirical`](#empirical) | Does it report findings but propose no technique? | 6 |
| [`tech-report`](#tech-report) | Is it an artifact disclosure from whoever built it? | 6 |
| [`practitioner`](#practitioner) | Is it a guide/spec rather than a research paper? | 5 |
| [`system`](#system) | Is the contribution a working, usable artifact? | 4 |
| [`position`](#position) | Is it an argument about what the field should do? | 1 |

Counts cover all 75 papers in the corpus and sum to 75 — each assigned its single
primary type. Where a paper is a genuine hybrid, the primary type is the one that
survives; see [Hybrids](#hybrids).

---

### `method`

**Claim:** "Here is a new technique, and it outperforms the alternatives."

A named mechanism plus experiments against baselines. The lasting contribution is
something reusable: after reading, you could implement it.

**Rubric — expect all of:**
- [ ] Names its contribution so others can cite it ("GEPA", "LoRA", "Tree of Thoughts")
- [ ] Positions against a baseline class, often in the title
- [ ] Reports experiments where the proposed thing wins
- [ ] Ablations isolating which component does the work

**Reads as method but isn't:** a paper naming a *dataset* or *harness* rather than a
technique — that's `benchmark` or `system`.

**How it fails:** weak or stale baselines; wins that vanish under tuning parity;
ablations that don't actually isolate the mechanism.

**In this corpus (32):** GEPA, LoRA, QLoRA, Chain-of-Thought, Tree of Thoughts, DSPy,
Self-Consistency, Least-to-Most, Auto-CoT, Zero-Shot Reasoners, LLMs Can Self-Improve,
Human-Level Prompt Engineers, AdaMix, P-Tuning v2, Sparsely-Gated MoE, SkillOpt,
Trace2Skill, Mind2Report, Eureka, Meta-Harness, Agentic Context Engineering,
Decentralized Multi-Agent Systems with Shared Context, Beyond Semantic Similarity,
Keyword Search Is All You Need, Ask/Retrieve/Summarize, PaperQA2 (*Language agents
achieve superhuman synthesis*), Context-Aware Hierarchical Taxonomy Generation,
Multi-Agent Conversational Recommender, Thought-Augmented Planning, seq2seq
pretraining for NMT, RNN translation techniques, RL for autonomous vehicle control

---

### `survey`

**Claim:** "Here is the landscape, organized."

Contributes a taxonomy and a map of existing work. You finish knowing the field's
shape, with nothing new to implement.

**Rubric — expect most of:**
- [ ] Taxonomy or axes imposed on prior work
- [ ] Broad citation coverage over a defined scope
- [ ] No new technique evaluated against baselines
- [ ] Often an explicit "open problems" or roadmap section

**Variant — `sok` (Systematization of Knowledge):** re-derives the framing rather than
cataloging, usually in security venues. Tag as `survey` unless the venue's own label
matters to you; it's a stronger claim than a survey, since the organizing argument *is*
the contribution.

**How it fails:** a taxonomy whose categories don't carve reality (everything lands in
one bucket); coverage that silently stops at the authors' subfield; staleness.

**In this corpus (12):** *A Survey of Context Engineering*, *Deep Research Agents: A
Systematic Examination and Roadmap*, *Agent Skills for LLMs*, *Externalization in LLM
Agents*, *Memory in the Age of AI Agents: A Survey*, *A Survey on the Memory Mechanism
of LLM-based Agents*, *LLM Agent: A Survey on Methodology*, *A Survey on Efficient
Training of Transformers*, *An Overview of Multi-Task Learning*, *AI Agent Systems:
Architectures, Applications, and Evaluation*, *Understanding Random Forests*,
*SoK: Agentic Skills*

---

### `benchmark`

**Claim:** "Here is how to measure this, plus the measuring stick."

The lasting contribution is the artifact others evaluate *against*. Nearly always ships
baseline results too, but those age while the benchmark persists.

**Rubric — expect all of:**
- [ ] A named, releasable task set / dataset / metric
- [ ] Documented construction and validation of the tasks
- [ ] Multiple existing systems scored on it
- [ ] Intended for reuse by others, not just this paper

**Distinguishing from `empirical`:** does the paper *build* the measuring stick, or
measure with someone else's? *Agent Skills Can Be Harmful* analyzes 307 failures but
evaluates on existing SkillsBench — that's `empirical`. *Why Your Deep Research Agent
Fails?* builds DeepHalluBench — that's `benchmark`.

**How it fails:** tasks unrepresentative of real use; saturation; contamination from
training data; metrics that reward the wrong thing.

**In this corpus (9):** Terminal-Bench, DAB (*Can AI Agents Answer Your Data
Questions?*), GitSkills, *Why Your Deep Research Agent Fails?*, *Know Your RAG*,
*Agent Skill Evaluation and Evolution*, Harbor-Index, *Neural Network Acceptability
Judgments* (CoLA), *Evaluating AI-based Scientific Knowledge Synthesis*

---

### `empirical`

**Claim:** "Here is what is actually true, measured."

No new technique. The contribution is a *finding* — often a surprising or deflationary
one. These are the papers that change how you use methods you already have.

**Rubric — expect all of:**
- [ ] A question about reality, not a proposed solution
- [ ] Controlled comparison or systematic measurement
- [ ] Headline result stated as a quantity or rate
- [ ] Introduces no named technique for others to adopt

**Includes negative / replication results:** "the claimed effect doesn't hold as
stated" is an empirical claim. *Mind Your Step* — showing CoT *hurts* on some tasks —
belongs here despite sitting in a prompting topic.

**How it fails:** confounds; a setup too narrow to generalize; cherry-picked task
selection; conclusions overreaching the measurement.

**In this corpus (6):** *Demystifying Agent Skills*, *Agent Skills Can Be Harmful*,
*Evaluating AGENTS.md*, *Mind Your Step (by Step)*, *LitLLMs: Are we there yet?*,
*Towards Understanding Mixture of Experts*

---

### `tech-report`

**Claim:** "Here is what we built." Artifact disclosure, typically industrial.

Describes a shipped model or system. Structured as disclosure rather than hypothesis
testing: no controlled comparison against alternatives, and often deliberate omissions
about data or training.

**Rubric — expect most of:**
- [ ] Authored by the team that built the artifact (often very many authors)
- [ ] Describes scale, training, and eval results for one specific system
- [ ] No ablation of design choices against alternatives
- [ ] Evaluation is a scorecard, not a hypothesis test

**How it fails:** unreproducible by construction; selective evals; undisclosed data
makes contamination unassessable. Read as evidence of capability, not as science.

**In this corpus (6):** GPT-4 Technical Report, Llama 2, LLaMA, The Llama 3 Herd of
Models, Mistral 7B, Apple Intelligence Foundation Language Models

---

### `system`

**Claim:** "Here is working infrastructure others can run."

Engineering contribution — the artifact is the point, and its value is adoption rather
than a benchmark delta.

**Rubric — expect most of:**
- [ ] A runnable tool, framework, registry, or pipeline
- [ ] Architecture and interface described in implementable detail
- [ ] Evaluated on usability/coverage/throughput, not only accuracy
- [ ] Usually open-sourced

**Distinguishing from `method`:** a method's contribution survives as an *idea* you can
reimplement; a system's survives as a *thing you install*.

**In this corpus (4):** Skilldex, HARBOR, Insight Agents, PaperBanana

---

### `position`

**Claim:** "The field should think about this differently."

Argument rather than experiment. Legitimate and useful, but evidence is rhetorical and
illustrative, not systematic.

**Rubric:**
- [ ] A thesis about what research or practice *ought* to do
- [ ] Reasoning and selected examples carry the argument
- [ ] No systematic evaluation, and none claimed
- [ ] Often titled as a question or provocation

**How it fails:** unfalsifiable; strawmans the status quo; mistakes a preference for a
finding.

**In this corpus (1):** *Are We Ready For An Agent-Native Memory System?* (the title's
question is the thesis)

---

### `practitioner`

**Claim:** "Here is how to do this." Guides, specs, slide decks, industry reports.

Not research papers at all — no claim of novelty and no peer review. Worth keeping and
worth labeling honestly, so they aren't read as evidence.

**Rubric:**
- [ ] Instructional, normative, or descriptive-of-practice
- [ ] No novelty claim, no systematic evaluation
- [ ] Often no arXiv/DOI identifier and no author list
- [ ] Vendor, consultancy, or internal provenance

**In this corpus (5):** *The Complete Guide to Building Skills for Claude*, *Hermes
Kanban*, *Agentic SDLC*, *The New SDLC With Vibe Coding*, *AI Index Report 2022*

---

## Hybrids

These are soft categories and overlap is normal. Two rules keep it usable:

1. **Assign the primary type by what survives.** Ask: in two years, what will others
   cite this for? A method paper that builds a small benchmark to prove its point is
   still `method`. A benchmark paper that reports findings is still `benchmark`.
2. **Allow one secondary type when the hybrid is genuine.** *Why Your Deep Research
   Agent Fails?* is `benchmark` + `empirical`: it ships DeepHalluBench and the PING
   taxonomy *and* reports reliability gaps across six systems. Calling it either alone
   loses something real.

Common legitimate pairs:

| Pair | Why it happens |
| --- | --- |
| `method` + `benchmark` | New technique needs a new way to measure it |
| `benchmark` + `empirical` | Shipping the stick and the first reading from it |
| `survey` + `position` | A map that argues for where the field should go |
| `system` + `benchmark` | Infrastructure plus a meta-dataset (e.g. Harbor-Index) |

**Titles mislead.** *"Why Your Deep Research Agent Fails?"* reads as pure `empirical`;
the subtitle *"On Hallucination Evaluation..."* reveals the benchmark. Classify from the
abstract's stated contributions, not the title — and note that this corpus's titles were
truncated by PDF extraction until they were synced from the arXiv API
([`sync_arxiv.py`](sync_arxiv.py)).

## Applying this

Not yet encoded in the data. To add it, a `type` field (and optional `type_secondary`)
alongside `topic` in both [`papers.json`](papers.json) and
[`links.json`](links.json) — the two axes are independent, so `type` cannot be derived
from `topic` by keyword rules the way `topic` is derived from titles. Classification
needs the abstract, so it is a per-paper judgment, not a regex.
