1. **Edit `simulation.py` to add state 29 to `states` and `weights`**
   - At line 13, add `29` to the `states` array.
   - At line 15, add a weight of `0.005` to the `weights` array.
2. **Verify step 1**
   - Run `grep -C 2 "states =" simulation.py` to ensure the updates to states and weights are correct.
3. **Edit `simulation.py` to add state 29 to `blocking_states`**
   - At line 591, add `29` to the `blocking_states` set.
4. **Verify step 3**
   - Run `grep -C 2 "blocking_states" simulation.py` to verify the update.
5. **Edit `simulation.py` to insert the beam interaction logic for Radiotrophs**
   - Around line 753, inside the loop over the grid, add logic to handle `current_state == 29`.
   - If a Radiotroph is targeted by a beam (`(y, x) in beam_targets`), it survives and spreads to adjacent Void (State 6) cells. Add the new position to `new_grid`.
   - If not targeted by a beam, there is a chance (e.g. 5%) it decays to Void (State 6).
   - Also, update the beam effect logic so that if the `current_state` is 29, it does not turn into a Pulsar (state 8).
6. **Verify step 5**
   - Run `grep -C 5 "== 29" simulation.py` to verify the new logic.
7. **Edit `simulation.py` to add state 29 to the HTML template colors**
   - Around line 1118, add `29: '#7fff00'  // Radiotroph` to the template string generating `const colors` in the `generate_html` function.
8. **Verify step 7**
   - Run `grep -C 2 "'#7fff00'" simulation.py` to verify the new color assignment.
9. **Update `agent_handover.md`**
   - Append a new section for Shift 26 introducing Radiotrophs, their behavior, and color.
10. **Verify step 9**
    - Run `tail -n 20 agent_handover.md` to ensure the handover log was updated correctly.
11. **Run Core Simulation**
    - Execute `python simulation.py` to verify the changes don't break the main loop and `state.json` and `index.html` update correctly.
12. **Frontend Verification**
    - Follow `frontend_verification_instructions` and execute the Playwright script to visually verify `index.html`.
13. **Complete pre-commit steps**
    - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
14. **Submit the change**
    - Submit the branch to save the introduction of Radiotrophs.
