import re

with open('simulation.py', 'r') as f:
    content = f.read()

bhole_logic = """
            # --- STATE 63: BHOLE ---
            elif current_state == 63:
                new_grid[y][x] = 53 # Leaves Blighted Soil instead of Void by default
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)

                moved = False
                # Consume specific entities
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] in [41, 50, 51, 62]:
                        new_grid[cy][cx] = 63
                        moved = True
                        break

                if not moved:
                    # Move to adjacent void
                    for ny, nx in neighbors:
                        cy, cx = ny % height, nx % width
                        if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                            new_grid[cy][cx] = 63
                            moved = True
                            break

                if not moved:
                    new_grid[y][x] = 63 # Stay put
                continue
"""

content = content.replace(
    "                if not moved:\n                    new_grid[y][x] = 62 # Stay put\n                continue",
    "                if not moved:\n                    new_grid[y][x] = 62 # Stay put\n                continue\n" + bhole_logic
)

with open('simulation.py', 'w') as f:
    f.write(content)
