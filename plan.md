1. **Update `simulation.py` to add States 57 and 58 in arrays and dicts**
   - In `create_grid`, add 57 and 58 to `states`.
   - Add weights `0.005` (Yithian) and `0.005` (Flying Polyp) to the end of `weights`. Wait, Yithians are supposed to spawn? The instructions say "Flying Polyps spawn rarely (0.005%)" but don't specify Yithians. Let's make Yithians 0.005% too.
   - Update `chars` mapping to include `57: "Y"` and `58: "f"`. Let's pick appropriate chars.
   - Update `blocking_states` set to include 57 and 58.
   - Update `colorMap` inside the `const colors` string. We'll add 57 (Yithian, maybe `#DAA520` or something, wait `#DAA520` is Hastur. Let's use `#D2B48C` for Yithian and `#8B0000` is Nidhogg... let's use `#483D8B` for Flying Polyp). Let's use specific colors.

2. **Pre-Compute Yithian targets**
   - Find all positions of states 0, 1, 2, 3, 4, 39, 40 during the pre-computation loop and store them in `yithian_targets`.

3. **Implement Yithian (State 57) Logic**
   - If `random.random() < 0.02` and `yithian_targets` is not empty: Mind Swap!
   - `ty, tx = random.choice(yithian_targets)`
   - `new_grid[y][x] = grid[ty][tx]`
   - `global_modifications[(ty, tx)] = 57`
   - Else, random walk like state 55.

4. **Implement Flying Polyp (State 58) Logic**
   - Random walk.
   - Loop over neighbors. If `new_grid[cy][cx] in [0, 1, 2, 3, 4, 40, 57]`: `new_grid[cy][cx] = 6`.
   - `if random.random() < 0.01`: spawn 58 in an adjacent void.

5. **Update `agent_handover.md`**
   - Append Shift 47 describing Yithians and Flying Polyps.

6. **Complete pre commit steps to ensure proper testing, verification, review, and reflection are done.**
   - Run `pre_commit_instructions` and follow steps.
