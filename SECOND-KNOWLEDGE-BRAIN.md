# SECOND-KNOWLEDGE-BRAIN.md — Pregnancy / Prenatal Care Support (weekly)

> Self-improving domain knowledge base for `prenatal-care-support` (idea #86, cluster `health-wellness`).
> Grown weekly by `tools/knowledge_updater.py`. Last manual seed: 2026-06-18.

## Core Concepts & Frameworks
This skill grounds every judgment in named, citable methodologies:

| Framework / Method | Type | Role in this skill |
|--------------------|------|--------------------|
| WHO antenatal care (ANC) guidelines | core methodology | applied in scoring |
| ACOG prenatal care recommendations | core methodology | applied in scoring |
| Gestational-week milestone framework | core methodology | applied in scoring |
| Danger-sign triage (pre-eclampsia, bleeding, reduced movement) | core methodology | applied in scoring |
| Nutrition in pregnancy (folate, iron, etc.) | core methodology | applied in scoring |
| Validated screening (EPDS for perinatal mood) | core methodology | applied in scoring |

### Scoring Dimensions
1. Gestational-week appropriateness
2. Danger-sign screening
3. Nutrition & supplementation
4. Lifestyle & safety
5. Mental-health (EPDS)
6. Care-schedule adherence

## Key Research Papers
| Title | Authors | Year | Venue | DOI/Link | Relevance |
|-------|---------|------|-------|----------|-----------|
| _(seed pending first crawl)_ | — | — | q-bio.QM | — | Establish baseline state-of-the-art |

## State-of-the-Art Methods & Tools
- Apply the highest-tier framework available for each dimension.
- Prefer current standards and benchmarks over legacy heuristics.
- Cross-check at least two independent sources for any quantitative claim.

## Authoritative Data Sources
- WHO ANC guidelines
- ACOG / NICE antenatal guidance
- PubMed obstetrics
- Cochrane pregnancy reviews
- CDC pregnancy resources
- ArXiv categories: q-bio.QM

## Analytical Frameworks (world-renowned)
- WHO antenatal care (ANC) guidelines
- ACOG prenatal care recommendations
- Gestational-week milestone framework
- Danger-sign triage (pre-eclampsia, bleeding, reduced movement)
- Nutrition in pregnancy (folate, iron, etc.)
- Validated screening (EPDS for perinatal mood)

## Self-Update Protocol
- **Tool:** `tools/knowledge_updater.py` (crawl4ai)
- **Sources:** ArXiv (q-bio.QM) + domain URLs above
- **Search queries:** antenatal care WHO guideline; pregnancy danger signs screening; prenatal nutrition evidence
- **Frequency:** weekly (cron)
- **Append format:** `| Title | Authors | Year | Venue | DOI/URL | Relevance |` rows + dated log entry
- **Dedup:** skip entries whose URL/DOI hash already exists

## Knowledge Update Log
- **2026-06-18** — Seeded knowledge base: 6 frameworks, 6 scoring dimensions, 5 authoritative sources registered. Awaiting first automated crawl.
