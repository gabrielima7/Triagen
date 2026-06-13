import re

with open('simulation.py', 'r') as f:
    content = f.read()

new_logic = """
            # --- STATE 48: SHUB-NIGGURATH ---
            elif current_state == 48:
                new_grid[y][x] = 6 # Default to move/leave Void
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)
                moved = False
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                        new_grid[cy][cx] = 48
                        moved = True
                        break
                if not moved:
                    new_grid[y][x] = 48

                if random.random() < 0.05:
                    for ny, nx in neighbors:
                        cy, cx = ny % height, nx % width
                        if new_grid[cy][cx] in [0, 1, 2, 3, 4, 6]:
                            new_grid[cy][cx] = 49
                            break
                continue

            # --- STATE 49: DARK YOUNG ---
            elif current_state == 49:
                new_grid[y][x] = 6 # Default to move/leave Void
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)
                moved = False
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                        new_grid[cy][cx] = 49
                        moved = True
                        break
                if not moved:
                    new_grid[y][x] = 49

                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if new_grid[cy][cx] in [0, 1, 2, 3, 4] and random.random() < 0.10:
                        new_grid[cy][cx] = 40
                continue
"""

# Insert before State 29
content = content.replace(
    '            # --- STATE 29: RADIOTROPH ---',
    new_logic.lstrip('\n') + '            # --- STATE 29: RADIOTROPH ---'
)

with open('simulation.py', 'w') as f:
    f.write(content)
