# Cluster-Shared Sub-Skills Reference

> **Cluster:** health-wellness (Health, Wellness & Psychology)
> **Purpose:** Share common sub-skills across sibling skills to avoid duplication
> **Version:** 1.0.0
> **Last Updated:** 2026-07-01

## Overview

This document defines the shared sub-skill architecture for the `health-wellness` cluster. Sibling skills can reference these sub-skills instead of duplicating logic.

## Shared Sub-Skills

### 1. Shared: `shared-intake-collector`

**Purpose:** Standardized intake, scoping, and artifact collection across health/wellness domains.

**Applicable Skills:** All health-wellness cluster skills requiring user input analysis.

**Procedure Template:**
```markdown
1. Parse the incoming artifact/text.
2. Extract key domain fields (skill-specific).
3. Identify missing critical information.
4. Ask ≤5 targeted clarifying questions if needed.
5. Build structured profile for next stage.
```

**Inputs:** User artifact, context, domain framework
**Outputs:** Structured profile, identified gaps, clarification questions (if any)
**Quality Gate:** Profile is complete and evidence-linked

**Implementations:**
- `prenatal-care-support/skills/sub-profile-intake.md`
- Other cluster skills: reference this template

---

### 2. Shared: `shared-safety-triage`

**Purpose:** Universal safety screening for crisis, emergency, or severe-symptom indicators.

**Applicable Skills:** All health-wellness cluster skills providing guidance.

**Procedure Template:**
```markdown
1. Scan input for emergency/crisis indicators.
2. Check against skill-specific red-flag vocabulary.
3. If red flag detected:
   a. STOP normal workflow
   b. Emit escalation resources only
   c. Do NOT provide self-help guidance
4. Return CLEAR/ESCALATE status to harness.
```

**Red-Flag Categories:**
- Medical emergencies (severe symptoms, acute conditions)
- Mental health crises (self-harm, suicide indicators)
- Safety emergencies (abuse, violence)
- Legal/financial emergencies (immediate legal action needed)

**Inputs:** User artifact, context, red-flag definitions
**Outputs:** CLEAR/ESCALATE status, escalation resources (if needed)
**Quality Gate:** No guidance proceeds without CLEAR status

**Implementations:**
- `prenatal-care-support/skills/sub-safety-screener.md`
- Other cluster skills: adapt red-flag vocabulary per domain

---

### 3. Shared: `shared-evidence-framework-selector`

**Purpose:** Apply named, citable frameworks to score user artifacts against domain standards.

**Applicable Skills:** All health-wellness cluster skills requiring evaluation.

**Procedure Template:**
```markdown
1. Load skill-specific framework catalog.
2. Select appropriate frameworks for this case.
3. Score each dimension using framework criteria.
4. Document justification with citations.
5. Return dimension scores + framework references.
```

**Dimension Scoring Standard:**
- Scale: 0-5 per dimension
- Format: `| Dimension | Score | Framework | Justification |`
- Evidence: Each score needs citation or fallback label

**Inputs:** Scoped profile, framework catalog
**Outputs:** Scoring table, dimension justifications, framework citations
**Quality Gate:** All dimensions scored with citations

**Implementations:**
- `prenatal-care-support/skills/sub-framework-selector.md`
- Other cluster skills: define domain-specific dimensions

---

### 4. Shared: `shared-devils-advocate`

**Purpose:** Challenge initial findings through systematic counter-argument generation.

**Applicable Skills:** All health-wellness cluster skills producing recommendations.

**Procedure Template:**
```markdown
1. Generate ≥3 counter-arguments to initial findings:
   - Optimism bias check
   - Alternative framework interpretation
   - Population generalizability concerns
   - Resource constraint considerations
2. Re-evaluate scores based on counter-arguments.
3. Document revisions with rationale.
```

**Inputs:** Initial scoring, dimension analysis
**Outputs:** Revised scores, counter-argument documentation
**Quality Gate:** ≥3 counter-arguments considered; revisions documented

**Implementations:**
- `prenatal-care-support/skills/sub-improvement-roadmap.md`
- Other cluster skills: adapt challenge questions per domain

---

## Standardized Output Formats

### Roadmap Table Format (Cluster Standard)

All health-wellness cluster skills MUST use this roadmap format:

```markdown
## Prioritized Improvement Roadmap

| # | Recommendation | Impact (H/M/L) | Effort (H/M/L) | Framework Basis | Dependencies |
|---|----------------|----------------|----------------|-----------------|---------------|
| 1 | [Specific action] | H | M | [Named framework] | None/Specified |
| 2 | [Specific action] | M | L | [Named framework] | Depends on #1 |
```

**Ranking Logic:**
- Primary sort: Impact (H > M > L)
- Secondary sort: Effort (L > M > H)  # Low effort first
- Tertiary: Dependencies

### Evidence Citation Format (Cluster Standard)

```markdown
## Sources & Evidence Grade

| # | Source | Evidence Tier | Relevance |
|---|--------|---------------|-----------|
| 1 | [Title, Authors, Year] | Tier-X (Systematic Review/RCT/etc) | [Justification] |
```

**Evidence Tiers:**
- Tier 5: Systematic Review, Meta-Analysis
- Tier 4: RCT, Clinical Guideline
- Tier 3: Cohort, Case-Control, Review
- Tier 2: Expert Opinion, Consensus
- Tier 1: Blog, Anecdote (avoid when possible)

### Challenge/Devil's-Advocate Format (Cluster Standard)

```markdown
## Challenge / Devil's-Advocate Notes

### Counter-Argument 1: [Title]
- **Issue:** [What could be wrong with initial assessment]
- **Consideration:** [Alternative perspective or framework]
- **Resolution:** [How this changed the analysis]
```

---

## Cross-Skill Integration Points

### 1. Shared Red-Flag Vocabulary

Skills in the cluster can share red-flag definitions:

| Category | Example Indicators | Applicable Skills |
|----------|-------------------|-------------------|
| Medical Emergency | Severe pain, bleeding, acute symptoms | prenatal, postpartum, chronic-condition |
| Mental Health Crisis | Self-harm, hopelessness, suicide ideation | mental-health, perinatal-psych |
| Safety Emergency | Abuse, violence, neglect | family-planning, pediatric |

### 2. Shared Evidence Sources

Common authoritative sources across the cluster:

| Source | Domain | URL |
|--------|--------|-----|
| WHO Guidelines | Global health | https://www.who.int/guidelines |
| CDC | US public health | https://www.cdc.gov |
| NIH/NLM | Research evidence | https://www.nlm.nih.gov |
| Cochrane | Systematic reviews | https://www.cochranelibrary.com |
| PubMed | Research database | https://pubmed.ncbi.nlm.nih.gov |

### 3. Shared Quality Gates

All cluster skills must pass these gates before emitting output:

- [ ] Every dimension scored with citation (or labeled fallback)
- [ ] ≥1 named framework explicitly applied
- [ ] Challenge phase documented (≥3 counter-arguments)
- [ ] Safety screen passed or escalation issued
- [ ] Roadmap items carry impact + effort ratings

---

## Implementing Shared Sub-Skills in Your Skill

To use shared sub-skills in a new health-wellness skill:

1. **Copy the template** from this document to your `skills/` directory.
2. **Customize for your domain:**
   - Define your specific dimensions and frameworks
   - Adapt red-flag vocabulary to your domain
   - Set appropriate scoring ranges
3. **Reference this document** in your skill's `main.md`:
   ```markdown
   ## Cluster Integration
   Uses shared sub-skills from `.shared/cluster-shared-subskills.md`:
   - `shared-intake-collector` → `sub-profile-intake.md`
   - `shared-safety-triage` → `sub-safety-screener.md`
   - `shared-evidence-framework-selector` → `sub-framework-selector.md`
   - `shared-devils-advocate` → `sub-improvement-roadmap.md`
   ```
4. **Follow output format standards** for roadmaps, citations, and challenges.

---

## Version History

- **1.0.0** (2026-07-01) — Initial shared sub-skill definition for health-wellness cluster
