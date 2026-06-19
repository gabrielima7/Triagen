import re

with open('simulation.py', 'r') as f:
    content = f.read()

# Update states list
content = re.sub(
    r'(states = \[[0-9, ]+)60\]',
    r'\g<1>60, 61]',
    content
)

# Update weights list
content = re.sub(
    r'(weights = \[[0-9., ]+)0\.005\]',
    r'\g<1>0.005, 0.005]',
    content
)

# Update chars dictionary
content = re.sub(
    r'(59: "T", 60: "E")}',
    r'\g<1>, 61: "N"}',
    content
)

# Update blocking_states set
content = re.sub(
    r'(blocking_states = \{[0-9, ]+)60\}',
    r'\g<1>60, 61}',
    content
)

# Update Legend HTML string
content = re.sub(
    r'(Elder Thing)</p>',
    r'\1 | Indigo: Nightgaunt</p>',
    content
)

# Update Title HTML string
content = re.sub(
    r'(Elder Thing)</h2>',
    r'\1, Nightgaunt</h2>',
    content
)

# Update JavaScript colors object
content = re.sub(
    r'(60: \'#2e8b57\')(  // Elder Thing)\n(        \}\};)',
    r"\1,\2\n            61: '#4B0082' // Nightgaunt\n\3",
    content
)

# Add State 61 Logic block before returning new_grid
state_61_logic = """
            # --- STATE 61: NIGHTGAUNT ---
            elif current_state == 61:
                new_grid[y][x] = 6 # Default to move/leave Void
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)

                moved = False
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] in [0, 1, 2, 3, 4, 39, 40]:
                        if available_voids:
                            target_y, target_x = random.choice(available_voids)
                            available_voids.remove((target_y, target_x))
                            # Move victim
                            teleportation_targets[(target_y, target_x)] = grid[cy][cx]
                            new_grid[cy][cx] = 6 # Replace victim with void
                        new_grid[cy][cx] = 61 # Move nightgaunt to victim's original spot
                        moved = True
                        break

                if not moved:
                    # Wander randomly to a void space
                    for ny, nx in neighbors:
                        cy, cx = ny % height, nx % width
                        if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                            new_grid[cy][cx] = 61
                            moved = True
                            break
                if not moved:
                     new_grid[y][x] = 61 # Stay put if can't move
                continue
"""

content = re.sub(
    r'(            else:\n                # Evolve quantum non-local teleportation via Wormhole horizons if neighbor to one)',
    state_61_logic + r'\n\1',
    content
)

with open('simulation.py', 'w') as f:
    f.write(content)
