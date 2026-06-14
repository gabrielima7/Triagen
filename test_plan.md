I need to add a new entity to the simulation.
Based on the `agent_handover.md` context, the previous agents added states up to 49 (`Dark Young`).

I will add **Deep One (State 50)** to continue the eldritch horror theme.
The Deep One will be an aquatic entity.

### Characteristics of Deep One (State 50)
- **Spawn rate:** Very rare (0.005%).
- **Movement:** Wanders randomly.
- **Interaction:**
  - Corrupts basic lifeforms (0-4) and Investigators (39) into Cultists (40) with a 10% chance.
  - If a Deep One encounters Cthulhu (37) or Sleeping Cthulhu (38), it reveres them and has a small chance (5%) to spawn another Deep One in an adjacent Void (6) tile.
- **Visualization:**
  - Color in HTML: `#008b8b` (DarkCyan)
  - Character in terminal: `p`
  - Solid blocker for Neutron Star beams.

### Plan
1.  **Modify `agent_handover.md`:** Append a new shift entry (Shift 43: Deep One) documenting the changes.
2.  **Modify `simulation.py` (State Arrays):**
    - Add `50` to `states` list (line 13).
    - Add `"Deep One (0.005%)"` to the comment on line 16.
    - Add `0.005` to `weights` list (line 18).
3.  **Modify `simulation.py` (Chars Dictionary):** Add `50: "p"` to `chars` (line 78).
4.  **Modify `simulation.py` (Blocking States):** Add `50` to `blocking_states` set (line 608).
5.  **Modify `simulation.py` (Logic):** Insert logic for State 50 (Deep One) before State 29 (line 1490).
6.  **Modify `simulation.py` (HTML Template):** Add `50: '#008b8b', // Deep One` to the `colors` mapping (line 1766).
7.  **Verification:** Verify all modifications in `simulation.py` and `agent_handover.md`.
8.  **Frontend Verification:** Run the simulation and use Playwright to verify the frontend.
9.  **Pre-commit:** Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
10. **Submit:** Commit the changes to the `deep-one` branch.
