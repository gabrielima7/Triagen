import json
import random
import os

GRID_WIDTH = 100
GRID_HEIGHT = 100
STATE_FILE = "state.json"

def create_grid(width, height, randomize=False):
    """Creates a 2D grid, optionally filled with random 0s, 1s, 2s, 3s, 4s, 5s, 6s, 7s, 8s, and 9s."""
    grid = []
    for _ in range(height):
        if randomize:
            row = [random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) for _ in range(width)]
        else:
            row = [0 for _ in range(width)]
        grid.append(row)
    return grid

def load_state():
    """Loads the grid state from state.json if it exists, otherwise creates a new random grid."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                print("Loaded existing state from", STATE_FILE)
                grid = data.get("grid", create_grid(GRID_WIDTH, GRID_HEIGHT, randomize=True))

                # Check if we need to resize the grid
                if len(grid) != GRID_HEIGHT or (len(grid) > 0 and len(grid[0]) != GRID_WIDTH):
                    print(f"Resizing grid from {len(grid[0]) if len(grid) > 0 else 0}x{len(grid)} to {GRID_WIDTH}x{GRID_HEIGHT}.")
                    new_grid = create_grid(GRID_WIDTH, GRID_HEIGHT, randomize=True)
                    # Copy old grid data over to new grid
                    min_height = min(len(grid), GRID_HEIGHT)
                    min_width = min(len(grid[0]) if len(grid) > 0 else 0, GRID_WIDTH)
                    for y in range(min_height):
                        for x in range(min_width):
                            new_grid[y][x] = grid[y][x]
                    grid = new_grid

                # Check if it's a legacy grid (missing states 3 or 4) and seed them
                has_three = any(3 in row for row in grid)
                has_four = any(4 in row for row in grid)
                if not (has_three and has_four):
                    print("Legacy grid detected. Seeding State 3 (Spock) and State 4 (Lizard).")
                    for y in range(len(grid)):
                        for x in range(len(grid[y])):
                            rand_val = random.random()
                            if rand_val < 0.05: # 5% chance to become Spock
                                grid[y][x] = 3
                            elif rand_val < 0.10: # 5% chance to become Lizard
                                grid[y][x] = 4
                return grid
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading state: {e}. Creating a new random grid.")
            return create_grid(GRID_WIDTH, GRID_HEIGHT, randomize=True)
    else:
        print("No existing state found. Creating a new random grid.")
        return create_grid(GRID_WIDTH, GRID_HEIGHT, randomize=True)

def save_state(grid):
    """Saves the grid state to state.json."""
    data = {
        "grid": grid,
        "width": len(grid[0]) if grid else 0,
        "height": len(grid)
    }
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("Saved state to", STATE_FILE)

def print_grid(grid):
    """Prints the grid to the console."""
    chars = {0: "R", 1: "P", 2: "S", 3: "K", 4: "L", 5: "B", 6: "V", 7: "*", 8: "@", 9: "W"}
    for row in grid:
        print(" ".join(chars.get(cell, "?") for cell in row))
    print()

def count_predator_neighbors(grid, x, y, state):
    """Counts the number of predator neighbors for a given cell in RPS-Spock-Lizard."""
    # 0: Rock, 1: Paper, 2: Scissors, 3: Spock, 4: Lizard
    # Predators of X: states that beat X.
    predators_of = {
        0: [1, 3],
        1: [2, 4],
        2: [0, 3],
        3: [1, 4],
        4: [0, 2]
    }

    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    count = 0
    if state in predators_of:
        predator_states = predators_of[state]
    else:
        predator_states = []
    predator_counts = {p: 0 for p in predator_states}

    # Check the 8 surrounding cells
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue # Skip the cell itself

            # Wrap around edges (toroidal array)
            neighbor_y = (y + i) % height
            neighbor_x = (x + j) % width

            neighbor_state = grid[neighbor_y][neighbor_x]
            if neighbor_state in predator_states:
                count += 1
                predator_counts[neighbor_state] += 1

    return count, predator_counts

def update_grid(grid):
    """Applies RPSLK + Black Hole + Void + Supernova + Pulsar + Wormhole rules."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    new_grid = create_grid(width, height)

    # 1. PRE-COMPUTATION (O(N) search for Wormholes and Voids to avoid O(N^2) complexity inside the loop)
    wormholes = []
    voids = []
    for y in range(height):
        for x in range(width):
            state = grid[y][x]
            if state == 9:
                wormholes.append((y, x))
            elif state == 6:
                voids.append((y, x))

    # 2. COLLECT WORMHOLE HORIZONS (Normal states adjacent to any Wormhole)
    wormhole_horizons = []
    for wy, wx in wormholes:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0: continue
                ny, nx = (wy + i) % height, (wx + j) % width
                neighbor_state = grid[ny][nx]
                if neighbor_state in [0, 1, 2, 3, 4]:
                    wormhole_horizons.append(neighbor_state)

    # 3. PRE-DETERMINE WORMHOLE QUANTUM TELEPORTATION TARGETS (Resolves overwrite bug by applying targets in cell loop)
    available_voids = list(voids)
    teleportation_targets = {}
    for wy, wx in wormholes:
        if available_voids:
            target_y, target_x = random.choice(available_voids)
            available_voids.remove((target_y, target_x))
            teleported_state = random.choice(wormhole_horizons) if wormhole_horizons else random.choice([0, 1, 2, 3, 4])
            teleportation_targets[(target_y, target_x)] = teleported_state

    # 4. MAIN CELLULAR AUTOMATON UPDATE PASS
    for y in range(height):
        for x in range(width):
            # Check if this cell receives a quantum teleported state (priority over normal void processing)
            if (y, x) in teleportation_targets:
                new_grid[y][x] = teleportation_targets[(y, x)]
                continue

            current_state = grid[y][x]

            # --- STATE 5: BLACK HOLE ---
            if current_state == 5:
                # Black Hole vs Wormhole: adjacent Wormholes destroy Black Holes completely
                has_wormhole_neighbor = any(
                    grid[(y + i) % height][(x + j) % width] == 9
                    for i in range(-1, 2)
                    for j in range(-1, 2)
                    if not (i == 0 and j == 0)
                )
                if has_wormhole_neighbor:
                    new_grid[y][x] = 6 # Destroyed by Wormhole and turns into Void
                else:
                    rand_val = random.random()
                    if rand_val < 0.01:
                        new_grid[y][x] = 7 # Supernova (1% chance)
                    elif rand_val < 0.02:
                        new_grid[y][x] = 9 # Wormhole (1% chance from Black Hole)
                    else:
                        new_grid[y][x] = 6 # Decays into Void (98% chance)
                continue

            # --- STATE 6: VOID ---
            elif current_state == 6:
                # Check for Pulsar neighbor
                has_pulsar_neighbor = any(
                    grid[(y + i) % height][(x + j) % width] == 8
                    for i in range(-1, 2)
                    for j in range(-1, 2)
                    if not (i == 0 and j == 0)
                )

                # Check for Wormhole neighbor
                has_wormhole_neighbor = any(
                    grid[(y + i) % height][(x + j) % width] == 9
                    for i in range(-1, 2)
                    for j in range(-1, 2)
                    if not (i == 0 and j == 0)
                )

                if has_pulsar_neighbor:
                    # Pulsar violently colonizes adjacent Void
                    new_grid[y][x] = random.choice([0, 1, 2, 3, 4])
                elif has_wormhole_neighbor:
                    # Wormhole spit-out mechanics
                    r = random.random()
                    if r < 0.10:
                        new_grid[y][x] = random.choice([0, 1, 2, 3, 4]) # Wormhole spits out normal life
                    elif r < 0.11:
                        new_grid[y][x] = 5 # Wormhole perturbation forms Black Hole (1% chance)
                    else:
                        new_grid[y][x] = 6
                else:
                    # Spontaneous transitions
                    rand_val = random.random()
                    if rand_val < 0.001:
                        new_grid[y][x] = 9 # Spontaneous Wormhole (0.1% chance)
                    elif rand_val < 0.05:
                        new_grid[y][x] = random.choice([0, 1, 2, 3, 4]) # Spontaneous emergence
                    else:
                        new_grid[y][x] = 6
                continue

            # --- STATE 7: SUPERNOVA ---
            elif current_state == 7:
                new_grid[y][x] = 8 # Supernova becomes Pulsar
                continue

            # --- STATE 8: PULSAR ---
            elif current_state == 8:
                rand_val = random.random()
                if rand_val < 0.05:
                    new_grid[y][x] = 9 # Pulsar collapses into Wormhole (5% chance)
                elif rand_val < 0.10:
                    new_grid[y][x] = 6 # Pulsar fades to Void (5% chance)
                else:
                    new_grid[y][x] = 8 # Remains Pulsar
                continue

            # --- STATE 9: WORMHOLE ---
            elif current_state == 9:
                rand_val = random.random()
                if rand_val < 0.05:
                    new_grid[y][x] = 5 # Wormhole collapses into Black Hole (5% chance, closes cycle)
                elif rand_val < 0.15:
                    new_grid[y][x] = 6 # Wormhole decays into Void (10% chance)
                else:
                    new_grid[y][x] = 9 # Wormhole persists
                continue

            # --- NORMAL STATES 0-4: ROCK-PAPER-SCISSORS-SPOCK-LIZARD ---
            # Check environmental hazards first
            # 1. Supernova neighbor: completely destroys normal states
            has_supernova_neighbor = False
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0: continue
                    if grid[(y + i) % height][(x + j) % width] == 7:
                        has_supernova_neighbor = True
                        break
                if has_supernova_neighbor:
                    break

            if has_supernova_neighbor:
                new_grid[y][x] = 6 # Supernova incinerates cell to Void
                continue

            # 2. Black Hole neighbor: consumes normal states
            has_blackhole_neighbor = False
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0: continue
                    if grid[(y + i) % height][(x + j) % width] == 5:
                        has_blackhole_neighbor = True
                        break
                if has_blackhole_neighbor:
                    break

            if has_blackhole_neighbor:
                new_grid[y][x] = 5 # Consumed by Black Hole
                continue

            # 3. Wormhole neighbor: sucked in with a 20% chance
            has_wormhole_neighbor = False
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0: continue
                    if grid[(y + i) % height][(x + j) % width] == 9:
                        has_wormhole_neighbor = True
                        break
                if has_wormhole_neighbor:
                    break

            if has_wormhole_neighbor and random.random() < 0.20:
                new_grid[y][x] = 6 # Sucked into Void by Wormhole gravitational pull
                continue

            # 4. Standard RPSLK predators check
            total_predators, predator_counts = count_predator_neighbors(grid, x, y, current_state)
            if total_predators >= 3:
                # Eaten by the most common predator
                max_count = max(predator_counts.values())
                most_common = [p for p, c in predator_counts.items() if c == max_count]
                new_grid[y][x] = random.choice(most_common)
            else:
                # Evolve quantum non-local teleportation via Wormhole horizons if neighbor to one
                if has_wormhole_neighbor and wormhole_horizons and random.random() < 0.10:
                    new_grid[y][x] = random.choice(wormhole_horizons)
                else:
                    new_grid[y][x] = current_state

    return new_grid

def generate_html(grid):
    """Generates an HTML file to visualize the grid using a canvas."""
    width = len(grid[0]) if grid else 0
    height = len(grid)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="1">
        <title>AI Collective: RPS-Spock-Lizard-Wormhole Simulation</title>
        <style>
            body {{ background-color: #111; color: #eee; font-family: monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; flex-direction: column; }}
            canvas {{ background-color: #333; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7); border-radius: 4px; }}
            h2 {{ margin-bottom: 5px; color: #ff00ff; text-shadow: 0 0 10px rgba(255, 0, 255, 0.4); }}
            p {{ margin-top: 15px; font-size: 11px; color: #999; }}
        </style>
    </head>
    <body>
        <h2>Rock-Paper-Scissors-Spock-Lizard with Wormhole Singularity</h2>
        <canvas id="simCanvas" width="{width * 5}" height="{height * 5}"></canvas>
        <p>Red: Rock | Green: Paper | Blue: Scissors | Purple: Spock | Yellow: Lizard | Black: Black Hole | Gray: Void | White: Supernova | Cyan: Pulsar | Magenta: Wormhole</p>

        <script>
            const canvas = document.getElementById('simCanvas');
            const ctx = canvas.getContext('2d');
            const cellSize = 5;

            const colors = {{
                0: '#e74c3c', // Rock
                1: '#2ecc71', // Paper
                2: '#3498db', // Scissors
                3: '#9b59b6', // Spock
                4: '#f1c40f', // Lizard
                5: '#000000', // Black Hole
                6: '#7f8c8d', // Void
                7: '#ffffff', // Supernova
                8: '#00ffff', // Pulsar
                9: '#ff00ff'  // Wormhole (Magenta glow)
            }};

            const grid = {json.dumps(grid)};

            for (let y = 0; y < grid.length; y++) {{
                for (let x = 0; x < grid[y].length; x++) {{
                    const state = grid[y][x];
                    ctx.fillStyle = colors[state] || '#333';
                    ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
                }}
            }}
        </script>
    </body>
    </html>
    """

    with open("index.html", "w") as f:
        f.write(html_content)
    print("Generated visualizer at index.html")

def main():
    print("--- AI Collective: Continuous Execution Shift ---")
    grid = load_state()

    print("Current State:")
    print_grid(grid)

    print("Computing next generation...")
    next_grid = update_grid(grid)

    print("Next State:")
    print_grid(next_grid)

    save_state(next_grid)
    generate_html(next_grid)
    print("Shift complete. Handing over state to next agent.")

if __name__ == "__main__":
    main()
