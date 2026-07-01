# PROJECT-detail.md — Pregnancy / Prenatal Care Support (weekly)

## Executive Summary
`prenatal-care-support` is a Claude Skill in the **Health, Wellness & Psychology** cluster (idea #86). It acts as a prenatal health-education guide grounded in obstetric evidence (psychoeducational, NOT a substitute for an obstetrician/midwife). It runs a research-first, evidence-graded harness that profiles the input, selects named world-renowned frameworks, scores the subject across 6 dimensions, challenges its own conclusions, and emits a professional deliverable with a prioritized improvement roadmap.

## Problem Statement
Expectant parents lack structured, trustworthy week-by-week guidance and miss warning signs. This skill provides week-specific education, screens for danger signs, and always routes risk to clinical care.

Domain context: practitioners in health, wellness & psychology need decisions grounded in citable, current methodology rather than ad-hoc opinion. This skill enforces the evidence hierarchy (Systematic Review > Meta-Analysis > RCT > Cohort > Expert Opinion > Blog) and keeps its knowledge current through a weekly crawl.

## Target Users & Use Cases
- **Trigger example A:** User says *"Evaluate / score / optimize my pregnancy / prenatal care support"* → skill runs the full harness and returns a scored report + roadmap.
- **Trigger example B:** User provides an artifact (document, dataset, design, plan) → skill audits it against the frameworks below.
- **Trigger example C:** User asks *"What should I improve first?"* → skill returns the impact/effort-ranked roadmap section only.

## Harness Architecture
```
USER INPUT
   |
   v
[Stage 1] sub-profile-intake  --> scoped profile / context
   |
   v
[Stage 2] sub-safety-screener  --> selected frameworks (WHO antenatal care (ANC) guidelines, ...)
   |
   v
[Stage 3] RESEARCH (WebSearch/WebFetch) --> evidence pack  (fallback: SECOND-KNOWLEDGE-BRAIN.md)
   |
   v
[Stage 4] sub-framework-selector  --> 6-dimension score
   |
   v
[Stage 5] sub-improvement-roadmap  --> challenge / validation
   |
   v
[SAFETY GATE] sub-safety-screener --> escalate red flags BEFORE advice
   |
   v
[Stage 6] MAIN HARNESS --> final deliverable (score table + prioritized roadmap)
```

## Full Sub-Skill Catalog

### sub-profile-intake
- **Purpose:** Capture gestational week, history and risk factors with a clear non-clinical disclaimer.
- **Inputs:** scoped context from prior stage + user artifact
- **Outputs:** structured findings passed to the next stage
- **Tools used:** Read, WebSearch, WebFetch, Write
- **Quality gate:** output must be evidence-linked and complete before the harness advances

### sub-safety-screener
- **Purpose:** Screen for obstetric danger signs FIRST and route urgent symptoms to emergency/clinical care.
- **Inputs:** scoped context from prior stage + user artifact
- **Outputs:** structured findings passed to the next stage
- **Tools used:** Read, WebSearch, WebFetch, Write
- **Quality gate:** output must be evidence-linked and complete before the harness advances

### sub-framework-selector
- **Purpose:** Apply WHO/ACOG week-specific ANC guidance and validated screens (EPDS).
- **Inputs:** scoped context from prior stage + user artifact
- **Outputs:** structured findings passed to the next stage
- **Tools used:** Read, WebSearch, WebFetch, Write
- **Quality gate:** output must be evidence-linked and complete before the harness advances

### sub-improvement-roadmap
- **Purpose:** Provide a week-by-week education and care-schedule plan with clinical-visit triggers.
- **Inputs:** scoped context from prior stage + user artifact
- **Outputs:** structured findings passed to the next stage
- **Tools used:** Read, WebSearch, WebFetch, Write
- **Quality gate:** output must be evidence-linked and complete before the harness advances

## Skill File Format Specification
Frontmatter schema (all skill files):
```yaml
---
name: prenatal-care-support            # or sub-<name>
description: <one-line summary shown in /help>
---
```
Required sections in `main.md`: Role & Persona, Workflow (Harness Flow), Sub-skills Available, Tools, Output Format, Quality Gates.

## E2E Execution Flow
1. Parse user request and artifact; if ambiguous, ask targeted intake questions.
2. Run `sub-profile-intake` to build the scoped profile.
3. Run `sub-safety-screener` to lock frameworks: WHO antenatal care (ANC) guidelines, ACOG prenatal care recommendations, Gestational-week milestone framework, Danger-sign triage (pre-eclampsia, bleeding, reduced movement)....
4. Research: issue WebSearch queries (antenatal care WHO guideline; pregnancy danger signs screening; prenatal nutrition evidence); WebFetch top authoritative hits; grade evidence. On failure, fall back to SECOND-KNOWLEDGE-BRAIN.md and label the degradation.
5. Run `sub-framework-selector` to score the 6 dimensions.
6. Run `sub-improvement-roadmap` challenge pass.
7. **SAFETY:** run sub-safety-screener; if red flags, halt and emit escalation guidance only.

8. Synthesize the final deliverable.

## Scoring Dimensions
1. Gestational-week appropriateness
2. Danger-sign screening
3. Nutrition & supplementation
4. Lifestyle & safety
5. Mental-health (EPDS)
6. Care-schedule adherence

Each dimension is scored 0–5 with an evidence citation and a one-line justification; the overall score is the weighted mean (weights set by `sub-safety-screener`).

## SECOND-KNOWLEDGE-BRAIN Integration
- **Sources:** ArXiv (q-bio.QM); WHO ANC guidelines, ACOG / NICE antenatal guidance, PubMed obstetrics, Cochrane pregnancy reviews, CDC pregnancy resources.
- **Crawl config:** weekly cron via `tools/knowledge_updater.py` (crawl4ai).
- **Append format:** scored entries (title, authors, year, DOI/URL, key finding, relevance) added to the Knowledge Update Log with a date stamp and dedup by URL/DOI hash.

## Supporting Tools Spec
`tools/knowledge_updater.py`:
- **Inputs:** search queries (above), ArXiv categories, last-run timestamp.
- **Outputs:** appended entries in `SECOND-KNOWLEDGE-BRAIN.md`.
- **Schedule:** weekly.

## Quality Gates (must all be TRUE before final output)
- Every dimension scored with a cited source or explicit fallback label.
- At least one framework from the catalog explicitly applied.
- Challenge phase documented (≥3 counter-arguments considered).
- Safety screen passed / escalation issued.

- Roadmap items carry impact + effort ratings.

## Test Scenarios (summary; full set in tests/)
1. Happy-path full audit of a typical health, wellness & psychology artifact.
2. Ambiguous/incomplete input → intake clarification path.
3. Offline/degraded mode → graceful fallback to knowledge brain.
4. Safety red-flag input → escalation path.
5. Roadmap-only request → returns prioritized recommendations.

## Key Design Decisions
1. Framework-grounded scoring only — no ad-hoc criteria.
2. Research-first with explicit graceful degradation.
3. Mandatory challenge phase before synthesis.
4. Safety screening precedes all guidance.
5. Self-improving knowledge base via weekly crawl.
