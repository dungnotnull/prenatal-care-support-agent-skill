---
name: sub-safety-screener
description: (prenatal-care-support) Screen for obstetric danger signs, crisis indicators, and emergencies. Route urgent symptoms to emergency/clinical care.
---

# Sub-skill: Safety Screener

> **Shared cluster template:** `.shared/cluster-shared-subskills.md` → `shared-safety-triage`

## Purpose
Screen for obstetric danger signs, crisis indicators, and medical emergencies. Route urgent symptoms to emergency/clinical care. This sub-skill **gates the entire harness** — no guidance proceeds until safety screen returns CLEAR.

## When the Harness Calls This
- **Stage 2:** After profile intake, before any guidance or scoring
- **Pre-guidance gate:** Before any roadmap or recommendations are emitted

## Inputs
- **Structured profile:** From `sub-profile-intake`
- **User artifact:** Original input text for symptom scanning
- **Red-flag definitions:** Pregnancy-specific danger signs

## Red-Flag Vocabulary (Obstetric)

### Tier 1: Immediate Emergency (Call 911/Emergency)

| Indicator | Description | Rationale |
|-----------|-------------|------------|
| Vaginal bleeding | Heavy, soaking pad/hr, or passing clots | Possible placental abruption, previa |
| Severe abdominal pain | Constant, intense, not relieved | Possible abruption, rupture |
| Loss of consciousness | Fainting, syncope | Possible hemorrhage, shock |
| Seizure activity | Convulsions | Possible eclampsia |
| No fetal movement | >24 hours without movement | Possible fetal demise |
| Fluid gush | Sudden gush of fluid <37w | Possible PPROM, preterm labor |

### Tier 2: Urgent Clinical Visit (Same-Day)

| Indicator | Description | Rationale |
|-----------|-------------|------------|
| Severe headache + vision changes | "Thunderclap" headache, aura, flashing lights | Possible preeclampsia |
| Sudden swelling | Face, hands, rapid weight gain | Possible preeclampsia |
| BP ≥160/110 or ≥140/90 with symptoms | Severe range hypertension | Possible severe preeclampsia |
| Fever ≥38°C/100.4°F | With or without chills | Possible infection, chorio |
| Reduced fetal movement | <10 movements in 2 hours, after 28w | Possible fetal compromise |
| Regular contractions <37w | 6+/hour, painful | Possible preterm labor |
| Suicidal/homicidal thoughts | Direct or indirect expression | Mental health emergency |
| Physical abuse | Injury pattern, partner violence | Safety emergency |

### Tier 3: Prompt Evaluation (Within 48 Hours)

| Indicator | Description | Rationale |
|-----------|-------------|------------|
| New-onset swelling | Mild, progressive | Possible early preeclampsia |
| Mild headache | Persistent, not severe | Monitor for progression |
| Spotting | Light pink/brown, not heavy | Possible placental issue |
| Decreased movement | Noticeable reduction but >10 in 2h | Possible early compromise |
| Elevated mood symptoms | Low mood, anxiety, worry | Possible perinatal depression |

## Procedure

### 1. Primary Scan (Run FIRST)

Before any other processing, scan the input for emergency indicators:

```python
# Pseudocode for scanning process
def scan_for_emergencies(text, profile):
    tier1_indicators = []
    tier2_indicators = []
    tier3_indicators = []

    # Check for Tier 1 emergencies
    if contains(text, ['bleeding heavy', 'soaking pad', 'passing clots']):
        tier1_indicators.append('heavy_bleeding')
    if contains(text, ['severe pain', 'constant intense', 'worse pain']):
        tier1_indicators.append('severe_pain')
    if contains(text, ['faint', 'pass out', 'lose consciousness']):
        tier1_indicators.append('syncope')
    if contains(text, ['seizure', 'convulsion']):
        tier1_indicators.append('seizure')
    if contains(text, ['no movement', 'no kicks', 'no baby moving']):
        tier1_indicators.append('no_fetal_movement')
    if contains(text, ['gush fluid', 'water broke', 'water broken']):
        tier1_indicators.append('premem_rupture')

    # Check for Tier 2 urgent
    if contains(text, ['headache', 'vision', 'blur', 'flash', 'aura']):
        tier2_indicators.append('preeclampsia_symptoms')
    if contains(text, ['swelling', 'puffy', 'edema', 'sudden']):
        tier2_indicators.append('swelling')
    if bp_high(text, profile) or contains(text, ['bp 160', 'blood pressure high']):
        tier2_indicators.append('hypertension')
    if contains(text, ['fever', 'chills', 'hot']):
        tier2_indicators.append('fever')
    if contains(text, ['less movement', 'decreased movement', 'fewer kicks']):
        tier2_indicators.append('decreased_movement')
    if contains(text, ['contraction', 'cramping', 'tightening']) and weeks < 37:
        tier2_indicators.append('preterm_labor')
    if contains(text, ['suicid', 'hurt myself', 'end it', 'want to die']):
        tier2_indicators.append('mental_health_crisis')
    if contains(text, ['abuse', 'hit', 'hurt', 'violent', 'scared of partner']):
        tier2_indicators.append('domestic_violence')

    return tier1_indicators, tier2_indicators, tier3_indicators
```

### 2. Emergency Escalation (Tier 1)

If ANY Tier 1 indicator is present:

**Step 2.1: IMMEDIATELY halt normal workflow**
- Stop all other processing
- Do not proceed to scoring or roadmap

**Step 2.2: Emit ONLY emergency guidance**

```markdown
## ⚠️ EMERGENCY — Call 911 or go to the nearest emergency room immediately.

### What's Happening
Your symptoms suggest a **medical emergency** that requires immediate evaluation.

### What To Do NOW
1. **Call 911** or have someone drive you to the **nearest hospital with labor & delivery**
2. Do **not** drive yourself if you're feeling dizzy, faint, or in severe pain
3. If you pass out or can't respond, emergency services need to find you

### What To Bring
- Your insurance card
- ID
- List of current medications
- This note about your symptoms

### What NOT To Do
- Do **not** wait to see if symptoms improve
- Do **not** try home remedies
- Do **not** delay seeking care

**This is a time-sensitive emergency. Every hour counts.**
```

**Step 2.3: Return ESCALATE status to harness**
- Harness must not proceed to guidance
- No scoring table, no roadmap

### 3. Urgent Clinical Escalation (Tier 2)

If any Tier 2 indicator is present (but no Tier 1):

**Step 3.1: Emit same-day clinical visit guidance**

```markdown
## ⚠️ URGENT — Contact your obstetrician or midwife TODAY

### What's Happening
Your symptoms require **same-day evaluation** by a prenatal care provider.

### What To Do NOW
1. **Call your obstetrician/midwife immediately**
2. If unable to reach, go to **labor & delivery triage** at your hospital
3. Do not wait until your next scheduled appointment

### What To Say
- "I am [X] weeks pregnant and experiencing [symptoms]."
- "I'm concerned about [preeclampsia / preterm labor / etc]."

### What To Expect
- Your provider will likely want you to come in for:
  - Blood pressure check
  - Fetal monitoring
  - Urine protein check
  - Ultrasound if needed

**Do not delay. These symptoms can progress quickly.**
```

**Step 3.2: Return ESCALATE status to harness**
- Harness may provide educational context AFTER escalation
- No self-help or home remedies in place of clinical care

### 4. Prompt Evaluation (Tier 3)

If only Tier 3 indicators (no Tier 1/2):

**Step 4.1: Emit prompt evaluation guidance**

```markdown
## Prompt Evaluation Recommended (Within 48 Hours)

Your symptoms suggest the need for **prompt clinical evaluation**. Contact your obstetrician or midwife within the next 24-48 hours to discuss.

### What To Do
- Call your provider's office to schedule an urgent visit
- Describe your symptoms clearly
- Ask about monitoring instructions while you wait

### Red-Flag Warning
If symptoms worsen or any of the following develop:
- [List Tier 1/2 symptoms specific to condition]

...seek immediate emergency care instead.
```

**Step 4.2: Return CLEAR-CAUTION status**
- Harness may proceed with educational content
- Must include symptom monitoring guidance

### 5. Safety Screen Clear (No Red Flags)

If no indicators detected:

**Step 5.1: Return CLEAR status**
- Harness proceeds to framework selection and scoring
- Educational guidance appropriate

**Step 5.2: Still include standard safety reminder**

```markdown
### Safety Reminder
If you experience any of these symptoms during pregnancy, seek care promptly:
- Vaginal bleeding (any amount)
- Severe headache or vision changes
- Sudden swelling in hands/face
- Fever >100.4°F
- Decreased fetal movement
- Regular contractions before 37 weeks

When in doubt, call your obstetrician or midwife.
```

## Outputs

### If ESCALATE (Tier 1/2)
- **Escalation guidance only** (no roadmap)
- Emergency/clinical resources
- **Status:** ESCALATE
- Harness does NOT proceed to guidance

### If CLEAR-CAUTION (Tier 3)
- Prompt evaluation guidance
- Symptom monitoring instructions
- **Status:** CLEAR-CAUTION
- Harness may proceed with caution

### If CLEAR (No red flags)
- Standard safety reminder
- **Status:** CLEAR
- Harness proceeds normally

## Quality Gate

**Pass conditions:**
- [ ] Tier 1 indicators → ESCALATE + emergency guidance only
- [ ] Tier 2 indicators → ESCALATE + same-day clinical guidance only
- [ ] Tier 3 indicators → CLEAR-CAUTION + prompt evaluation
- [ ] No indicators → CLEAR + safety reminder

**Fail conditions:**
- Red flag detected but guidance still emitted
- Emergency case but scoring/roadmap produced
- Self-help content provided for urgent symptoms

## Integration with Shared Cluster Template

This sub-skill implements `shared-safety-triage` from `.shared/cluster-shared-subskills.md`:
- Uses pregnancy-specific red-flag vocabulary
- Follows tiered escalation protocol
- Gates entire harness until CLEAR

## Mental Health Crisis Protocol

If suicidal/homicidal thoughts detected:

```markdown
## Mental Health Emergency — Help Is Available

If you are thinking about hurting yourself or others, please reach out now:

**Immediate Crisis Lines:**
- National Suicide Prevention Lifeline: **988** (US)
- Crisis Text Line: Text HOME to **741741**
- International: https://suicideprevention-lifeline.org

**What To Do:**
1. Call or text one of the crisis lines above
2. If immediate danger, call **911** or go to the nearest emergency room
3. Let your obstetrician know when you can — mental health is part of pregnancy care

**You are not alone. Help is available 24/7.**
```

## Next Stage
- **If ESCALATE:** Harness stops; no further stages
- **If CLEAR/CAUTION:** Proceeds to research → `sub-framework-selector`
