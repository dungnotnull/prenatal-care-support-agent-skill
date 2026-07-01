---
name: sub-framework-selector
description: (prenatal-care-support) Apply WHO/ACOG week-specific ANC guidelines and validated screening tools. Score 6 dimensions 0-5 with evidence citations.
---

# Sub-skill: Framework Selector

> **Shared cluster template:** `.shared/cluster-shared-subskills.md` → `shared-evidence-framework-selector`

## Purpose
Apply WHO/ACOG week-specific antenatal care (ANC) guidelines and validated screening tools. Score each of the 6 dimensions (0-5 scale) with explicit framework citations and evidence-based justifications.

## When the Harness Calls This
Stage 4 of the `prenatal-care-support` main workflow. After research/evidence gathering, before challenge phase.

## Inputs
- **Structured profile:** From `sub-profile-intake`
- **Safety status:** CLEAR/ESCALATE from `sub-safety-screener`
- **Research evidence:** From WebSearch/WebFetch or SECOND-KNOWLEDGE-BRAIN.md fallback
- **Framework catalog:** Pre-loaded from skill definition

## Framework Catalog

### Core Frameworks

| Framework | Source | Application | Evidence Tier |
|-----------|--------|-------------|---------------|
| WHO ANC Guidelines (2016/2022) | WHO | Antenatal contact schedule, interventions | 5 (Systematic Review/Guideline) |
| ACOG Prenatal Care Recommendations | ACOG | US-standard prenatal care, screening | 4 (Clinical Guideline) |
| Gestational Age Milestone Framework | NIH/ACOG | Week-specific developmental milestones | 4 (Guideline/Consensus) |
| Danger Sign Triage Framework | WHO/CDC | Symptom-based emergency identification | 5 (Systematic Review) |
| Nutrition in Pregnancy Framework | ACOG/WHO | Supplementation, dietary guidance | 4 (Guideline) |
| Edinburgh Postnatal Depression Scale (EPDS) | COchrane/Validated tool | Perinatal mood screening | 4 (Validated instrument) |

### Supplementary Frameworks

| Framework | Source | Application |
|-----------|--------|-------------|
| USPSTF Prenatal Screening Recommendations | USPSTF | Evidence-based screening indications |
| NICE Antenatal Care Guidelines | NICE (UK) | International standard comparison |
| IOM Pregnancy Weight Guidelines | IOM | Gestational weight gain standards |
| CDC Pregnancy Vaccine Schedule | CDC | Immunization timing and safety |

## Scoring Dimensions

### Dimension 1: Gestational-Week Appropriateness (0-5)

**Framework:** WHO ANC Guidelines + ACOG Timing Recommendations

**Score Criteria:**
| Score | Criteria | Framework Basis |
|-------|----------|-----------------|
| 5 | All milestone-appropriate interventions completed (dating USG ≤12w, anatomy scan 20w, GDM screen 24-28w) | WHO ANC 2016 |
| 4 | Core milestones met, minor interventions may be pending | ACOG PBs |
| 3 | Basic care established but missing milestone-specific care | WHO minimum 8 contacts |
| 2 | Significant gaps in milestone-appropriate care | WHO gap analysis |
| 1 | No milestone-appropriate care documented | WHO deviation |
| 0 | No care or inappropriate for gestational age | WHO standard not met |

**Evidence Context:**
```markdown
### WHO ANC Contact Schedule (8 contacts minimum)
- 12 weeks: Dating ultrasound, bloodwork, initial counseling
- 20 weeks: Anatomy ultrasound, fetal growth assessment
- 26 weeks: Blood pressure, fundal height, anemia screen
- 30 weeks: Blood pressure, fundal height, fetal position
- 34 weeks: Blood pressure, fetal presentation, growth
- 36 weeks: GDM screen if not done, Group B Strep
- 38 weeks: Birth planning, fetal wellbeing
- 40 weeks: Postdates planning if no labor
```

### Dimension 2: Danger-Sign Screening (0-5)

**Framework:** WHO Danger Sign Triage + ACOG Emergency Protocols

**Score Criteria:**
| Score | Criteria | Framework Basis |
|-------|----------|-----------------|
| 5 | Proactive danger-sign education provided; no red flags present | WHO education standard |
| 4 | Danger signs reviewed; patient knows when to seek care | ACOG patient education |
| 3 | Basic symptom review but no proactive education | Minimum standard |
| 2 | Danger signs not reviewed or patient unaware | Below standard |
| 1 | Red flags present but not escalated | WHO emergency protocol violation |
| 0 | Emergency symptoms present without escalation | Critical deviation |

**Evidence Context:**
```markdown
### WHO Danger Signs (must-know for every pregnant person)
- Vaginal bleeding
- Severe headache, vision changes
- Sudden swelling, especially face/hands
- Severe abdominal pain
- Fever >38°C
- Reduced or no fetal movement
- Regular contractions before 37 weeks
```

### Dimension 3: Nutrition & Supplementation (0-5)

**Framework:** ACOG Nutrition in Pregnancy + WHO Micronutrient Guidelines

**Score Criteria:**
| Score | Criteria | Framework Basis |
|-------|----------|-----------------|
| 5 | All recommended supplements taken daily; appropriate weight gain | ACOG PB #291 |
| 4 | Prenatal vitamins with folate taken; appropriate nutrition | ACOG standard |
| 3 | Basic prenatal vitamins; minor gaps in nutrition | Minimum acceptable |
| 2 | Inconsistent supplementation or significant dietary gaps | Below standard |
| 1 | No supplementation documented | Major gap |
| 0 | Contra-indicated substances (alcohol, unsafe medications) | ACOG禁忌清单 |

**Evidence Context:**
```markdown
### ACOG Recommended Supplements (PB #291, 2024)
- **Folic acid:** 400-800 mcg daily (start 1 month preconception through 12 weeks)
- **Iron:** 27 mg daily (30 mg elemental iron, 2nd/3rd trimester)
- **Prenatal vitamin:** Daily with DHA (200-300 mg) recommended
- **Calcium:** 1,000 mg daily dietary + supplement if needed
- **Vitamin D:** 600 IU daily (1,000 IU if deficient)

### Avoid (ACOG Teratology):
- Alcohol (no amount safe)
- High-mercury fish (shark, swordfish, king mackerel)
- Unpasteurized dairy (Listeria risk)
- Excess caffeine (>200 mg/day)
- NSAIDs after 20 weeks (avoid ibuprofen, naproxen)
```

### Dimension 4: Lifestyle & Safety (0-5)

**Framework:** ACOG Lifestyle Recommendations + CDC Pregnancy Safety

**Score Criteria:**
| Score | Criteria | Framework Basis |
|-------|----------|-----------------|
| 5 | All safe practices followed; no unsafe exposures | ACOG Lifestyle PBs |
| 4 | Major safety measures in place; minor education needed | Standard care |
| 3 | Basic safety established; some gaps in knowledge | Minimum acceptable |
| 2 | Significant unsafe practices or exposures | Below standard |
| 1 | Multiple unsafe exposures | Major concern |
| 0 | Documented dangerous exposures (abuse, substances) | Critical concern |

**Evidence Context:**
```markdown
### ACOG Safe Practices
- Exercise: 150 min/week moderate activity (walking, swimming)
- Sleep: Side-sleeping (left lateral) after 20 weeks
- Seatbelts: Lap belt below bump, shoulder belt across chest
- Cat litter: Avoid due to toxoplasmosis risk
- Hot tubs: Avoid (core temperature >101°F risky)
- Dental care: Safe and recommended; local anesthesia OK

### Avoid
- Smoking (nicotine replacement only if medically indicated)
- Alcohol (no amount safe)
- Recreational drugs
- High-impact/contact sports after 1st trimester
- Excessive heat (saunas, hot yoga)
```

### Dimension 5: Mental-Health (EPDS) (0-5)

**Framework:** Edinburgh Postnatal Depression Scale (EPDS) + ACOG Mental Health Screening

**Score Criteria:**
| Score | Criteria | Framework Basis |
|-------|----------|-----------------|
| 5 | EPDS ≤9 or negative; no mood concerns; coping well | EPDS validated |
| 4 | EPDS 10-12 or mild symptoms addressed | ACOG screening |
| 3 | EPDS 13-15 but evaluation initiated | Below threshold |
| 2 | EPDS ≥13 without evaluation or moderate symptoms untreated | Below standard |
| 1 | Severe symptoms or suicidal ideation without escalation | Critical concern |
| 0 | Active crisis, self-harm, or suicidality | EMERGENCY |

**Evidence Context:**
```markdown
### EPDS Scoring (10-item screen)
- **≤9:** Negative for depression/perinatal mood
- **10-12:** Mild symptoms; monitor, support resources
- **13-15:** Moderate depression; clinical evaluation recommended
- **≥16:** Severe depression; urgent evaluation needed

### Item 10 (Self-Harm) — ANY positive answer requires immediate evaluation:
- "The thought of harming myself has occurred to me"
- If YES → Assess for active suicidal ideation → ESCALATE

### ACOG Recommendation (PB #220, 2023)
- Screen at least once during pregnancy (ideally 28 weeks)
- Screen again postpartum (6 weeks)
- Use validated tool (EPDS, PHQ-9)
```

### Dimension 6: Care-Schedule Adherence (0-5)

**Framework:** WHO ANC Contact Schedule + ACOG Visit Frequency

**Score Criteria:**
| Score | Criteria | Framework Basis |
|-------|----------|-----------------|
| 5 | ≥8 ANC contacts; weekly by 36 weeks; all milestone visits done | WHO optimal |
| 4 | 6-7 contacts; biweekly by 32 weeks; milestone visits done | ACOG standard |
| 3 | 4-5 contacts; monthly through 36 weeks; basic care | Minimum acceptable |
| 2 | 2-3 visits; significant gaps in schedule | Below standard |
| 1 | ≤1 visit or no established care | Major gap |
| 0 | No prenatal care | Critical deviation |

**Evidence Context:**
```markdown
### WHO 2022 Recommendations (≥8 contacts)
- First contact: ≤12 weeks
- Second: 20 weeks (anatomy scan)
- Third: 26 weeks
- Fourth: 30 weeks
- Fifth: 34 weeks
- Sixth: 36 weeks
- Seventh: 38 weeks
- Eighth: 40 weeks (postdates planning)

### ACOG Frequency (minimum)
- ≤28 weeks: Every 4 weeks
- 28-36 weeks: Every 2 weeks
- ≥36 weeks: Every week
- Postdates (≥41 weeks): Twice weekly (NST/BPP)
```

## Procedure

### 1. Load Framework Selection

Based on gestational age and clinical context, select applicable frameworks:

```python
def select_frameworks(gestational_week, risk_factors):
    frameworks = []

    # Always include
    frameworks.append('WHO ANC Guidelines')
    frameworks.append('ACOG Prenatal Care')

    # Week-specific
    if gestational_week <= 12:
        frameworks.append('First Trimester Care Standards')
    elif 13 <= gestational_week <= 27:
        frameworks.append('Second Trimester Care Standards')
    else:
        frameworks.append('Third Trimester Care Standards')

    # Risk-specific
    if 'hypertension' in risk_factors or 'preeclampsia' in risk_factors:
        frameworks.append('ACOG Hypertension in Pregnancy')
    if 'diabetes' in risk_factors or 'GDM' in risk_factors:
        frameworks.append('ACOG Gestational Diabetes')

    return frameworks
```

### 2. Score Each Dimension

For each of the 6 dimensions:

**Step 2.1: Gather evidence**
- Check research results for dimension-specific guidelines
- Verify with SECOND-KNOWLEDGE-BRAIN.md if offline
- Note any applicable framework criteria

**Step 2.2: Apply score rubric**
- Match profile evidence to score criteria
- Document justification
- Cite framework and evidence tier

**Step 2.3: Document scoring**

```markdown
### Dimension 1: Gestational-Week Appropriateness — 4/5

**Evidence:** Dating ultrasound at 10 weeks (WHO standard ≤12w). Anatomy scan scheduled for 20w6d (WHO 20w milestone). GDM screening planned for 26w (WHO 24-28w window).

**Framework:** WHO ANC Guidelines (2016) — 8-contact model

**Justification:** Core milestone care is appropriate for gestational age. Minor gap: anemia screening not yet documented (recommended 26w, can be completed).

**Evidence Tier:** Tier 4 (Clinical Guideline)

**Score:** 4/5 — All major milestones met; one minor screening pending.
```

### 3. Calculate Overall Score

```python
def calculate_weighted_score(dimension_scores):
    # Safety dimensions weighted higher
    weights = {
        'gestational_week': 0.15,
        'danger_sign_screening': 0.25,  # Highest weight
        'nutrition': 0.15,
        'lifestyle': 0.15,
        'mental_health': 0.20,  # High weight
        'care_schedule': 0.10
    }

    weighted = sum(
        dimension_scores[dim] * weights[dim]
        for dim in dimension_scores
    )

    return round(weighted, 1)
```

### 4. Output Scoring Table

```markdown
## Scoring Table

| Dimension | Score (0-5) | Framework | Justification | Evidence Tier |
|-----------|-------------|-----------|---------------|---------------|
| Gestational-week appropriateness | 4/5 | WHO ANC 2016 | All major milestones met; one minor screening pending | Tier 4 |
| Danger-sign screening | 5/5 | WHO Triage + ACOG Emergency | No red flags; proactive education provided | Tier 5 |
| Nutrition & supplementation | 3/5 | ACOG PB #291 | Prenatal vitamins taken; inconsistent folate timing | Tier 4 |
| Lifestyle & safety | 4/5 | ACOG Lifestyle PBs | All safe practices; minor education gaps | Tier 4 |
| Mental-health (EPDS) | 5/5 | EPDS validated | EPDS 7/30 (negative); coping well | Tier 4 |
| Care-schedule adherence | 4/5 | WHO 8-contact | 6 contacts to date; on track for ≥8 | Tier 4 |

**Overall Score:** 4.2/5

**Frameworks Applied:** WHO ANC Guidelines (2016), ACOG Prenatal Care Recommendations, Edinburgh Postnatal Depression Scale (validated), ACOG Nutrition in Pregnancy (PB #291)
```

## Outputs
- **Scoring table:** All 6 dimensions with scores, frameworks, justifications
- **Overall score:** Weighted mean (0-5)
- **Evidence citations:** Tier-graded sources for each dimension
- **Applied frameworks:** List of frameworks used in scoring

## Quality Gate

**Pass conditions:**
- [ ] All 6 dimensions scored
- [ ] Each score has framework citation
- [ ] Each score has evidence tier (or fallback label)
- [ ] Justification provided for each score
- [ ] At least one framework explicitly applied
- [ ] Overall score calculated

**Fail conditions:**
- Missing dimension score
- Score without citation or framework
- No evidence tier or fallback label
- No justification for score

## Integration with Shared Cluster Template

This sub-skill implements `shared-evidence-framework-selector` from `.shared/cluster-shared-subskills.md`:
- Uses standardized scoring format (0-5)
- Requires framework citation for each dimension
- Outputs structured scoring table

## Next Stage
Output passes to `sub-improvement-roadmap` for challenge/devil's-advocate phase.
