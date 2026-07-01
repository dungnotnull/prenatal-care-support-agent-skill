---
name: sub-profile-intake
description: (prenatal-care-support) Capture gestational age, medical history, risk factors, and care context with clear non-clinical disclaimer.
---

# Sub-skill: Profile Intake

> **Shared cluster template:** `.shared/cluster-shared-subskills.md` → `shared-intake-collector`

## Purpose
Capture gestational age, medical history, risk factors, and care context with clear non-clinical disclaimer. Build a structured profile for evaluation while detecting gaps that require clarification.

## When the Harness Calls This
Stage 1 of the `prenatal-care-support` main workflow. Runs immediately after user input is received.

## Inputs
- **User artifact:** Free-form text, document, or structured data about the pregnancy/care situation
- **Context:** Any prior conversation context or follow-up information
- **Domain frameworks:** WHO ANC guidelines, ACOG recommendations, gestational milestone framework

## Procedure

### 1. Initial Parsing and Disclaimer Display

```markdown
DISCLAIMER: This analysis is educational only and not a substitute for professional medical care. Always consult with a qualified obstetrician, midwife, or healthcare provider before making decisions.
```

Execute these steps in order:

**Step 1.1: Parse the incoming artifact**
- Extract all pregnancy-relevant information from user input
- Identify structured vs. unstructured data
- Note any explicit dates, weeks, measurements

**Step 1.2: Display disclaimer prominently**
- Must appear before any analysis or guidance
- Non-negotiable: every intake starts with this

### 2. Domain-Specific Field Extraction

Extract and validate these fields:

| Field | Description | Source | Validation |
|-------|-------------|--------|------------|
| Gestational Age | Weeks + days (e.g., "28w3d") | User input, due date, LMP | Must be 0-42 weeks |
| Parity | G#P# (gravida/para) | User input | Format: G1P0, G2P1, etc. |
| Due Date | Estimated delivery date | User input, EDD | Must be valid date |
| Risk Factors | Identified risks (diabetes, hypertension, etc.) | User input | Categorize: pre-existing, pregnancy-related |
| Current Care | Prenatal visit frequency, provider type | User input | Monthly, biweekly, weekly? |
| Nutrition | Supplements, diet patterns | User input | Prenatal vitamins, folate, iron |
| Mental Health | Screened or self-reported concerns | User input | EPDS score, PHQ-9 if available |
| Lifestyle | Smoking, alcohol, activity | User input | Binary (yes/no) or frequency |

### 3. Gap Detection and Clarification

If critical fields are missing, ask targeted questions (≤5 total):

**Priority 1 (Critical): Gestational Age**
```
Question: "What is your current gestational age in weeks? (e.g., '28 weeks' or '28w3d')"
Fallback: "What is your due date or last menstrual period?"
```

**Priority 2 (High): Risk Factors**
```
Question: "Have you been diagnosed with any pregnancy complications or risk factors? (e.g., gestational diabetes, hypertension, preeclampsia history)"
```

**Priority 3 (High): Current Care**
```
Question: "How often are you seeing your prenatal care provider? (monthly, biweekly, weekly)"
```

**Priority 4 (Medium): Nutrition**
```
Question: "Are you taking prenatal vitamins? Any specific supplements?"
```

**Priority 5 (Medium): Mental Health Screening**
```
Question: "Have you been screened for postpartum depression or anxiety? Any concerns about mood or stress?"
```

**Rule:** Stop asking after 5 questions total. Do not fabricate missing data.

### 4. Structured Profile Building

Output the profile in this format:

```markdown
## Pregnancy Profile

| Field | Value | Source |
|-------|-------|--------|
| Gestational Age | [X]w[Y]d | User-provided |
| Parity | G#P# | User-provided |
| Due Date | YYYY-MM-DD | User-provided/estimated |
| Risk Factors | [List] | User-provided |
| Current Care | [Frequency, Provider] | User-provided |
| Nutrition | [Supplements, Diet] | User-provided |
| Mental Health | [Screened/Concerns] | User-provided |
| Lifestyle | [Smoking, Alcohol, Activity] | User-provided |

### Missing Information (If Any)
- [Fields that could not be obtained]
```

### 5. Evidence Linking

For each extracted field, provide evidence context:

```markdown
### Evidence Context
- **Gestational Age:** According to WHO ANC guidelines, key milestones occur at specific weeks (12w: dating ultrasound, 20w: anatomy scan, 28w: glucose screening).
- **Risk Factors:** ACOG defines high-risk pregnancy by conditions such as chronic hypertension, pre-existing diabetes, BMI > 35, prior preeclampsia.
- **Care Schedule:** WHO recommends at least 8 antenatal contacts: 12w, 20w, 26w, 30w, 34w, 36w, 38w, 40w.
```

### 6. Quality Gate Check

Before passing to next stage, verify:

- [ ] Disclaimer displayed
- [ ] Gestational age obtained (or clarification requested)
- [ ] All present fields accurately extracted
- [ ] Missing fields clearly identified
- [ ] Evidence context provided for key fields
- [ ] Profile is complete and structured

## Outputs
- **Structured profile:** Markdown table with all extracted fields
- **Gap analysis:** List of missing critical information
- **Clarification questions:** If gaps exist (≤5 questions)
- **Evidence context:** Framework references for key fields

## Quality Gate
**Pass condition:** Profile is complete with evidence-linked fields OR appropriate clarification questions have been asked (≤5).

**Fail conditions:**
- Missing gestational age without clarification request
- Fabricated data for missing fields
- No disclaimer displayed
- >5 clarification questions (overwhelming user)

## Integration with Shared Cluster Template

This sub-skill implements `shared-intake-collector` from `.shared/cluster-shared-subskills.md`:
- Uses standardized intake procedure
- Follows gap detection protocol
- Outputs structured profile for framework selector

## Next Stage
Output passes to `sub-safety-screener` for emergency/crisis screening.
