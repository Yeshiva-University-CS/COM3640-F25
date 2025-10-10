# Domain Requirements

## Overview
A streamlined clinical trial system focused on core workflow, state management, and outcome measurement.

---

## 1. Core Domain Entities

### 1.1 Clinical Trial
**Required Attributes:**
- trial_id: unique identifier (immutable - never changes)
- drug_name: name of drug being tested (immutable - set at creation)
- indication: disease/condition being treated (immutable - set at creation)
- minimum_age: minimum age for participant eligibility in years (immutable - set at creation)
- maximum_age: maximum age for participant eligibility in years (immutable - set at creation)
- target_enrollment: number of participants needed (mutable only in Planning state)
- current_state: lifecycle state (mutable - changes throughout trial lifecycle)

**Purpose:** Represents the entire trial from planning to completion

**Mutability Model:**
- **Immutable (set at trial creation):** trial_id, drug_name, indication, minimum_age, maximum_age
- **Planning state only:** target_enrollment can be modified
- **After Planning:** target_enrollment becomes locked
- **All states:** current_state changes through state transitions

**Design Rationale:**
A trial is fundamentally about testing a specific drug for a specific condition on a specific age group - these cannot change. During planning, you may adjust how many participants you need. Outcome strategies are not stored but passed as parameters when calculating results.

---

### 1.2 Participant
**Required Attributes:**
- participant_id: unique identifier
- date_of_birth: for age eligibility calculation
- screening_status: Accepted | Rejected
- enrollment_date: when enrolled (only for Accepted participants)
- assignment_group: null | Treatment | Control

**Purpose:** Represents a person who has been screened for the trial

**Screening Status:**
- **Accepted:** Participant met age eligibility criteria and was enrolled in the trial
- **Rejected:** Participant did not meet age eligibility criteria and was not enrolled

**Key Behaviors:**
- Age calculated from date_of_birth must fall within trial's minimum_age and maximum_age for Accepted status
- Participants with Rejected status count toward screening totals but are not enrolled
- Can be randomized to treatment groups only after baseline visit is recorded (Accepted participants only)
- A participant can only be screened once (cannot re-screen the same participant_id)

---

### 1.3 Visit
**Required Attributes:**
- visit_id: unique identifier
- participant: reference to participant (must be Accepted status)
- visit_type: Baseline | Week4 | Week8 | Week12 | Final
- appointment_date: when the visit occurred (required)
- measurements: dictionary containing specific measurements (see below)

**Measurements Structure:**
All visits collect the following four measurements:
- `symptom_severity`: integer 0-10 (0 = no symptoms, 10 = severe symptoms)
- `blood_pressure_systolic`: integer (e.g., 120, 140, 160 mmHg)
- `weight`: decimal (e.g., 165.5 lbs or 75.2 kg)
- `symptom_free`: boolean (true if participant is symptom-free, false otherwise)

**Purpose:** Represents a completed data collection point

**Key Rules:**
- Visits can only be recorded for Accepted participants
- Visits are recorded after they occur (appointment_date is when visit happened)
- Baseline visit recorded during Recruiting state
- Follow-up visits (Week4, Week8, etc.) can only be recorded for randomized participants
- Follow-up visits can only be recorded when trial is in Active state
- Baseline must be recorded before randomization
- Visit dates must be chronologically valid (after enrollment_date)
- All four core measurements must be collected at every visit

---

### 1.4 Outcome Measurement Strategies
Different approaches to measuring trial success. All strategies analyze participants separated by treatment group and return results for both Treatment and Control groups.

**Binary Outcome Strategy:**
- Measures: Success or Failure (participant achieved symptom relief)
- Uses: `symptom_free` measurement from Final visit
- Calculates: success_rate = (participants with symptom_free=true / total_participants) × 100
- Returns: Treatment group success rate AND Control group success rate
- Example output: "Treatment: 70% achieved relief, Control: 45% achieved relief"

**Continuous Outcome Strategy:**
- Measures: Numeric change in a single measurement
- Uses: One measurement from Baseline and Final visits
- Can measure change in: `symptom_severity`, `blood_pressure_systolic`, or `weight`
- Calculates: mean_change = average(baseline_value - final_value)
- Returns: Treatment group mean change AND Control group mean change
- Example output: "Treatment: Average reduction of 5.2 points, Control: Average reduction of 2.1 points"

**Time-to-Event Strategy:**
- Measures: Days until symptom relief occurs
- Uses: All visits' `symptom_free` and `appointment_date` fields to find first occurrence
- Calculates: 
  - For each participant, find first visit where symptom_free = true
  - Calculate days_to_first_relief = (first_symptom_free_visit.appointment_date - enrollment_date)
  - median_time = median(days_to_first_relief for participants who achieved relief)
- Excludes participants who never achieved symptom_free = true
- Returns: Treatment group median days AND Control group median days
- Example output: "Treatment: Median 21 days to relief, Control: Median 42 days to relief"

**Weighted Continuous Outcome Strategy:**
- Measures: Combined numeric changes across multiple measurements
- Uses: Multiple measurements from Baseline and Final visits
- Can combine any of: symptom_severity change, blood_pressure_systolic change, weight change
- Each measurement has an associated weight (must sum to 1.0)
- All measurements normalized to same scale (e.g., percent change from baseline or standard deviations)
- Calculates: weighted_score = Σ(normalized_measurement_change × weight)
- Returns: Treatment group weighted score AND Control group weighted score
- Example: 40% symptom severity reduction + 30% blood pressure reduction + 30% weight change
- Example output: "Treatment: Weighted score 0.68, Control: Weighted score 0.42"

---

## 2. State Machine: Clinical Trial Lifecycle

Trials progress through states with strict rules about what operations are allowed.

```
Planning → Recruiting → Active → Completed
               ↓
          Terminated
```

### State 1: Planning (Initial State)
**Purpose:** Protocol design and preparation

**Allowed Operations:**
- Set/modify target_enrollment (adjust how many participants needed)

**Restrictions:**
- CANNOT change drug_name or indication (set at creation)
- CANNOT screen or enroll participants
- CANNOT randomize
- CANNOT record visits

**Business Rules:**
- Must set target_enrollment > 0 before transitioning to Recruiting

**Transitions:**
- → Recruiting (when protocol is ready)

---

### State 2: Recruiting
**Purpose:** Screening and enrolling participants

**Allowed Operations:**
- Screen potential participants for age eligibility (creates participant record)
- Record Baseline visits for Accepted participants (after they occur)

**Restrictions:**
- CANNOT randomize participants (must reach Active state first)
- CANNOT record follow-up visits (Week4, Week8, etc.)
- CANNOT change target_enrollment (protocol now locked)
- CANNOT screen the same participant twice (by participant_id)

**Business Rules:**
- Screening creates a participant record with screening_status:
  - **Accepted:** Age (calculated from date_of_birth) falls within trial's minimum_age and maximum_age; participant is enrolled with enrollment_date
  - **Rejected:** Age outside eligibility range; participant is NOT enrolled, has no enrollment_date
- Both Accepted and Rejected participants count toward total screened
- Must reach target_enrollment of **Accepted** participants before transitioning to Active
- Each Accepted participant must have Baseline visit recorded before randomization

**Transitions:**
- → Active (when target_enrollment of Accepted participants reached AND ready to begin treatment)
- → Terminated (if 2 × target_enrollment participants **screened** without reaching target_enrollment of **Accepted** participants)

---

### State 3: Active
**Purpose:** Treating participants and collecting data

**Allowed Operations:**
- Record Baseline visits for Accepted participants
- Randomize Accepted participants (after their Baseline visit is recorded)
- Record follow-up visits (Week4, Week8, Week12, Final) for randomized participants

**Restrictions:**
- CANNOT screen new participants (screening phase complete)
- CANNOT run final outcome analysis (trial must complete first)
- CANNOT change target_enrollment (configuration locked)
- CANNOT modify completed visit data

**Business Rules:**
- Only Accepted participants can be randomized
- Randomization assigns to Treatment or Control group (balanced assignment)
- Once randomized, assignment is permanent
- Follow-up visits must be recorded in chronological order

**Transitions:**
- → Completed (when all Accepted participants have Final visit recorded)

---

### State 4: Completed (Terminal State)
**Purpose:** All data collection finished, final analysis

**Allowed Operations:**
- Lock all participant data (read-only)
- Calculate outcomes by passing strategies - each strategy returns separate results for Treatment and Control groups
- Compare Treatment vs Control group outcomes
- Generate final trial report

**Restrictions:**
- CANNOT screen new participants
- CANNOT randomize participants
- CANNOT record new visits
- CANNOT change target_enrollment (configuration locked)
- This is a terminal state (no transitions out)

**Business Rules:**
- All Accepted participants must have Final visit recorded
- Only Accepted participants are included in outcome analysis
- Can calculate outcomes multiple times with different strategies
- Each strategy returns separate results for Treatment and Control groups for comparison

---

### State 5: Terminated (Terminal State)
**Purpose:** Trial ended early due to insufficient enrollment

**Allowed Operations:**
- Lock all data
- Generate termination report with available data

**Restrictions:**
- CANNOT screen new participants
- CANNOT collect new data
- This is a terminal state (no transitions out)

**Business Rules:**
- Trial automatically terminates if 2 × target_enrollment participants have been **screened** (Accepted + Rejected) without reaching target_enrollment of **Accepted** participants
- Only Accepted participants are included in available data

---

## 3. Business Workflows

### Workflow 1: Participant Screening and Enrollment
**State:** Recruiting only

1. Screen participant by checking if participant_id has been screened before
2. If already screened (Accepted or Rejected) → Reject screening attempt with error
3. Calculate participant's age from date_of_birth
4. Check age against trial's minimum_age and maximum_age:
   - **If age is within range:**
     - Create participant record with screening_status = Accepted
     - Set enrollment_date to current date
     - Participant counts toward target_enrollment
   - **If age is outside range:**
     - Create participant record with screening_status = Rejected
     - No enrollment_date (not enrolled)
     - Participant does NOT count toward target_enrollment
5. Both Accepted and Rejected participants count toward total screened
6. Record Baseline visit for Accepted participants (after it occurs)

**Validation:**
- Cannot screen same participant_id twice
- Trial must be in Recruiting state

---

### Workflow 2: Randomization
**State:** Active only

1. Verify participant has screening_status = Accepted
2. Verify participant has Baseline visit recorded
3. Randomly assign to Treatment or Control group
4. Assignment is permanent
5. Participant now eligible for follow-up visits

**Validation:**
- Can only randomize Accepted participants
- Cannot randomize same participant twice
- Maintain balance (roughly equal group sizes)

---

### Workflow 3: Visit Data Recording
**State:** Recruiting (Baseline only) or Active (all visits)

1. Verify participant has screening_status = Accepted
2. Verify participant has been randomized
3. Create Visit record for the participant
4. Set appointment_date to when visit occurred
5. Enter all four required measurements:
   - symptom_severity (0-10)
   - blood_pressure_systolic (integer)
   - weight (decimal)
   - symptom_free (boolean)

**Validation:**
- Can only record visits for Accepted participants who are randomized
- Participant must not have all visits recorded yet
- Visit dates must be in chronological order

---

### Workflow 4: Outcome Analysis
**State:** Completed only

The trial calculates outcomes by passing different outcome strategies:

**Process:**
1. Pass an outcome strategy to the trial's analysis capability
2. Strategy receives all Accepted participants (Rejected participants excluded)
3. Strategy separates Accepted participants by Treatment vs Control group
4. Strategy calculates result for Treatment group
5. Strategy calculates result for Control group
6. Strategy returns both results for comparison
7. Can perform analysis multiple times with different strategies

**Strategy Return Value:**
- Each strategy returns results for BOTH groups
- Treatment group result and Control group result
- Enables direct comparison between groups
- Only Accepted participants are included in analysis

---