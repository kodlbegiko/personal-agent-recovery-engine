# Validation Report

Validation used 120 fixed cases (seed 2202). Under the frozen safety-first selection rule:

- Candidate-v1 Recovery Success Rate: **0.85**.
- Candidate-v2 Recovery Success Rate: **0.875**.
- Candidate-v3 Recovery Success Rate: **0.875**.
- Candidate-v2 and Candidate-v3 were identical on benign-state preservation (1.00), duplicate side-effect rate (0.00), and mean recovery actions (0.8083).
- The frozen simplicity tie-break therefore selected **Candidate-v2**.
- Strongest safety-eligible baseline selected for protected comparison: **B0 No Recovery** (validation Recovery Success Rate 0.60).

Protected data was not used for candidate selection.
