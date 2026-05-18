with open("simulation.py", "r") as f:
    content = f.read()

# I am adding a new state, state 10, "Godzilla"

# 1. Update create_grid
content = content.replace(
    "row = [random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) for _ in range(width)]",
    "row = [random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) for _ in range(width)]"
)

# 2. Update print_grid
content = content.replace(
    'chars = {0: "R", 1: "P", 2: "S", 3: "K", 4: "L", 5: "B", 6: "V", 7: "*", 8: "@", 9: "W"}',
    'chars = {0: "R", 1: "P", 2: "S", 3: "K", 4: "L", 5: "B", 6: "V", 7: "*", 8: "@", 9: "W", 10: "G"}'
)

# 3. Update HTML generation
content = content.replace(
    "<p>Red: Rock | Green: Paper | Blue: Scissors | Purple: Spock | Yellow: Lizard | Black: Black Hole | Gray: Void | White: Supernova | Cyan: Pulsar | Magenta: Wormhole</p>",
    "<p>Red: Rock | Green: Paper | Blue: Scissors | Purple: Spock | Yellow: Lizard | Black: Black Hole | Gray: Void | White: Supernova | Cyan: Pulsar | Magenta: Wormhole | Orange: Godzilla</p>"
)
content = content.replace(
    "                9: '#ff00ff'  // Wormhole\n            };",
    "                9: '#ff00ff', // Wormhole\n                10: '#ff7f00' // Godzilla\n            };"
)


# 4. Update update_grid logic
new_logic = """            elif current_state == 9:
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
                continue
            elif current_state == 10: # Godzilla
                # Godzilla slowly walks and destroys
                directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                dy, dx = random.choice(directions)
                ny, nx = (y + dy) % height, (x + dx) % width
                if (ny, nx) not in pending_changes and grid[ny][nx] != 10:
                    pending_changes[(ny, nx)] = 10
                    pending_changes[(y, x)] = 6 # Leaves void behind
                else:
                     new_grid[y][x] = 10
                continue
"""

content = content.replace(
"""            elif current_state == 9:
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
                continue""", new_logic
)


with open("simulation.py", "w") as f:
    f.write(content)
