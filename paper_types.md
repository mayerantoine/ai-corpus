# Paper Types

A classification of **what kind of claim a paper makes** — orthogonal to the
subject-matter topics in [`papers.json`](papers.json), which classify *what a paper is
about*. GEPA is a **method** paper about prompting; a survey of prompt optimizers would
share its topic but not its type.

Why bother: the type tells you how a paper can fail, and therefore how to read it.
A method paper fails if its baselines were weak. An evaluation fails if its setup was
confounded. A benchmark fails if its tasks don't represent the real distribution.
Knowing the type tells you where to aim your skepticism.

## Classify from the abstract, never the title

**This is a rule, not a suggestion.** Titles systematically mislead about contribution
type, and this corpus is full of examples:

| Title suggests | Abstract says | Actual type |
| --- | --- | --- |
| *Why Your Deep Research Agent Fails?* — a failure study | "we introduce the PING Taxonomy ... curate DeepHalluBench" | `benchmark` |
| *Evaluating AGENTS.md* — an evaluation harness | measures existing agents on SWE-bench; releases nothing | `evaluation` |
| *Agent Skill Evaluation and Evolution: Frameworks and Benchmarks* | "**In this survey**, we systematically examine..." | `survey` |
| *Are We Ready For An Agent-Native Memory System?* — a position piece | "we evaluate 12 representative memory systems across 11 datasets" | `evaluation` |
| *Keyword search is all you need* — a method claim | "we question how much value ... systematic comparison" | `evaluation` |
| *Agent Skills Can Be Harmful: An Empirical Study* | differential framework instantiated on *existing* SkillsBench | `evaluation` |
| *Language agents achieve superhuman synthesis* — a result | "we developed a rigorous human-AI comparison methodology" | `evaluation` |

The decisive questions are all answered in the abstract, not the title:

1. **Does it release a reusable artifact?** → `benchmark` or `system`
2. **Does it propose a named technique and beat baselines?** → `method`
3. **Does it say "in this survey/review" or impose a taxonomy on others' work?** → `survey`
4. **Does it assess how well systems or practices perform?** → `evaluation`
5. **Does it explain a mechanism without grading anything?** → `empirical`

## The types

| Type | One-line test | Count here |
| --- | --- | --- |
| [`method`](#method) | Could I implement the thing it proposes? | 32 |
| [`survey`](#survey) | Does it organize others' work rather than add its own? | 14 |
| [`benchmark`](#benchmark) | Does it ship something others will measure against? | 9 |
| [`evaluation`](#evaluation) | Does it assess how well systems/practices perform? | 6 |
| [`tech-report`](#tech-report) | Is it an artifact disclosure from whoever built it? | 6 |
| [`practitioner`](#practitioner) | Is it a guide/spec rather than a research paper? | 5 |
| [`empirical`](#empirical) | Does it explain a mechanism, grading nothing? | 3 |
| [`system`](#system) | Is the contribution a thing you install? | 3 |

Counts cover all 78 papers and sum to 78, each assigned one primary type from its
abstract. A paper may carry **at most two types** — one primary, one optional secondary
— see [Hybrids](#hybrids).

---

### `method`

**Claim:** "Here is a new technique, and it outperforms the alternatives."

A named mechanism plus experiments against baselines. The lasting contribution is
reusable: after reading, you could implement it.

**Rubric — expect all of:**
- [ ] Abstract contains "we propose / we introduce / we present" + a named thing
- [ ] Positions against a baseline class
- [ ] Reports experiments where the proposed thing wins
- [ ] Ablations isolating which component does the work

**Reads as method but isn't:** a paper naming a *dataset* or *harness* rather than a
technique — that's `benchmark` or `system`.

**How it fails:** weak or stale baselines; wins that vanish under tuning parity;
ablations that don't isolate the mechanism.

**In this corpus (32):** GEPA, LoRA, QLoRA, Chain-of-Thought, Tree of Thoughts, DSPy,
Self-Consistency, Least-to-Most, Auto-CoT, Zero-Shot Reasoners, LLMs Can Self-Improve,
APE (*Human-Level Prompt Engineers*), AdaMix, P-Tuning v2, Sparsely-Gated MoE, SkillOpt,
Trace2Skill, Mind2Report, Eureka, Meta-Harness, ACE (*Agentic Context Engineering*),
Decentralized Multi-Agent Systems with Shared Context, Beyond Semantic Similarity (DCI),
Ask/Retrieve/Summarize, Context-Aware Hierarchical Taxonomy Generation, LitLLMs,
Multi-Agent Conversational Recommender, Thought-Augmented Planning, PaperBanana,
RNN translation techniques, RL for autonomous vehicle control, SkillAlign

Note *LitLLMs, Are we there yet?* lands here despite its question-title: the abstract
introduces "a novel two-step search strategy" and a re-ranking mechanism.

---

### `survey`

**Claim:** "Here is the landscape, organized."

Contributes a taxonomy and a map of existing work. You finish knowing the field's shape,
with nothing new to implement.

**Rubric — expect most of:**
- [ ] Abstract self-identifies: "in this survey", "this review", "we survey"
- [ ] Taxonomy or axes imposed on prior work
- [ ] Broad citation coverage over a defined scope
- [ ] No new technique evaluated against baselines

**Variant — `sok` (Systematization of Knowledge):** re-derives the framing rather than
cataloging, usually in security venues. Tagged `survey` here; it's a stronger claim,
since the organizing argument *is* the contribution.

**How it fails:** a taxonomy whose categories don't carve reality; coverage that stops
at the authors' subfield; staleness.

**In this corpus (14):** *A Survey of Context Engineering*, *Deep Research Agents: A
Systematic Examination and Roadmap*, *Agent Skills for LLMs*, *Externalization in LLM
Agents*, *Memory in the Age of AI Agents*, *A Survey on the Memory Mechanism of
LLM-based Agents*, *LLM Agent: A Survey on Methodology*, *A Survey on Efficient Training
of Transformers*, *An Overview of Multi-Task Learning*, *AI Agent Systems:
Architectures, Applications, and Evaluation*, *Understanding Random Forests*,
*Agent Skill Evaluation and Evolution*, *SoK: Agentic Skills*, *Code as Agent Harness*

---

### `benchmark`

**Claim:** "Here is how to measure this, plus the measuring stick."

The lasting contribution is the artifact others evaluate *against*. Nearly always ships
baseline results too, but those age while the benchmark persists.

**Rubric — expect all of:**
- [ ] A **named, releasable** task set / dataset / metric / harness
- [ ] Documented construction and validation
- [ ] Multiple existing systems scored on it
- [ ] Intended for reuse by others, not just this paper

**The dividing line with `evaluation`:** does the paper *build* the measuring stick, or
measure with someone else's? This is the single question that separates them, and it is
answerable only from the abstract. *Why Your Deep Research Agent Fails?* curates
DeepHalluBench → `benchmark`. *Agent Skills Can Be Harmful* instantiates its framework
on existing SkillsBench → `evaluation`.

**How it fails:** tasks unrepresentative of real use; saturation; training-data
contamination; metrics that reward the wrong thing.

**In this corpus (9):** Terminal-Bench, DAB, GitSkills, *Why Your Deep Research Agent
Fails?* (DeepHalluBench + PING), *Know Your RAG*, Harbor-Index, AgentSLR
(*Evaluating AI-based Scientific Knowledge Synthesis*), CoLA (*Neural Network
Acceptability Judgments*), Skill Constellations

---

### `evaluation`

**Claim:** "Here is how well existing systems or practices actually perform."

An assessment study. The goal is to *grade* something — a system, a tool, a widespread
practice — against a question, using benchmarks and harnesses that mostly already exist.
Verdicts are frequently negative, which is much of their value.

**Rubric — expect all of:**
- [ ] A question of the form "does X actually work / how well?"
- [ ] Named existing systems or practices as the subject under test
- [ ] Measurement on existing benchmarks, or a purpose-built setup not pitched for reuse
- [ ] A verdict, often deflationary

**Distinguish from `benchmark`:** no reusable measuring stick is the deliverable.
**Distinguish from `empirical`:** the object is a *system or practice being graded*, not
a mechanism being explained.

**How it fails:** confounds; too few systems to generalize; a setup that quietly
advantages one condition; conclusions overreaching the measurement.

**In this corpus (6):** *Evaluating AGENTS.md*, *Demystifying Agent Skills*, *Agent
Skills Can Be Harmful*, *Are We Ready For An Agent-Native Memory System?*, *Keyword
search is all you need*, PaperQA2 (*Language agents achieve superhuman synthesis*)

---

### `empirical`

**Claim:** "Here is why this works, mechanistically."

Measures or analyzes to *explain* a phenomenon. Grades no system and proposes no
technique. Often paired with theory.

**Rubric — expect all of:**
- [ ] A why/how question about a mechanism
- [ ] Controlled experiments or formal analysis isolating a cause
- [ ] No named technique offered for adoption
- [ ] No pass/fail verdict on a named system

**Includes negative results about mechanisms:** *Mind Your Step* shows CoT *hurts* on
tasks where human deliberation hurts — a claim about when a mechanism misfires, not a
grade on any product.

**How it fails:** a setup too narrow to generalize; confounds; theory whose assumptions
don't hold at real scale.

**In this corpus (3):** *Towards Understanding Mixture of Experts*, *Mind Your Step (by
Step)*, *Understanding and Improving Seq2Seq Pretraining for NMT*

---

### `tech-report`

**Claim:** "Here is what we built." Artifact disclosure, typically industrial.

Describes a shipped model. Structured as disclosure rather than hypothesis testing: no
controlled comparison of design alternatives, and often deliberate omissions about data.

**Rubric — expect most of:**
- [ ] Authored by the team that built it (frequently hundreds of authors)
- [ ] Describes scale, training, and evals for one specific system
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
- [ ] Architecture and interface in implementable detail
- [ ] Evaluated on usability/coverage/throughput, not only accuracy
- [ ] Usually open-sourced

**Distinguishing from `method`:** a method's contribution survives as an *idea* you
reimplement; a system's survives as a *thing you install*.

**In this corpus (3):** Skilldex, HARBOR, Insight Agents

---

### `practitioner`

**Claim:** "Here is how to do this." Guides, specs, slide decks, industry reports.

Not research papers — no novelty claim, no peer review. Worth keeping and worth
labeling honestly, so they aren't read as evidence.

**Rubric:**
- [ ] Instructional, normative, or descriptive-of-practice
- [ ] No novelty claim, no systematic evaluation
- [ ] Often no arXiv/DOI identifier and no author list
- [ ] Vendor, consultancy, or internal provenance

**In this corpus (5):** *The Complete Guide to Building Skills for Claude*, *Hermes
Kanban*, *Agentic SDLC*, *The New SDLC With Vibe Coding*, *AI Index Report 2022*

---

## Hybrids

These are soft categories and overlap is normal. Three rules keep it usable:

1. **Maximum two types per paper — a hard cap.** One primary, at most one secondary.
   A paper needing three labels has been read too generously: go back to rule 2 and
   pick what actually survives. The cap is what keeps the taxonomy a classification
   rather than a tag cloud, and it is what makes counts add up to the corpus size.
2. **Assign the primary type by what survives.** In two years, what will others cite
   this for? A method paper that builds a small benchmark to prove its point is still
   `method`.
3. **Add a secondary type only when the hybrid is genuine** — when dropping it would
   lose something a reader needs. *Why Your Deep Research Agent Fails?* is `benchmark`
   + `evaluation`: it ships DeepHalluBench and PING *and* grades six systems with them.
   Most papers need no secondary type at all; reach for one only when the primary label
   alone would mislead.

Common legitimate pairs:

| Pair | Why it happens |
| --- | --- |
| `benchmark` + `evaluation` | Shipping the stick and the first reading from it |
| `method` + `benchmark` | New technique needs a new way to measure it |
| `survey` + `evaluation` | A map plus a scorecard of what's on it |
| `system` + `benchmark` | Infrastructure plus a meta-dataset (Harbor-Index) |
| `evaluation` + `empirical` | A grade plus an explanation of the cause |

**No `position` papers.** The taxonomy previously had one, *Are We Ready For An
Agent-Native Memory System?*, assigned from its provocation-style title. Its abstract
says it "evaluate[s] 12 representative memory systems and two reference baselines across
five benchmark workloads spanning 11 datasets" — an `evaluation`. The category is kept
out until a paper actually earns it, which is itself a demonstration of the
abstract-over-title rule.

## Applying this

Encoded in the data. Every entry in [`papers.json`](papers.json) and
[`links.json`](links.json) carries three fields:

```json
"type": "benchmark",
"type_secondary": "evaluation",
"type_evidence": "we introduce the PING Taxonomy and curate DeepHalluBench; six systems show reliability gaps"
```

`type_secondary` is `null` for the 73 papers that need only one label.
`type_evidence` quotes the abstract phrase the assignment rests on, so any
classification can be audited without re-reading the paper.

[`apply_types.py`](apply_types.py) owns the assignments and writes both files
(`--dry-run` to preview; idempotent). It validates on every run that each type is
one of the eight, and that no secondary duplicates its primary or pushes a paper
past the two-type cap.

The two axes stay independent: unlike `topic`, which `extract_papers.py` derives
from title keywords, `type` **cannot** be derived that way — the table at the top
of this file is the evidence, since the title-based guess was wrong for seven
papers here. New papers therefore need a row added to `apply_types.py` by hand,
after reading the abstract.
