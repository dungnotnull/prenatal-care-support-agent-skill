---
name: sub-improvement-roadmap
description: (prenatal-care-support) Generate week-by-week education and care-schedule plan with clinical-visit triggers. Run challenge phase before final roadmap.
---

# Sub-skill: Improvement Roadmap

> **Shared cluster template:** `.shared/cluster-shared-subskills.md` → `shared-devils-advocate`

## Purpose
Generate a week-by-week education and care-schedule plan with clinical-visit triggers. Run a challenge/devil's-advocate phase before synthesizing the final roadmap. Ensure recommendations are ranked by impact and effort.

## When the Harness Calls This
Stage 5 of the `prenatal-care-support` main workflow. After scoring, before final synthesis.

## Inputs
- **Scoring table:** From `sub-framework-selector`
- **Structured profile:** From `sub-profile-intake`
- **Safety status:** CLEAR/ESCALATE from `sub-safety-screener`
- **Research evidence:** From WebSearch/WebFetch or SECOND-KNOWLEDGE-BRAIN.md

## Challenge / Devil's-Advocate Phase (Must Run FIRST)

Before generating any roadmap, challenge the initial scoring to surface counter-arguments and potential biases.

### Challenge Categories

#### 1. Optimism Bias Challenge

**Question:** "What if the user's self-report is overly optimistic?"

**Common Optimism Biases in Pregnancy:**
- Under-reporting symptoms (don't want to worry provider)
- Overestimating adherence ( prenatal vitamins "most days" vs. daily)
- Minimizing stress ("I'm fine" when overwhelmed)
- Normalizing symptoms ("swelling is just pregnancy")

**Challenge Protocol:**
```python
def challenge_optimism_bias(profile, scores):
    # If self-reported as "perfect" or "no concerns"
    if profile.get('self_report') == 'perfect':
        # Re-score with pessimistic assumption
        revised_scores = {}
        for dim in scores:
            revised_scores[dim] = scores[dim] - 1  # Reduce by 1 point
        return revised_scores
    return scores
```

**Documentation:**
```markdown
### Counter-Argument 1: Optimism Bias
- **Issue:** Self-report indicates "no concerns" which may underestimate actual risks.
- **Consideration:** Patients often minimize symptoms to avoid worrying providers or due to normalization of pregnancy discomforts.
- **Resolution:** Reduced Gestational-week appropriateness score from 4 to 3 (pending verification), Danger-sign screening from 5 to 4 (needs objective confirmation).
```

#### 2. Framework Conflict Challenge

**Question:** "What if different frameworks disagree on this dimension?"

**Common Framework Conflicts:**
- WHO vs. ACOG on visit frequency (WHO: 8 contacts, ACOG: minimum 8-10)
- USPSTF vs. ACOG on GDM screening timing (USPSTF: 24-28w, ACOG: 24-28w plus early if high-risk)
- NICE vs. ACOG on anemia screening thresholds

**Challenge Protocol:**
```python
def challenge_framework_conflicts(scores, frameworks_used):
    # Check for conflicting recommendations
    conflicts = identify_framework_conflicts(frameworks_used)

    if conflicts:
        # If multiple frameworks apply, take conservative score
        return min_score(frameworks)
    return scores
```

**Documentation:**
```markdown
### Counter-Argument 2: Framework Conflict
- **Issue:** WHO ANC guidelines recommend earlier anemia screening (26w) than ACOG standard (28w).
- **Consideration:** Applying the more conservative recommendation (earlier) yields lower adherence score.
- **Resolution:** Reduced Care-schedule adherence score from 4 to 3 based on WHO 26w standard not being met.
```

#### 3. Population Generalizability Challenge

**Question:** "What if this guidance doesn't apply to the user's specific situation?"

**Population-Specific Considerations:**
- Age-related risks (≤20 or ≥35)
- BMI-related complications
- Geographic access to care (rural vs. urban)
- Socioeconomic factors (insurance, transportation)
- Cultural/language barriers
- Pre-existing conditions (hypertension, diabetes, mental health)

**Challenge Protocol:**
```python
def challenge_generalizability(profile, recommendations):
    # Check if recommendations account for specific population factors
    factors = extract_population_factors(profile)

    if factors.get('age', 0) >= 35:
        # Recalculate with AMA (advanced maternal age) considerations
        return adjust_for_ama(recommendations)

    if factors.get('bmi', 0) >= 30:
        # Recalculate with obesity considerations
        return adjust_for_obesity(recommendations)

    return recommendations
```

**Documentation:**
```markdown
### Counter-Argument 3: Population Generalizability
- **Issue:** Standard guidance may not fully account for AMA (age ≥35) risk factors.
- **Consideration:** AMA pregnancies have higher risk of hypertension, GDM, and stillbirth; may warrant enhanced surveillance.
- **Resolution:** Added recommendation for AMA-specific screening (detailed anatomic scan, growth scans) not in standard protocol.
```

#### 4. Resource Constraint Challenge

**Question:** "What if the user can't access recommended care?"

**Common Resource Constraints:**
- Insurance coverage gaps
- Geographic barriers (rural, no local OB)
- Transportation limitations
- Cost barriers (medications, supplements)
- Time constraints (work, childcare)
- Language/cultural barriers

**Challenge Protocol:**
```python
def challenge_resource_constraints(profile, roadmap):
    # If recommendations assume ideal access
    if not profile.get('access_barriers'):
        # Add alternative options for limited-access scenarios
        return add_access_alternatives(roadmap)

    return roadmap
```

**Documentation:**
```markdown
### Counter-Argument 4: Resource Constraints
- **Issue:** Initial roadmap assumes full insurance coverage and local OB access, which may not apply.
- **Consideration:** Limited access requires prioritization of high-impact interventions and alternative care models.
- **Resolution:** Added alternatives: community health clinics, Medicaid enrollment assistance, telehealth options for mental health.
```

#### 5. Evidence Quality Challenge

**Question:** "What if the evidence supporting this score is weak or outdated?"

**Evidence Quality Checks:**
- Is the source current (≤5 years old for guidelines)?
- Is the evidence tier appropriate (prefer systematic reviews over expert opinion)?
- Is there conflicting evidence?
- Has the guidance changed recently?

**Challenge Protocol:**
```python
def challenge_evidence_quality(scores, evidence_sources):
    # Check evidence age and tier
    for dim, source in evidence_sources.items():
        if source.get('year') < 2019:  # >5 years old
            # Reduce score or flag for review
            scores[dim] = min(scores[dim], 3)  # Cap at 3

        if source.get('tier') <= 2:  # Weak evidence
            # Flag for higher-quality evidence needed
            flag_weak_evidence(dim)

    return scores
```

**Documentation:**
```markdown
### Counter-Argument 5: Evidence Quality
- **Issue:** Nutrition guidance cited from 2015 ACOG PB may be outdated compared to 2024 updates.
- **Consideration:** Newer evidence on choline, DHA dosing, and iron supplementation changes recommendations.
- **Resolution:** Updated Nutrition score from 3 to 2 pending review of 2024 ACOG guidelines; flagged for evidence refresh.
```

### Challenge Phase Output

Document ALL counter-arguments considered and their impact:

```markdown
## Challenge / Devil's-Advocate Notes

### Counter-Arguments Considered (5)

1. **Optimism Bias** — Reduced Gestational-week appropriateness (4→3) and Danger-sign screening (5→4) pending objective verification.

2. **Framework Conflict** — Reduced Care-schedule adherence (4→3) based on WHO 26w anemia screening standard vs. ACOG 28w.

3. **Population Generalizability** — Added AMA-specific screening recommendations for advanced maternal age.

4. **Resource Constraints** — Added alternative care options for limited-access scenarios.

5. **Evidence Quality** — Flagged Nutrition guidance for update based on 2024 ACOG revisions; score reduced 3→2 pending review.

### Revised Scores After Challenge
- Gestational-week appropriateness: 3/5 (was 4)
- Danger-sign screening: 4/5 (was 5)
- Nutrition: 2/5 (was 3)
- Care-schedule adherence: 3/5 (was 4)

**Original Overall: 4.2/5 → Revised Overall: 3.6/5**
```

## Roadmap Generation

After challenge phase, generate prioritized improvement roadmap.

### Week-by-Week Education Plan

By trimester and gestational age:

```markdown
## Week-by-Week Education Plan

### Current Trimester: [First/Second/Third] (Weeks X-Y)

**Week [X]: [Topic]**
- **What to expect:** [Milestone, symptom, or development]
- **Action items:** [Specific recommendations]
- **When to seek care:** [Red flags specific to this week]
- **Resources:** [Links or references]

**Week [X+1]: [Next topic]**
...
```

### Clinical Visit Schedule

```markdown
## Clinical Visit Schedule

### Upcoming Visits

| Visit | Gestational Age | Purpose | What to Expect | Prep Needed |
|-------|-----------------|---------|----------------|-------------|
| [1] | [X]w [Y]d | [Purpose] | [Tests, measurements] | [Prep instructions] |
| [2] | [X]w [Y]d | [Purpose] | [Tests, measurements] | [Prep instructions] |
```

### Prioritized Improvement Roadmap

**Format:** Must follow cluster standard from `.shared/cluster-shared-subskills.md`

```markdown
## Prioritized Improvement Roadmap

| # | Recommendation | Impact (H/M/L) | Effort (H/M/L) | Framework Basis | Dependencies |
|---|----------------|----------------|----------------|-----------------|---------------|
| 1 | [Specific action] | H | M | [Named framework] | None/Specified |
| 2 | [Specific action] | M | L | [Named framework] | Depends on #1 |
```

### Ranking Logic

1. **Primary sort:** Impact (High > Medium > Low)
2. **Secondary sort:** Effort (Low > Medium > High) — prioritize quick wins
3. **Tertiary sort:** Dependencies — foundational items first

### Impact Assessment Framework

| Impact Level | Definition | Examples |
|--------------|------------|----------|
| High | Direct effect on maternal/fetal safety or critical milestone | Emergency symptom recognition, GDM screening, anemia treatment |
| Medium | Improves outcomes or addresses significant gap | Prenatal vitamin optimization, mental health screening |
| Low | Quality of life or minor improvement | Exercise guidance, sleep positioning |

### Effort Assessment Framework

| Effort Level | Definition | Examples |
|--------------|------------|----------|
| High | Requires multiple steps, specialist access, or significant behavior change | Establishing new care provider, lifestyle overhaul |
| Medium | Some steps required or moderate behavior change | Starting supplements, symptom monitoring routine |
| Low | Simple action or one-time step | Single educational session, one lab test |

## Procedure

### 1. Run Challenge Phase
- Generate ≥3 counter-arguments (ideally 5)
- Document each counter-argument and its resolution
- Revise scores based on valid challenges
- Output challenge notes section

### 2. Generate Week-by-Week Plan
- Based on current gestational age
- Cover topics through next 4-8 weeks
- Include action items and red flags
- Reference appropriate frameworks

### 3. Generate Clinical Schedule
- List upcoming visits per WHO/ACOG schedule
- Include visit purpose and expectations
- Add prep instructions
- Flag any high-priority visits

### 4. Generate Roadmap
- Based on revised scores (post-challenge)
- Prioritize by Impact × Effort matrix
- Include framework basis for each recommendation
- Note dependencies between items

### 5. Quality Gate Check
Before passing to final synthesis:
- [ ] Challenge phase documented (≥3 counter-arguments)
- [ ] Revised scores documented
- [ ] Week-by-week plan covers next 4-8 weeks
- [ ] Clinical schedule aligned with WHO/ACOG
- [ ] Roadmap ranked by Impact (primary) and Effort (secondary)
- [ ] Each roadmap item has framework citation

## Outputs

### Challenge Output
- Counter-arguments considered (≥3)
- Score revisions documented
- Challenge notes section for final report

### Roadmap Output
- Week-by-week education plan (next 4-8 weeks)
- Clinical visit schedule (upcoming visits)
- Prioritized improvement roadmap (cluster-standard format)
- Impact/Effort matrix for each recommendation

## Quality Gate

**Pass conditions:**
- [ ] Challenge phase run with ≥3 counter-arguments
- [ ] All counter-arguments documented
- [ ] Score revisions justified
- [ ] Week-by-week plan generated
- [ ] Clinical schedule aligned with frameworks
- [ ] Roadmap in cluster-standard format
- [ ] Roadmap ranked by Impact/Effort
- [ ] All recommendations have framework citations

**Fail conditions:**
- Challenge phase skipped or <3 counter-arguments
- Roadmap not in cluster-standard format
- Recommendations without framework basis
- No Impact/Effort assessment

## Integration with Shared Cluster Template

This sub-skill implements `shared-devils-advocate` from `.shared/cluster-shared-subskills.md`:
- Runs systematic challenge phase
- Uses cluster-standard roadmap format
- Applies Impact × Effort ranking logic

## Next Stage
Output passes to main harness for final synthesis into professional deliverable.
