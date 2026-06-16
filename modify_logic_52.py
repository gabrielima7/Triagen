import re

with open('simulation.py', 'r') as f:
    content = f.read()

new_logic = """
            # --- STATE 52: THE COLOR OUT OF SPACE ---
            elif current_state == 52:
                new_grid[y][x] = 6 # Default to move/leave Void
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)
                moved = False
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                        new_grid[cy][cx] = 52
                        moved = True
                        break
                if not moved:
                    new_grid[y][x] = 52
                else:
                    if random.random() < 0.20:
                        new_grid[y][x] = 53 # Leave behind Blighted Soil
                continue

            # --- STATE 53: BLIGHTED SOIL ---
            elif current_state == 53:
                new_grid[y][x] = 53 # Remains static
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if new_grid[cy][cx] in [0, 1, 2, 3, 4] and random.random() < 0.15:
                        new_grid[cy][cx] = 54
                continue

            # --- STATE 54: ASHEN DUST ---
            elif current_state == 54:
                if random.random() < 0.05:
                    new_grid[y][x] = 6
                else:
                    new_grid[y][x] = 54
                continue
"""

content = content.replace(
    '            # --- STATE 29: RADIOTROPH ---',
    new_logic.lstrip('\n') + '            # --- STATE 29: RADIOTROPH ---'
)

with open('simulation.py', 'w') as f:
    f.write(content)
