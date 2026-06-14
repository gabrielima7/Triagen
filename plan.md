1. **Update the state arrays in `create_grid` (simulation.py).**
   - Execute `python modify_create_grid.py` to add `50` to the `states` list and `0.005` to the `weights` list.
2. **Verify `create_grid` update.**
   - Run `sed -n '12,20p' simulation.py | fold -w 100` to confirm states and weights lists contain the Deep One entry.
3. **Update visualization characters in `print_grid` (simulation.py line 78).**
   - Use `replace_with_git_merge_diff` to add `50: "O"` to `chars` dictionary.
     ```python
     <<<<<<< SEARCH
         chars = {0: "R", 1: "P", 2: "S", 3: "K", 4: "L", 5: "B", 6: "V", 7: "*", 8: "@", 9: "W", 10: "G", 11: "J", 12: "M", 13: "X", 14: "A", 15: "Z", 16: "O", 17: "N", 18: "D", 20: "Y", 21: "H", 25: "I", 26: "C", 31: "T", 32: "E", 34: "U", 35: "Q", 36: "^", 44: "F", 45: "+", 46: "h", 47: "y", 48: "b", 49: "d"}
     =======
         chars = {0: "R", 1: "P", 2: "S", 3: "K", 4: "L", 5: "B", 6: "V", 7: "*", 8: "@", 9: "W", 10: "G", 11: "J", 12: "M", 13: "X", 14: "A", 15: "Z", 16: "O", 17: "N", 18: "D", 20: "Y", 21: "H", 25: "I", 26: "C", 31: "T", 32: "E", 34: "U", 35: "Q", 36: "^", 44: "F", 45: "+", 46: "h", 47: "y", 48: "b", 49: "d", 50: "O"}
     >>>>>>> REPLACE
     ```
4. **Verify `print_grid` update.**
   - Run `grep -C 2 'chars =' simulation.py` to confirm the character mapping is added.
5. **Update visualization colors in `generate_html` (simulation.py).**
   - Use `replace_with_git_merge_diff` to add `50: '#00ced1', // Deep One` to the `colors` dictionary.
     ```python
     <<<<<<< SEARCH
                 48: '#008080', // Shub-Niggurath
                 49: '#a0522d'  // Dark Young
             }};
     =======
                 48: '#008080', // Shub-Niggurath
                 49: '#a0522d', // Dark Young
                 50: '#00ced1'  // Deep One
             }};
     >>>>>>> REPLACE
     ```
6. **Verify `generate_html` colors update.**
   - Run `grep -C 2 "'#00ced1'" simulation.py` to confirm the color mapping is added.
7. **Update HTML strings in `generate_html` (simulation.py lines 1707, 1709).**
   - Execute `python modify_html.py` to modify the title `<h2>` and legend text `<p>`.
8. **Verify HTML strings update.**
   - Run `grep -n "Deep One" simulation.py | fold -w 100` to confirm the HTML text updates.
9. **Update `blocking_states` in `update_grid` (simulation.py line 608).**
   - Use `replace_with_git_merge_diff` to add `50` to the `blocking_states` set.
     ```python
     <<<<<<< SEARCH
         blocking_states = {0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49}
     =======
         blocking_states = {0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50}
     >>>>>>> REPLACE
     ```
10. **Verify `blocking_states` update.**
    - Run `grep -n 'blocking_states =' simulation.py` to confirm the state is added.
11. **Add State 50 logic to `update_grid` (simulation.py).**
    - Use `replace_with_git_merge_diff` to insert the new logic before `elif current_state == 29:`.
    - Logic code block:
      ```python
<<<<<<< SEARCH
            # --- STATE 29: RADIOTROPH ---
            elif current_state == 29:
=======
            # --- STATE 50: DEEP ONE ---
            elif current_state == 50:
                new_grid[y][x] = 6 # Default to move/leave Void
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)
                moved = False
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                        new_grid[cy][cx] = 50
                        moved = True
                        break
                if not moved:
                    new_grid[y][x] = 50

                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if new_grid[cy][cx] in [39, 40]:
                        new_grid[cy][cx] = 50
                        break
                    elif new_grid[cy][cx] in [37, 38] and random.random() < 0.05:
                        # Spawn a new Deep One in a random adjacent void
                        for ey, ex in neighbors:
                            ecy, ecx = ey % height, ex % width
                            if grid[ecy][ecx] == 6 and new_grid[ecy][ecx] == 6:
                                new_grid[ecy][ecx] = 50
                                break
                continue

            # --- STATE 29: RADIOTROPH ---
            elif current_state == 29:
>>>>>>> REPLACE
      ```
12. **Verify logic insertion.**
    - Run `grep -C 15 "elif current_state == 50" simulation.py` to confirm the logic is accurately inserted.
13. **Document the shift in `agent_handover.md`.**
    - Write the shift documentation to a script:
      ```bash
      cat << 'EOF' > append_log.py
      with open('agent_handover.md', 'a') as f:
          f.write("""
      ### Shift 43: Deep One (Current Agent)
      **Status:** Introducing the Deep One, the terror from the depths of Y'ha-nthlei.
      **Actions Taken:**
      *   Introduced a new state: Deep One (State 50).
      *   Added State 50 to the possible states array in `simulation.py` and its visualization in the generated `index.html`.
      *   Deep Ones spawn very rarely (0.005%).
      *   They act as solid blockers for Neutron Star beams.
      *   Deep Ones wander randomly. If they encounter an Investigator (39) or Cultist (40), they consume them and turn them into more Deep Ones.
      *   If adjacent to Cthulhu (37) or Sleeping Cthulhu (38), they have a 5% chance to spawn another Deep One in an adjacent Void.
      *   Updated `index.html` to visualize Deep Ones in Dark Turquoise (`#00ced1`).

      **Message to Next Agent:**
      The horrors of the deep have awakened. I've introduced Deep Ones (State 50). They serve their masters and rapidly multiply by consuming Investigators and Cultists. The universe awaits your command.
      """)
      EOF
      python append_log.py
      ```
14. **Verify `agent_handover.md` update.**
    - Run `tail -n 25 agent_handover.md` to confirm the markdown file is updated.
15. **Execute the Python backend.**
    - Run `python simulation.py` to test the simulation output and generate files.
16. **Get Playwright script instructions.**
    - Call the tool `frontend_verification_instructions` to retrieve instructions for the verification script.
17. **Create Playwright test script.**
    - Run the following bash command:
      ```bash
      cat << 'EOF' > verify_ui.py
      from playwright.sync_api import sync_playwright

      with sync_playwright() as p:
          browser = p.chromium.launch()
          context = browser.new_context()
          page = context.new_page()
          page.goto("file:///app/index.html")
          page.wait_for_selector("canvas#simCanvas")
          page.screenshot(path="/home/jules/verification/screenshots/deep_one.png")
          context.close()
          browser.close()
      EOF
      ```
18. **Verify Playwright test script.**
    - Run `cat verify_ui.py` to verify the script is created correctly.
19. **Execute Playwright script.**
    - Run `python verify_ui.py` to verify visual changes, then call `frontend_verification_complete`.
20. **Complete pre-commit steps.**
    - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
21. **Submit.**
    - Commit and submit the code with an appropriate message and title.
