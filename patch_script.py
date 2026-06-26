import re

with open("simulation.py", "r") as f:
    text = f.read()

# 1. Update states array
states_match = re.search(r'(states = \[.*?)(])', text)
if states_match:
    text = text[:states_match.end(1)] + ', 71' + text[states_match.end(1):]

# 2. Update weights array
weights_match = re.search(r'(weights = \[.*?)(])', text)
if weights_match:
    text = text[:weights_match.end(1)] + ', 0.005' + text[weights_match.end(1):]

# 3. Update Legend Comment
text = text.replace(
    'Yithian (0.005%), Flying Polyp (0.005%), Hound of Tindalos (0.005%)',
    'Yithian (0.005%), Flying Polyp (0.005%), Hound of Tindalos (0.005%), Spider of Leng (0.005%)'
)

# 4. Update chars dict
chars_match = re.search(r'(chars = \{.*?)(})', text)
if chars_match:
    text = text[:chars_match.end(1)] + ', 71: "8"' + text[chars_match.end(1):]

# 5. Update blocking states
blocking_match = re.search(r'(blocking_states = \{.*?)(})', text)
if blocking_match:
    text = text[:blocking_match.end(1)] + ', 71' + text[blocking_match.end(1):]

# 6. Add to main loop logic
logic = """
            # --- STATE 71: SPIDER OF LENG ---
            elif current_state == 71:
                new_grid[y][x] = 6 # Default to move/leave Void
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)

                moved = False

                # Preys on basic lifeforms, Investigators, and Cultists
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] in [0, 1, 2, 3, 4, 39, 40]:
                        new_grid[cy][cx] = 71
                        moved = True
                        break

                if not moved:
                    # Wander
                    for ny, nx in neighbors:
                        cy, cx = ny % height, nx % width
                        if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                            new_grid[cy][cx] = 71
                            moved = True
                            break

                if not moved:
                    new_grid[y][x] = 71 # Stay put
                continue
"""
# Replace "            else:" with logic + "\n            else:"
# making sure it's the one at the very end of the loop
# We can find the exact block:
else_block = """            else:
                # Evolve quantum non-local teleportation via Wormhole horizons if neighbor to one"""

text = text.replace(else_block, logic + "\n" + else_block)

# 7. Replace legend title
text = text.replace(
    'Abhoth, Glaaki</h2>',
    'Abhoth, Glaaki, Spider of Leng</h2>'
)

# 8. Replace legend description
text = text.replace(
    '| Crimson: Fed Star Vampire</p>',
    '| Crimson: Fed Star Vampire | Purple: Spider of Leng</p>'
)

# 9. Add to JavaScript dictionary
js_color_match = re.search(r"(70: '#dc143c' // Fed Star Vampire)(\n\s+)(}})", text)
if js_color_match:
    text = text[:js_color_match.start(2)] + ",\n            71: '#800080' // Spider of Leng" + text[js_color_match.start(2):]

with open("simulation.py", "w") as f:
    f.write(text)
