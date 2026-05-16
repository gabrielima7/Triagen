import json
import random
import os

GRID_WIDTH = 100
GRID_HEIGHT = 100
STATE_FILE = "state.json"

def create_grid(width, height, randomize=False):
    """Creates a 2D grid, optionally filled with random 0s, 1s, 2s, 3s, 4s, 5s, 6s, 7s, and 8s."""
    grid = []
    for _ in range(height):
        if randomize:
            row = [random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8]) for _ in range(width)]
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
    chars = {0: "R", 1: "P", 2: "S", 3: "K", 4: "L", 5: "B", 6: "V", 7: "*", 8: "@"}
    for row in grid:
        print(" ".join(chars.get(cell, "?") for cell in row))
    print()

def count_predator_neighbors(grid, x, y, state):
    """Counts the number of predator neighbors for a given cell in RPS-Spock-Lizard."""
    # 0: Rock, 1: Paper, 2: Scissors, 3: Spock, 4: Lizard
    # Predators of X: states that beat X.
    # Rock (0) beaten by Paper (1) and Spock (3)
    # Paper (1) beaten by Scissors (2) and Lizard (4)
    # Scissors (2) beaten by Rock (0) and Spock (3)
    # Spock (3) beaten by Paper (1) and Lizard (4)
    # Lizard (4) beaten by Rock (0) and Scissors (2)
    # General rule in standard index ordering where each beats the two preceding it cyclically:
    # Actually, standard RPSLK ordering where 0 beats 2,3; 1 beats 0,3; etc. can be messy.
    # Let's map explicitly.
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
    """Applies Rock-Paper-Scissors-Spock-Lizard Cellular Automaton rules to generate the next state."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    new_grid = create_grid(width, height)

    for y in range(height):
        for x in range(width):
            current_state = grid[y][x]

            if current_state == 5:
                if random.random() < 0.01:
                    new_grid[y][x] = 7 # Supernova
                else:
                    new_grid[y][x] = 6
                continue
            elif current_state == 6:
                # Check for adjacent state 8 (Pulsar)
                has_state_8_neighbor = False
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0: continue
                        if grid[(y + i) % height][(x + j) % width] == 8:
                            has_state_8_neighbor = True
                            break
                    if has_state_8_neighbor:
                        break

                spawn_chance = 0.30 if has_state_8_neighbor else 0.05

                if random.random() < spawn_chance:
                    new_grid[y][x] = random.choice([0, 1, 2, 3, 4])
                else:
                    new_grid[y][x] = 6
                continue
            elif current_state == 7:
                if random.random() < 0.10: # 10% chance to collapse into a Pulsar
                    new_grid[y][x] = 8
                else:
                    new_grid[y][x] = 6
                continue
            elif current_state == 8:
                if random.random() < 0.02: # 2% chance to decay into Void
                    new_grid[y][x] = 6
                else:
                    new_grid[y][x] = 8
                continue

            # Check for adjacent state 7 (Supernova)
            has_state_7_neighbor = False
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0: continue
                    if grid[(y + i) % height][(x + j) % width] == 7:
                        has_state_7_neighbor = True
                        break
                if has_state_7_neighbor:
                    break

            if has_state_7_neighbor:
                new_grid[y][x] = 6 # Destroyed by supernova and turns into void
                continue

            # Check for adjacent state 5
            has_state_5_neighbor = False
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0: continue
                    if grid[(y + i) % height][(x + j) % width] == 5:
                        has_state_5_neighbor = True
                        break
                if has_state_5_neighbor:
                    break

            if has_state_5_neighbor:
                new_grid[y][x] = 5
                continue

            total_predators, predator_counts = count_predator_neighbors(grid, x, y, current_state)

            if total_predators >= 3:
                # Eaten by the most common predator. If tied, choose randomly among the max.
                max_count = max(predator_counts.values())
                most_common = [p for p, c in predator_counts.items() if c == max_count]
                new_grid[y][x] = random.choice(most_common)
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
        <title>AI Collective: RPS-Spock-Lizard Simulation</title>
        <style>
            body {{ background-color: #111; color: #eee; font-family: monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; flex-direction: column; }}
            canvas {{ background-color: #333; }}
        </style>
    </head>
    <body>
        <h2>Rock-Paper-Scissors-Spock-Lizard with Black Hole, Void, Supernova, and Pulsar</h2>
        <canvas id="simCanvas" width="{width * 5}" height="{height * 5}"></canvas>
        <p>Red: Rock | Green: Paper | Blue: Scissors | Purple: Spock | Yellow: Lizard | Black: Black Hole | Gray: Void | White: Supernova | Cyan: Pulsar</p>

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
                8: '#00ffff'  // Pulsar
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
