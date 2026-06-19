import re

with open("simulation.py", "r") as f:
    content = f.read()

# 1. states array
content = content.replace("59, 60, 61]", "59, 60, 61, 62]")

# 2. weights array
content = content.replace("0.005, 0.005, 0.005, 0.005, 0.005]", "0.005, 0.005, 0.005, 0.005, 0.005, 0.005]")

# 3. chars dict
content = content.replace("61: \"N\"}", "61: \"N\", 62: \"g\"}")

# 4. blocking_states
content = content.replace("59, 60, 61}", "59, 60, 61, 62}")

# 5. HTML H2
content = content.replace("Elder Thing, Nightgaunt</h2>", "Elder Thing, Nightgaunt, Gug</h2>")

# 6. HTML P
content = content.replace("Elder Thing | Indigo: Nightgaunt</p>", "Elder Thing | Indigo: Nightgaunt | Dark Brown: Gug</p>")

# 7. Colors
content = content.replace("61: '#4B0082' // Nightgaunt\n        }};", "61: '#4B0082', // Nightgaunt\n            62: '#5c4033' // Gug\n        }};")

# 8. Logic
logic = """
            # --- STATE 62: GUG ---
            elif current_state == 62:
                new_grid[y][x] = 6 # Default to move/leave Void
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)

                moved = False
                # Fear Nightgaunts (61)
                has_nightgaunt = any(grid[ny % height][nx % width] == 61 for ny, nx in neighbors)

                if has_nightgaunt:
                    # Flee to void
                    for ny, nx in neighbors:
                        cy, cx = ny % height, nx % width
                        if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                            new_grid[cy][cx] = 62
                            moved = True
                            break
                else:
                    # Eat prey
                    for ny, nx in neighbors:
                        cy, cx = ny % height, nx % width
                        if grid[cy][cx] in [0, 1, 2, 3, 4, 39, 40, 41, 50]:
                            new_grid[cy][cx] = 62
                            moved = True
                            break

                    if not moved:
                        # Wander
                        for ny, nx in neighbors:
                            cy, cx = ny % height, nx % width
                            if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                                new_grid[cy][cx] = 62
                                moved = True
                                break

                if not moved:
                    new_grid[y][x] = 62 # Stay put
                continue

            else:
                # Evolve quantum non-local teleportation via Wormhole horizons if neighbor to one"""

content = content.replace("\n            else:\n                # Evolve quantum non-local teleportation via Wormhole horizons if neighbor to one", logic)

with open("simulation.py", "w") as f:
    f.write(content)

print("Patch applied.")
