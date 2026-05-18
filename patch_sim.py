import re

with open("simulation.py", "r") as f:
    content = f.read()

# 1. Update create_grid
content = content.replace(
    "row = [random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8]) for _ in range(width)]",
    "row = [random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) for _ in range(width)]"
)

# 2. Update print_grid
content = content.replace(
    'chars = {0: "R", 1: "P", 2: "S", 3: "K", 4: "L", 5: "B", 6: "V", 7: "*", 8: "@"}',
    'chars = {0: "R", 1: "P", 2: "S", 3: "K", 4: "L", 5: "B", 6: "V", 7: "*", 8: "@", 9: "W"}'
)

# 3. Update update_grid top
content = content.replace(
    "new_grid = create_grid(width, height)",
    "new_grid = create_grid(width, height)\n    pending_changes = {}"
)

# 4. Update Pulsar logic (state 8)
pulsar_old = """            elif current_state == 8:
                if random.random() < 0.10:
                    new_grid[y][x] = 6 # Pulsar becomes Void
                else:
                    new_grid[y][x] = 8
                continue"""
pulsar_new = """            elif current_state == 8:
                r = random.random()
                if r < 0.05:
                    new_grid[y][x] = 9 # Pulsar becomes Wormhole
                elif r < 0.10:
                    new_grid[y][x] = 6 # Pulsar becomes Void
                else:
                    new_grid[y][x] = 8
                continue
            elif current_state == 9:
                if random.random() < 0.05:
                    new_grid[y][x] = 6 # Wormhole collapses into Void
                else:
                    new_grid[y][x] = 9

                    # Teleportation
                    adj_rpslk = []
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i == 0 and j == 0: continue
                            ny, nx = (y + i) % height, (x + j) % width
                            if grid[ny][nx] in [0, 1, 2, 3, 4]:
                                adj_rpslk.append((ny, nx, grid[ny][nx]))

                    if adj_rpslk:
                        src_y, src_x, state = random.choice(adj_rpslk)
                        target_y, target_x = random.randint(0, height - 1), random.randint(0, width - 1)
                        if grid[target_y][target_x] == 6 and (target_y, target_x) not in pending_changes:
                            pending_changes[(target_y, target_x)] = state
                            pending_changes[(src_y, src_x)] = 6
                continue"""
content = content.replace(pulsar_old, pulsar_new)

# 5. Apply pending_changes
apply_changes = """    for (ty, tx), state in pending_changes.items():
        new_grid[ty][tx] = state

    return new_grid"""
content = content.replace("    return new_grid", apply_changes)

# 6. Update HTML generation
content = content.replace(
    "<p>Red: Rock | Green: Paper | Blue: Scissors | Purple: Spock | Yellow: Lizard | Black: Black Hole | Gray: Void | White: Supernova | Cyan: Pulsar</p>",
    "<p>Red: Rock | Green: Paper | Blue: Scissors | Purple: Spock | Yellow: Lizard | Black: Black Hole | Gray: Void | White: Supernova | Cyan: Pulsar | Magenta: Wormhole</p>"
)
content = content.replace(
    "                8: '#00ffff'  // Pulsar",
    "                8: '#00ffff', // Pulsar\n                9: '#ff00ff'  // Wormhole"
)
content = content.replace(
    "                8: '#00ffff'  // Pulsar\n            };",
    "                8: '#00ffff', // Pulsar\n                9: '#ff00ff'  // Wormhole\n            };"
)


with open("simulation.py", "w") as f:
    f.write(content)
