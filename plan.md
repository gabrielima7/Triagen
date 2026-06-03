1. **Fix the Exponential Replication Bug for Leviathans**
   - The code review pointed out that the check `if (y, x) in leviathans and (y, x) not in leviathan_targets.values(): new_grid[y][x] = 6` is flawed. The check causes them to clone instead of move.
   - I need to change it simply to `if (y, x) in leviathans: new_grid[y][x] = 6`. Because stationary Leviathans stay in place via `leviathan_targets[(ly, lx)] = (ly, lx)`, which is caught by the check right above it: `if (y, x) in leviathan_targets: new_grid[y][x] = 33`. So if a cell was a leviathan but not targeted by anything, it should just be left as a void (6).
2. **Execute Simulation to verify the fix**
   - Run `python simulation.py` to make sure it doesn't crash and the logic is fixed.
3. **Run Code Review Again**
   - Request another code review.
4. **Initiate Memory Recording**
   - Document the cellular automaton movement resolution pattern.
5. **Complete pre-commit steps**
   - Mark the step as complete.
