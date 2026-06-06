1. **Introduce State 37: Cthulhu**
   - Add Cthulhu (State 37) to the possible states array (`states = [0...37]`) in `create_grid`.
   - Add Cthulhu to the HTML generation script with color `#006400` (Dark Green).
   - Add Cthulhu's character `C` to `chars` mapping in `print_grid`.
   - Update the weights in `create_grid` to include Cthulhu with a 0.005% spawn chance, adjusting `Void` chance to keep the total at 100%.

2. **Cthulhu Mechanics**
   - Cthulhu is the apex predator of the Kraken.
   - Spawn: Cthulhu spawns rarely during initialization.
   - Behavior: If Cthulhu finds a Kraken adjacent, it consumes it, turning into a Void. It immediately spawns a new Cthulhu in an adjacent Void cell (reproduction).
   - If there is no Kraken to consume, Cthulhu will wander aimlessly into an adjacent Void space (10% chance per turn).
   - Sleep mechanic: If Cthulhu does not consume a Kraken in a turn, it has a 1% chance to fall asleep for 100 turns. When asleep, it acts as a normal blocker and doesn't move or hunt. I will implement this simply as a new state (State 38: Sleeping Cthulhu, `#2e8b57` Sea Green).
   - Sleeping Cthulhu (State 38) acts exactly like a Black Monolith but awakens back into Cthulhu (State 37) with a 1% chance each turn.
   - Update `blocking_states` to include 37 and 38.

3. **Modify `simulation.py` to handle Cthulhu and Sleeping Cthulhu states**
   - In `update_grid` PRE-COMPUTATION phase, track Cthulhus and Sleeping Cthulhus.
   - Implement the logic for States 37 and 38 in the MAIN CELLULAR AUTOMATON UPDATE PASS.

4. **Update `agent_handover.md`**
   - Log Shift 34 detailing the introduction of Cthulhu (State 37) and Sleeping Cthulhu (State 38) to continue the chaotic evolution.

5. **Verify changes**
   - Run `python simulation.py` to ensure it executes without errors.
   - Run `python verify_frontend.py` to verify visualization.

6. **Complete pre-commit steps**
   - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.

7. **Submit the change.**
   - Once all tests pass, submit the change with a descriptive commit message.
