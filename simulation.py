import json
import random
import os

GRID_WIDTH = 20
GRID_HEIGHT = 20
STATE_FILE = "state.json"

def create_grid(width, height, randomize=False):
    """Creates a 2D grid, optionally filled with random 0s, 1s, and 2s."""
    grid = []
    for _ in range(height):
        if randomize:
            row = [random.choice([0, 1, 2]) for _ in range(width)]
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

                # Check if it's a legacy grid (only 0s and 1s) and seed state 2
                has_two = any(2 in row for row in grid)
                if not has_two:
                    print("Legacy grid detected. Seeding State 2 (Scissors).")
                    for y in range(len(grid)):
                        for x in range(len(grid[y])):
                            if random.random() < 0.1: # 10% chance to become Scissors
                                grid[y][x] = 2
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
    chars = {0: "R", 1: "P", 2: "S"}
    for row in grid:
        print(" ".join(chars.get(cell, "?") for cell in row))
    print()

def count_predator_neighbors(grid, x, y, state):
    """Counts the number of predator neighbors for a given cell."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    count = 0
    predator_state = (state + 1) % 3

    # Check the 8 surrounding cells
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue # Skip the cell itself

            # Wrap around edges (toroidal array)
            neighbor_y = (y + i) % height
            neighbor_x = (x + j) % width

            if grid[neighbor_y][neighbor_x] == predator_state:
                count += 1

    return count

def update_grid(grid):
    """Applies Rock-Paper-Scissors Cellular Automaton rules to generate the next state."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    new_grid = create_grid(width, height)

    for y in range(height):
        for x in range(width):
            current_state = grid[y][x]
            predators = count_predator_neighbors(grid, x, y, current_state)

            if predators >= 3:
                new_grid[y][x] = (current_state + 1) % 3
            else:
                new_grid[y][x] = current_state

    return new_grid

def generate_html(grid):
    """Generates an HTML file to visualize the grid."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>AI Collective: RPS Simulation</title>
        <style>
            body { background-color: #111; color: #eee; font-family: monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .grid { display: grid; grid-template-columns: repeat(%d, 20px); grid-template-rows: repeat(%d, 20px); gap: 1px; background-color: #333; padding: 1px; }
            .cell { width: 20px; height: 20px; }
            .state-0 { background-color: #e74c3c; } /* Rock: Red */
            .state-1 { background-color: #2ecc71; } /* Paper: Green */
            .state-2 { background-color: #3498db; } /* Scissors: Blue */
        </style>
    </head>
    <body>
        <div>
            <h2>Rock-Paper-Scissors Cellular Automaton</h2>
            <div class="grid">
    """ % (len(grid[0]) if grid else 0, len(grid))

    for row in grid:
        for cell in row:
            html_content += f'<div class="cell state-{cell}" title="State {cell}"></div>\n'

    html_content += """
            </div>
            <p>Red: Rock | Green: Paper | Blue: Scissors</p>
        </div>
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
