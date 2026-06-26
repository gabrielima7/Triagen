import re

with open("simulation.py", "r") as f:
    text = f.read()

# I need to add Spider of Leng logic
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
if "elif current_state == 71" not in text:
    text = text.replace("            else:", logic + "\n            else:")

with open("simulation.py", "w") as f:
    f.write(text)
