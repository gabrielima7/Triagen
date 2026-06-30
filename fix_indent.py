import re

with open("simulation.py", "r") as f:
    content = f.read()

# Let's fix the logic_block indentation we messed up
logic_block_wrong = """            elif current_state == 83:
                new_grid[y][x] = 6 # Default to move/leave Void
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)
                moved = False

                outer_gods = [42, 43, 45, 48, 82]
                near_god = any(grid[ny % height][nx % width] in outer_gods for ny, nx in neighbors)

                if near_god:
                    # Their maddening music lures mortals
                    for ny, nx in neighbors:
                        cy, cx = ny % height, nx % width
                        if grid[cy][cx] == 6 and new_grid[cy][cx] == 6 and random.random() < 0.1:
                            new_grid[cy][cx] = random.choice([39, 40])
                            break

                # Wander
                for ny, nx in neighbors:
                    cy, cx = ny % height, nx % width
                    if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                        new_grid[cy][cx] = 83
                        moved = True
                        break

                if not moved:
                    new_grid[y][x] = 83
            else:"""

logic_block_right = """            elif current_state == 83:
                new_grid[y][x] = 6 # Default to move/leave Void
                neighbors = [(y+dy, x+dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy != 0 or dx != 0]
                random.shuffle(neighbors)
                moved = False

                outer_gods = [42, 43, 45, 48, 82]
                near_god = any(grid[ny % height][nx % width] in outer_gods for ny, nx in neighbors)

                if near_god:
                    # Their maddening music lures mortals
                    for ny, nx in neighbors:
                        cy, cx = ny % height, nx % width
                        if grid[cy][cx] == 6 and new_grid[cy][cx] == 6 and random.random() < 0.1:
                            new_grid[cy][cx] = random.choice([39, 40])
                            break

                # Wander
                if not near_god or True: # They wander always
                    for ny, nx in neighbors:
                        cy, cx = ny % height, nx % width
                        if grid[cy][cx] == 6 and new_grid[cy][cx] == 6:
                            new_grid[cy][cx] = 83
                            moved = True
                            break

                if not moved:
                    new_grid[y][x] = 83
            else:"""

if logic_block_wrong in content:
    content = content.replace(logic_block_wrong, logic_block_right)
    with open("simulation.py", "w") as f:
        f.write(content)
    print("Fixed indentation.")
else:
    print("Could not find the wrong block to fix.")
