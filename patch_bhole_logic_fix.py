import re

with open("simulation.py", "r") as f:
    text = f.read()

# Locate insertion point using regex or string
# The insertion point from before:
#                if not moved:
#                    new_grid[y][x] = 62 # Stay put
#                continue
#
#            else:
#                # Evolve quantum non-local teleportation

insertion_point = """                if not moved:
                    new_grid[y][x] = 62 # Stay put
                continue"""

logic = """                if not moved:
                    new_grid[y][x] = 62 # Stay put
                continue

            # --- STATE 63: BHOLE ---
            elif current_state == 63:
                new_grid[y][x] = 53 # Leave behind Blighted Soil (53)
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)

                moved = False

                # Eat Gugs, Deep Ones, Nightgaunts, Void, Investigator, Cultists, Shoggoth
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] in [62, 50, 61, 6, 39, 40, 41] and new_grid[cy][cx] not in [63]:
                        new_grid[cy][cx] = 63
                        moved = True
                        break

                if not moved:
                    new_grid[y][x] = 63 # Stay put
                continue"""

if insertion_point in text:
    text = text.replace(insertion_point, logic)
    print("Injected logic!")
else:
    print("Could not find insertion point!")

with open("simulation.py", "w") as f:
    f.write(text)
