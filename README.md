# Pregnancy / Prenatal Care Support (weekly)

> **Research-first prenatal health education harness** grounded in WHO/ACOG guidelines and validated screening tools.

![Status: Production-Ready](https://img.shields.io/badge/status-production--ready-success)
![Version: 1.0.0](https://img.shields.io/badge/version-1.0.0-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

## Overview

This skill provides week-by-week prenatal care guidance through a research-first, evidence-based harness. It scores pregnancy care against 6 dimensions using world-renowned frameworks (WHO, ACOG, EPDS) and generates a prioritized improvement roadmap.

**⚠️ Disclaimer:** This skill provides educational analysis only and is not a substitute for a qualified obstetrician, midwife, or healthcare provider.

## Features

- **Evidence-Based Scoring:** 6 dimensions scored against WHO/ACOG guidelines
- **Safety-First Design:** Emergency/crisis screening before any guidance
- **Challenge Phase:** Devil's-advocate review to prevent bias
- **Week-by-Week Education:** Gestational-age-specific guidance
- **Prioritized Roadmap:** Impact/Effort-ranked recommendations
- **Offline Capable:** Graceful degradation to cached knowledge
- **Production-Grade:** Full implementation with comprehensive testing

## Quick Start

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/prenatal-care-support.git
cd prenatal-care-support
```

2. Verify file structure:
```bash
# Should see:
# - skills/main.md
# - skills/sub-*.md (4 sub-skills)
# - tools/knowledge_updater.py
# - tests/test-scenarios.md
# - tests/test_runner.py
```

### Usage

**As a Claude Skill:**
This skill integrates with the Claude Code harness. Reference `skills/main.md` for the complete workflow.

**Running Tests:**
```bash
# Run automated test suite
python tests/test_runner.py --save

# Output: test results saved to test_results/
# - test_results_YYYYMMDD_HHMMSS.json
# - calibration_report.md
```

**Updating Knowledge Base:**
```bash
# Run weekly knowledge crawl
python tools/knowledge_updater.py

# Dry run (no changes)
python tools/knowledge_updater.py --dry-run

# Force refresh (ignore cache)
python tools/knowledge_updater.py --force
```

## Documentation

| Document | Description |
|----------|-------------|
| [PROJECT-detail.md](PROJECT-detail.md) | Full technical specification |
| [PROJECT-DEVELOPMENT-PHASE-TRACKING.md](PROJECT-DEVELOPMENT-PHASE-TRACKING.md) | Development phase tracking |
| [skills/main.md](skills/main.md) | Main harness and workflow |
| [.shared/cluster-shared-subskills.md](.shared/cluster-shared-subskills.md) | Cluster integration templates |
| [tests/test-scenarios.md](tests/test-scenarios.md) | Test scenarios and validation |

## Architecture

### Harness Workflow

```
USER INPUT
   ↓
[Stage 1] sub-profile-intake    → Structured profile
   ↓
[Stage 2] sub-safety-screener   → CLEAR/ESCALATE status
   ↓
[Stage 3] Research              → Evidence pack (fallback: knowledge brain)
   ↓
[Stage 4] sub-framework-selector → 6-dimension scoring
   ↓
[Stage 5] sub-improvement-roadmap → Challenge phase + roadmap
   ↓
[Stage 6] Synthesis             → Final report
```

### Scoring Dimensions

1. **Gestational-Week Appropriateness** (WHO ANC milestones)
2. **Danger-Sign Screening** (WHO/AOG emergency protocols)
3. **Nutrition & Supplementation** (ACOG PB #291)
4. **Lifestyle & Safety** (ACOG lifestyle recommendations)
5. **Mental-Health** (Edinburgh Postnatal Depression Scale)
6. **Care-Schedule Adherence** (WHO 8-contact model)

### Frameworks Applied

- WHO Antenatal Care (ANC) Guidelines (2016/2022)
- ACOG Prenatal Care Recommendations
- Gestational Age Milestone Framework
- Danger Sign Triage Framework
- Nutrition in Pregnancy Framework
- Edinburgh Postnatal Depression Scale (EPDS)

## Quality Gates

All reports must pass these gates before output:

**Content:**
- [ ] Every dimension scored with cited source
- [ ] ≥1 named framework explicitly applied
- [ ] Challenge phase documented (≥3 counter-arguments)
- [ ] Safety screen passed or escalation issued

**Format:**
- [ ] Roadmap items carry impact + effort ratings
- [ ] Evidence tiers labeled on all citations
- [ ] Graceful-degradation label if offline

**Safety:**
- [ ] Disclaimer prominently displayed
- [ ] No emergency case with normal guidance

## Development

### Project Status

| Phase | Status | Output |
|-------|--------|--------|
| 0 | ✅ Complete | Architecture + frameworks |
| 1 | ✅ Complete | 4 sub-skills |
| 2 | ✅ Complete | Harness + quality gates |
| 3 | ✅ Complete | Knowledge pipeline |
| 4 | ✅ Complete | Test suite |
| 5 | ✅ Complete | Cluster integration |

**Total:** All phases 0-5 complete (4.5 days effort)

### File Structure

```
prenatal-care-support/
├── .shared/
│   └── cluster-shared-subskills.md
├── skills/
│   ├── main.md
│   ├── sub-profile-intake.md
│   ├── sub-safety-screener.md
│   ├── sub-framework-selector.md
│   └── sub-improvement-roadmap.md
├── tests/
│   ├── test-scenarios.md
│   └── test_runner.py
├── tools/
│   └── knowledge_updater.py
├── SECOND-KNOWLEDGE-BRAIN.md
├── CLAUDE.md
├── PROJECT-detail.md
├── PROJECT-DEVELOPMENT-PHASE-TRACKING.md
└── README.md
```

## Testing

Run the automated test suite:

```bash
python tests/test_runner.py --save
```

**Test Coverage:**
- Happy-path full evaluation
- Ambiguous/incomplete input
- Offline/degraded mode
- Challenge phase validation
- Roadmap-only request
- Safety red-flag escalation
- Tier 1 emergency handling

## Contributing

This skill is part of the `health-wellness` cluster. When contributing:

1. Follow cluster standards in `.shared/cluster-shared-subskills.md`
2. Maintain all quality gates
3. Update test scenarios for new features
4. Run test suite before submitting
5. Document framework references

## Cluster Integration

This skill implements shared cluster templates:

- `shared-intake-collector` → `sub-profile-intake.md`
- `shared-safety-triage` → `sub-safety-screener.md`
- `shared-evidence-framework-selector` → `sub-framework-selector.md`
- `shared-devils-advocate` → `sub-improvement-roadmap.md`

Sibling skills in the `health-wellness` cluster can reference these templates.

## License

MIT License — See [LICENSE](LICENSE) file for details.

## Disclaimer

This skill provides educational analysis only. Always consult with a qualified obstetrician, midwife, or healthcare provider before making decisions based on this information.

In case of emergency, call 911 or your local emergency number immediately.

---

**Version:** 1.0.0
**Status:** Production-Ready
**Last Updated:** 2026-07-01
**Skill:** prenatal-care-support
**Cluster:** health-wellness
