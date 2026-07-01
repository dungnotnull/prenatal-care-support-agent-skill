# CLAUDE.md — Pregnancy / Prenatal Care Support (weekly)

**Skill name:** `prenatal-care-support`
**Tagline:** Pregnancy / Prenatal Care Support (weekly)
**Source idea:** #86  |  **Cluster:** `health-wellness` (Health, Wellness & Psychology)
**Current phase:** Phase 2 complete (core sub-skills + harness + quality gates). Phase 3 knowledge pipeline scaffolded.

## Problem This Skill Solves
Expectant parents lack structured, trustworthy week-by-week guidance and miss warning signs. This skill provides week-specific education, screens for danger signs, and always routes risk to clinical care.

## Harness Flow Summary
1. **Intake / scoping** → `sub-profile-intake.md` gathers context and constraints.
2. **Framework selection** → `sub-safety-screener.md` chooses the named evaluation frameworks for this case.
3. **Research / evidence** → WebSearch + WebFetch pull authoritative sources; fall back to SECOND-KNOWLEDGE-BRAIN.md if offline.
4. **Scoring / analysis** → `sub-framework-selector.md` scores across the 6 dimensions.
5. **Challenge phase** → devil's-advocate review (`sub-improvement-roadmap.md`).
6. **Synthesis** → main harness assembles the final professional deliverable (score + prioritized roadmap).

**Safety gate:** `sub-safety-screener` MUST run before any guidance is produced; crisis/emergency red flags escalate to professional/emergency resources immediately.

## Sub-skills
- `skills/sub-profile-intake.md` — Capture gestational week, history and risk factors with a clear non-clinical disclaimer.
- `skills/sub-safety-screener.md` — Screen for obstetric danger signs FIRST and route urgent symptoms to emergency/clinical care.
- `skills/sub-framework-selector.md` — Apply WHO/ACOG week-specific ANC guidance and validated screens (EPDS).
- `skills/sub-improvement-roadmap.md` — Provide a week-by-week education and care-schedule plan with clinical-visit triggers.

## Tools Required
- WebSearch, WebFetch (research-first evidence gathering)
- Read, Write (deliverable assembly)
- Bash / Python (run `tools/knowledge_updater.py`)

## Knowledge Sources
- ArXiv categories: q-bio.QM
- Domain sources: WHO ANC guidelines, ACOG / NICE antenatal guidance, PubMed obstetrics, Cochrane pregnancy reviews, CDC pregnancy resources

## Supporting Python Tools
- `tools/knowledge_updater.py` — crawl4ai pipeline that refreshes `SECOND-KNOWLEDGE-BRAIN.md` weekly.

## Active Development Tasks
- [x] Scaffold folder + 8 required deliverables
- [x] Define 6 named evaluation frameworks
- [x] Implement 4 sub-skills (min 3)
- [ ] Wire shared cluster sub-skills across `health-wellness`
- [ ] First live crawl to seed SECOND-KNOWLEDGE-BRAIN knowledge log

## Reference Docs
- `PROJECT-detail.md` — full technical spec
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — phase roadmap
- `SECOND-KNOWLEDGE-BRAIN.md` — self-improving knowledge base
