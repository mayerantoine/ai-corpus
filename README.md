# AI Corpus

78 papers — 65 indexed from PDFs, 13 curated links. Links only; no PDFs are stored in this repo.
Generated 2026-09-13 by [`extract_papers.py`](extract_papers.py) from [`papers.json`](papers.json) and [`links.json`](links.json).

Each entry shows its contribution `type` — see [`paper_types.md`](paper_types.md) for the taxonomy and rubrics.

## Contents

- [Agent Skills](#agent-skills) (11)
- [Prompting & Reasoning](#prompting--reasoning) (11)
- [Agents & Multi-Agent Systems](#agents--multi-agent-systems) (8)
- [Evaluation & Benchmarks](#evaluation--benchmarks) (7)
- [Foundation Models](#foundation-models) (6)
- [Deep Research & Literature Review](#deep-research--literature-review) (5)
- [Fine-tuning & PEFT](#fine-tuning--peft) (5)
- [RAG & Retrieval](#rag--retrieval) (5)
- [Software Engineering with AI](#software-engineering-with-ai) (4)
- [Context Engineering](#context-engineering) (3)
- [Memory](#memory) (3)
- [Mixture-of-Experts](#mixture-of-experts) (2)
- [Surveys](#surveys) (2)
- [Other / Uncategorized](#other--uncategorized) (6)

## By contribution type

What kind of claim each paper makes — independent of the topics above. See [`paper_types.md`](paper_types.md) for the rubric behind each type.

| Type | Papers |
| --- | --- |
| `method` | 32 |
| `survey` | 14 |
| `benchmark` | 9 |
| `evaluation` | 6 |
| `tech-report` | 6 |
| `practitioner` | 5 |
| `empirical` | 3 |
| `system` | 3 |
| **total** | **78** |

5 papers carry a secondary type as well (shown as `primary+secondary`); a paper may have at most two.

## Agent Skills

- **Agent Skills Can Be Harmful: An Empirical Study of Skill-Induced Failures in LLM Agents**
  `evaluation` · Gen Dong, Yanjie Gao, Liqun Li — [arxiv](https://arxiv.org/abs/2608.11888)
  307 skill-induced failures on SkillsBench and SWE-Skills-Bench (125 functional, 182 efficiency); excessive procedural checklists and heavy implementation pipelines cut success rates and inflate cost.
- **Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward**
  `survey` · Renjun Xu, Yang Yan — [arxiv](https://arxiv.org/abs/2602.12430)
  Four-axis survey: architectural foundations (SKILL.md, progressive context loading, MCP integration), skill acquisition, deployment at scale (CUAs, OSWorld), and security frameworks.
- **Demystifying Agent Skills: Why They Work-Until They Don't**
  `evaluation` · Zhiyuan Jiang, Fangrui Huang, Hanwen Xing — [arxiv](https://arxiv.org/abs/2608.14036)
  Contrastive study of 8,135 trial records: skills act as procedural anchors (65.7%) rather than injecting missing facts (4.5%); retrieval precision falls from 29.6% to 3.3% as pools grow 5 to 100.
- **Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering**
  `survey` · Chenyu Zhou, Huacan Chai, Wenteng Chen — [arxiv](https://arxiv.org/abs/2604.08224)
  Examines how externalized artifacts (skills, workflow memory, protocols) substitute or complement internal model weights.
- **GitSkills: A Dataset of Agent Skills on GitHub**
  `benchmark` · Giuseppe Destefanis, Daniel Graziotin, Matteo Vaccargiu, +1 more — [arxiv](https://arxiv.org/abs/2608.10906)
  3,797,117 SKILL.md files from 282,200 public repositories, grouped into 1,877,981 distinct contents, shipped as a single searchable SQLite file.
- **Skill Constellations: Tracing the Supply Chain of Agent Skills on GitHub**
  `benchmark+evaluation` · Fahd Seddik — [arxiv](https://arxiv.org/abs/2610.11169)
  Skill sharing is a supply chain with no registry, versions, or provenance. A few repos are the source of almost all copies and stars do not identify them; copies almost never track their source, so a fix at the source rarely reaches them.
- **SkillAlign: Aligning Skill Interfaces for LLM-based Agents**
  `method` · Shuo Ren, Xiaomian Kang, Jiajun Zhang — [arxiv](https://arxiv.org/abs/2609.07255)
  The same skill can help or mislead depending on how it is exposed: full instructions, hints, summaries, workflows, or none. Exposure form swings ALFWorld success from 47.9% to 72.1%; compact top-k can beat full-library injection.
- **Skilldex: A Package Manager and Registry for Agent Skill Packages with Hierarchical Scope-Based Distribution**
  `system` · Sampriti Saha, Pranav Hemanth — [arxiv](https://arxiv.org/abs/2604.16911)
  Package management and hierarchical scope distribution (global/shared/project) for agent skill artifacts, with format conformance scoring.
- **SkillOpt: Executive Strategy for Self-Evolving Agent Skills**
  `method` · Yifan Yang, Ziyang Gong, Weiquan Huang — [arxiv](https://arxiv.org/abs/2605.23904)
  Treats skill files as trainable parameters outside frozen model weights via bounded text edits, validation gating, and rejected-edit feedback. Often cited by its Microsoft Research blog title, 'Agent Skills as Trainable Parameters'.
- **SoK: Agentic Skills -- Beyond Tool Use in LLM Agents**
  `survey` · Yanna Jiang, Delong Li, Haiyu Deng, +4 more — [arxiv](https://arxiv.org/abs/2602.20867)
  Systematization of knowledge mapping how skills transcend basic function-calling and tool-use paradigms, across the full skill lifecycle.
- **Trace2Skill: Distill Trajectory-Local Lessons into Transferable Agent Skills**
  `method` · Jingwei Ni, Yihao Liu, Xinpeng Liu — [arxiv](https://arxiv.org/abs/2603.25158)
  Turns single-run execution trajectories into reusable, generalized agent skills; harness-agnostic.

## Prompting & Reasoning

- **AUTOMATIC CHAIN OF THOUGHT PROMPTING IN LARGE LANGUAGE MODELS**
  `method` · Zhuosheng Zhang, Aston Zhang, Mu Li, +1 more — [arxiv](https://arxiv.org/abs/2210.03493)
- **Chain-of-Thought Prompting Elicits Reasoning in Large Language Models**
  `method` · Jason Wei, Xuezhi Wang, Dale Schuurmans, +6 more — [arxiv](https://arxiv.org/abs/2201.11903)
- **DSPY: COMPILING DECLARATIVE LANGUAGE MODEL CALLS INTO SELF-IMPROVING PIPELINES**
  `method` · Omar Khattab, Arnav Singhvi, Paridhi Maheshwari, +10 more — [arxiv](https://arxiv.org/abs/2310.03714)
- **GEPA: REFLECTIVE PROMPT EVOLUTION CAN OUTPERFORM REINFORCEMENT LEARNING**
  `method` · Lakshya A Agrawal, Shangyin Tan, Dilara Soylu, +14 more — [arxiv](https://arxiv.org/abs/2507.19457)
- **Large Language Models are Zero-Shot Reasoners**
  `method` · Takeshi Kojima, Shixiang Shane Gu, Machel Reid, +2 more — [arxiv](https://arxiv.org/abs/2205.11916)
- **LARGE LANGUAGE MODELS CAN SELF-IMPROVE**
  `method` · Jiaxin Huang, Shixiang Shane Gu, Le Hou, +4 more — [arxiv](https://arxiv.org/abs/2210.11610)
- **LEAST-TO-MOST PROMPTING ENABLES COMPLEX REASONING IN LARGE LANGUAGE MODELS**
  `method` · Denny Zhou, Nathanael Schärli, Le Hou, +8 more — [arxiv](https://arxiv.org/abs/2205.10625)
- **Meta-Harness: End-to-End Optimization of Model Harnesses**
  `method` · Yoonho Lee, Roshen Nair, Qizheng Zhang, +3 more — [arxiv](https://arxiv.org/abs/2603.28052)
- **MIND YOUR STEP (BY STEP): CHAIN-OF-THOUGHT CAN REDUCE PERFORMANCE ON TASKS WHERE THINKING MAKES HUMANS WORSE**
  `empirical` · Ryan Liu, Jiayi Geng, Addison J. Wu, +3 more — [arxiv](https://arxiv.org/abs/2410.21333)
- **SELF-CONSISTENCY IMPROVES CHAIN OF THOUGHT REASONING IN LANGUAGE MODELS**
  `method` · Xuezhi Wang, Jason Wei, Dale Schuurmans, +5 more — [arxiv](https://arxiv.org/abs/2203.11171)
- **Tree of Thoughts: Deliberate Problem Solving with Large Language Models**
  `method` · Shunyu Yao, Dian Yu, Jeffrey Zhao, +4 more — [arxiv](https://arxiv.org/abs/2305.10601)

## Agents & Multi-Agent Systems

- **A Multi-Agent Conversational Recommender System**
  `method` · Jiabao Fang, Shen Gao, Pengjie Ren, +3 more — [arxiv](https://arxiv.org/abs/2402.01135)
- **Code as Agent Harness**
  `survey` · Xuying Ning, Katherine Tieu, Dongqi Fu, +39 more — [arxiv](https://arxiv.org/abs/2605.18747)
  Frames code as the operational substrate of agent harnesses across three layers (interface, mechanisms, scaling to multi-agent); covers coding assistants, GUI/OS automation, embodied agents, DevOps.
- **HARBOR: A Harness Framework for Agentic Robot Reinforcement Learning**
  `system` · Zechu Li, Yufeng Jin, Xiaoyang Liu, +4 more — [arxiv](https://arxiv.org/abs/2606.08610)
- **Insight Agents: An LLM-Based Multi-Agent System for Data Insights**
  `system` · Jincheng Bai, Zhenyu Zhang, Jennifer Zhang, +1 more — [arxiv](https://arxiv.org/abs/2601.20048)
- **Large Language Model Agent: A Survey on Methodology, Applications and Challenges**
  `survey` · Junyu Luo, Weizhi Zhang, Ye Yuan, +23 more — [arxiv](https://arxiv.org/abs/2503.21460)
- **PaperBanana: Automating Academic Illustration for AI Scientists**
  `method` · Dawei Zhu, Rui Meng, Yale Song, +4 more — [arxiv](https://arxiv.org/abs/2601.23265)
- **Thought-Augmented Planning for LLM-Powered Interactive Recommender Agent**
  `method` · Haocheng Yu, Yaxiong Wu, Hao Wang, +6 more — [arxiv](https://arxiv.org/abs/2506.23485)
- **Using Reinforcement Learning and Simulation to Develop Autonomous Vehicle Control Strategies**
  `method` · _authors not detected_ — [doi](https://doi.org/10.4271/2020-01-0737)

## Evaluation & Benchmarks

- **Agent Skill Evaluation and Evolution: Frameworks and Benchmarks**
  `survey` · Kexin Ding, Yang Zhou, Can Jin — [arxiv](https://arxiv.org/abs/2606.11435)
  Automated, evaluation-driven skill evolution via execution feedback, trajectory distillation, compression, and RL; plus six skill-centric benchmark categories.
- **AI Agent Systems: Architectures, Applications, and Evaluation**
  `survey` · Bin Xu — [arxiv](https://arxiv.org/abs/2601.01743)
- **Can AI Agents Answer Your Data Questions? A Benchmark for Data Agents**
  `benchmark` · Ruiying Ma, Shreya Shankar, Ruiqi Chen, +7 more — [arxiv](https://arxiv.org/abs/2603.20576)
- **Context-Aware Hierarchical Taxonomy Generation for Scientific Papers via LLM-Guided Multi-Aspect Clustering**
  `method` · Kun Zhu, Lizi Liao, Yuxuan Gu, +3 more — [arxiv](https://arxiv.org/abs/2509.19125)
- **Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?**
  `evaluation` · Thibaud Gloaguen, Niels Mündler-Sasahara, Mark Niklas Müller, +2 more — [arxiv](https://arxiv.org/abs/2602.11988)
- **Harbor Adapters and Harbor-Index: Infrastructure and a Curated Meta-Dataset for Large-Scale Agentic Evaluation**
  `benchmark+evaluation` · Lin Shi, Haowei Lin, Zixuan Zhu, +123 more — [arxiv](https://arxiv.org/abs/2609.04298)
- **TERMINAL-BENCH: BENCHMARKING AGENTS ON HARD, REALISTIC TASKS IN COMMAND LINE INTERFACES**
  `benchmark` · Mike A. Merrill, Alexander G. Shaw, Nicholas Carlini, +82 more — [arxiv](https://arxiv.org/abs/2601.11868)

## Foundation Models

- **Apple Intelligence Foundation Language Models**
  `tech-report` · Tom Gunter, Zirui Wang, Chong Wang, +153 more — [arxiv](https://arxiv.org/abs/2407.21075)
- **GPT-4 Technical Report**
  `tech-report` · OpenAI, Josh Achiam, Steven Adler, +278 more — [arxiv](https://arxiv.org/abs/2303.08774)
- **Llama 2: Open Foundation and Fine-Tuned Chat Models**
  `tech-report` · Hugo Touvron, Louis Martin, Kevin Stone, +65 more — [arxiv](https://arxiv.org/abs/2307.09288)
- **LLaMA: Open and Efficient Foundation Language Models**
  `tech-report` · Hugo Touvron, Thibaut Lavril, Gautier Izacard, +11 more — [arxiv](https://arxiv.org/abs/2302.13971)
- **Mistral 7B**
  `tech-report` · Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, +15 more — [arxiv](https://arxiv.org/abs/2310.06825)
- **The Llama 3 Herd of Models**
  `tech-report` · Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, +558 more — [arxiv](https://arxiv.org/abs/2407.21783)

## Deep Research & Literature Review

- **DEEP RESEARCH AGENTS: A SYSTEMATIC EXAMINATION AND ROADMAP**
  `survey` · Yuxuan Huang, Yihang Chen, Haozheng Zhang, +10 more — [arxiv](https://arxiv.org/abs/2506.18096)
- **Evaluating AI-based Scientific Knowledge Synthesis with Epidemiological Systematic Reviews**
  `benchmark+evaluation` · Shreyansh Padarha, Ryan Othniel Kearns, Tristan Naidoo, +13 more — [arxiv](https://arxiv.org/abs/2603.22327)
- **LitLLMs, LLMs for Literature Review: Are we there yet?**
  `method` · Shubham Agarwal, Gaurav Sahu, Abhay Puri, +5 more — [arxiv](https://arxiv.org/abs/2412.15249)
- **Mind2Report: Expert-Level Commercial Report Synthesis via Cognitive Deep Research Agent**
  `method` · Mingyue Cheng, Daoyu Wang, Qi Liu, +7 more — [arxiv](https://arxiv.org/abs/2601.04879)
- **Why Your Deep Research Agent Fails? On Hallucination Evaluation in Full Research Trajectory**
  `benchmark+evaluation` · Yuhao Zhan, Tianyu Fan, Linxuan Huang, +2 more — [arxiv](https://arxiv.org/abs/2601.22984)

## Fine-tuning & PEFT

- **AdaMix: Mixture-of-Adaptations for Parameter-efficient Model Tuning**
  `method` · Yaqing Wang, Sahaj Agarwal, Subhabrata Mukherjee — [link](https://aclanthology.org/2022.emnlp-main.388/)
- **LARGE LANGUAGE MODELS ARE HUMAN-LEVEL PROMPT ENGINEERS**
  `method` · Yongchao Zhou, Andrei Ioan Muresanu, Ziwen Han, +4 more — [arxiv](https://arxiv.org/abs/2211.01910)
- **LORA: LOW-RANK ADAPTATION OF LARGE LANGUAGE MODELS**
  `method` · Edward J. Hu, Yelong Shen, Phillip Wallis, +5 more — [arxiv](https://arxiv.org/abs/2106.09685)
- **P-Tuning v2: Prompt Tuning Can Be Comparable to Fine-tuning Universally Across Scales and Tasks**
  `method` · Xiao Liu, Kaixuan Ji, Yicheng Fu, +4 more — [arxiv](https://arxiv.org/abs/2110.07602)
- **QLORA: Efficient Finetuning of Quantized LLMs**
  `method` · Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, +1 more — [arxiv](https://arxiv.org/abs/2305.14314)

## RAG & Retrieval

- **Ask, Retrieve, Summarize: A Modular Pipeline for Scientific Literature Summarization**
  `method` · Pierre Achkar, Tim Gollub, Martin Potthast — [arxiv](https://arxiv.org/abs/2505.16349)
- **Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via Direct Corpus Interaction**
  `method` · Zhuofeng Li, Haoxiang Zhang, Cong Wei, +16 more — [arxiv](https://arxiv.org/abs/2605.05242)
- **Keyword search is all you need: Achieving RAG-Level Performance without vector databases using agentic tool use**
  `evaluation` · Shreyas Subramanian, Adewale Akinfaderin, Yanyan Zhang, +4 more — [arxiv](https://arxiv.org/abs/2602.23368)
- **Know Your RAG: Dataset Taxonomy and Generation Strategies for Evaluating RAG Systems**
  `benchmark` · Rafael Teixeira de Lima, Shubham Gupta, Cesar Berrospi, +4 more — [arxiv](https://arxiv.org/abs/2411.19710)
- **Language agents achieve superhuman synthesis of scientific knowledge**
  `evaluation` · Michael D. Skarlinski, Sam Cox, Jon M. Laurent, +6 more — [arxiv](https://arxiv.org/abs/2409.13740)

## Software Engineering with AI

- **Agentic SDLC**
  `practitioner` · _authors not detected_ — [search](https://www.semanticscholar.org/search?q=Agentic+SDLC)
- **Hermes Kanban** ⚠️
  `practitioner` · _authors not detected_ — [search](https://www.semanticscholar.org/search?q=Hermes+Kanban)
- **The Complete Guide to Building Skills for Claude**
  `practitioner` · _authors not detected_ — [search](https://www.semanticscholar.org/search?q=The+Complete+Guide+to+Building+Skills+for+Claude)
- **The New SDLC With Vibe Coding F rom ad-hoc prompting to Agentic Engineering**
  `practitioner` · Addy Osmani, Shubham Saboo, Sokratis Kartakis — [search](https://www.semanticscholar.org/search?q=The+New+SDLC+With+Vibe+Coding+F+rom+ad-hoc+prompting+to+Agentic+Engineering)

## Context Engineering

- **A Survey of Context Engineering for Large Language Models**
  `survey` · Lingrui Mei, Jiayu Yao, Yuyao Ge, +12 more — [arxiv](https://arxiv.org/abs/2507.13334)
- **AGENTIC CONTEXT ENGINEERING: EVOLVING CONTEXTS FOR SELF-IMPROVING LANGUAGE MODELS**
  `method` · Qizheng Zhang, Changran Hu, Shubhangi Upasani, +10 more — [arxiv](https://arxiv.org/abs/2510.04618)
- **Decentralized Multi-Agent Systems with Shared Context**
  `method` · Yuzhen Mao, Jerry Gu, Aadi Chauhan, +3 more — [arxiv](https://arxiv.org/abs/2606.10662)

## Memory

- **A Survey on the Memory Mechanism of Large Language Model based Agents**
  `survey` · Zeyu Zhang, Xiaohe Bo, Chen Ma, +6 more — [arxiv](https://arxiv.org/abs/2404.13501)
- **Are We Ready For An Agent-Native Memory System?**
  `evaluation` · Wei Zhou, Xuanhe Zhou, Shaokun Han, +5 more — [arxiv](https://arxiv.org/abs/2606.24775)
- **Memory in the Age of AI Agents: A Survey**
  `survey` · Yuyang Hu, Shichun Liu, Yanwei Yue, +44 more — [arxiv](https://arxiv.org/abs/2512.13564)

## Mixture-of-Experts

- **OUTRAGEOUSLY LARGE NEURAL NETWORKS: THE SPARSELY-GATED MIXTURE-OF-EXPERTS LAYER**
  `method` · Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, +4 more — [arxiv](https://arxiv.org/abs/1701.06538)
- **Towards Understanding Mixture of Experts in Deep Learning**
  `empirical` · Zixiang Chen, Yihe Deng, Yue Wu, +2 more — [arxiv](https://arxiv.org/abs/2208.02813)

## Surveys

- **A Survey on Efficient Training of Transformers**
  `survey` · Bohan Zhuang, Jing Liu, Zizheng Pan, +3 more — [arxiv](https://arxiv.org/abs/2302.01107)
- **An Overview of Multi-Task Learning in Deep Neural Networks∗**
  `survey` · Sebastian Ruder — [arxiv](https://arxiv.org/abs/1706.05098)

## Other / Uncategorized

- **Artificial Intelligence Index Report 2022**
  `practitioner` · _authors not detected_ — [link](https://hai.stanford.edu/ai-index/2022-ai-index-report)
- **EUREKA: HUMAN-LEVEL REWARD DESIGN VIA CODING LARGE LANGUAGE MODELS**
  `method` · Yecheng Jason Ma, William Liang, Guanzhi Wang, +6 more — [arxiv](https://arxiv.org/abs/2310.12931)
- **Exploring techniques to improve RNN translation performance**
  `method` · Patrick Kelly — [search](https://www.semanticscholar.org/search?q=Exploring+techniques+to+improve+RNN+translation+performance)
- **Neural Network Acceptability Judgments**
  `benchmark+evaluation` · Alex Warstadt, Amanpreet Singh, Samuel R. Bowman — [arxiv](https://arxiv.org/abs/1805.12471)
- **Understanding and Improving Sequence-to-Sequence Pretraining for Neural Machine Translation**
  `empirical` · Wenxuan Wang, Wenxiang Jiao, Yongchang Hao, +4 more — [arxiv](https://arxiv.org/abs/2203.08442)
- **Understanding Random Forests: From Theory to Practice**
  `survey` · Gilles Louppe — [arxiv](https://arxiv.org/abs/1407.7502)

## Needs Review

Heuristic extraction was uncertain for these. Fix the entry in `papers.json`, set `"manually_edited": true` so it is preserved on re-run, then regenerate this file.

| File | Extracted title | Flags |
| --- | --- | --- |
| `hermes-kanban-v1-spec (1).pdf` | Hermes Kanban | no-authors |
