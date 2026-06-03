1. **Explore `simulation.py` structure for inserting Leviathan (State 33).**
   - Need to insert Leviathan in:
     - `create_grid` weighted list and weights.
     - `update_grid` pre-computation loop.
     - `update_grid` resolution phase (`# 2.13 RESOLVE LEVIATHAN MOVEMENT`).
     - `generate_html` for visualization.
   - Leviathan mechanics: seeks White Holes (32). If it consumes one, it emits a shockwave turning nearby entities into Void (6).
2. **Update `create_grid` logic.**
   - Add state `33` to `states` list.
   - Append `0.005` to `weights` list.
3. **Update `update_grid` Pre-computation.**
   - Add `leviathans = []`.
   - Add `elif state == 33: leviathans.append((y, x))` in the state scanning loop.
4. **Implement Leviathan Resolution Logic.**
   - Insert under `# 2.13 RESOLVE LEVIATHAN MOVEMENT`.
   - Leviathans move towards nearest White Hole (32) or move randomly if none exist.
   - If they land on a White Hole, they consume it and create a 3x3 shockwave of Voids (6).
5. **Update State Processing loop.**
   - Add `elif current_state == 33:` block to persist the Leviathan if it didn't move during the resolution phase.
6. **Update `generate_html`.**
   - Add `33: '#00008b' // Leviathan` to `colors` dict in JS.
   - Add Leviathan to the legend text.
7. **Document in `agent_handover.md`.**
   - Append my shift to the file outlining the addition of the Leviathan.
8. **Verify UI.**
   - Run the frontend verification process.
9. **Complete pre-commit steps.**
   - "Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done."
10. **Submit.**
