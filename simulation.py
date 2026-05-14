import json
import random
import os

GRID_WIDTH = 20
GRID_HEIGHT = 20
STATE_FILE = "state.json"

def create_grid(width, height, randomize=False):
    """Creates a 2D grid, optionally filled with random 0s and 1s."""
    grid = []
    for _ in range(height):
        if randomize:
            row = [random.choice([0, 1]) for _ in range(width)]
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
                return data.get("grid", create_grid(GRID_WIDTH, GRID_HEIGHT, randomize=True))
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
    for row in grid:
        print(" ".join("█" if cell else "." for cell in row))
    print()

def count_neighbors(grid, x, y):
    """Counts the number of alive neighbors for a given cell."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    count = 0

    # Check the 8 surrounding cells
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue # Skip the cell itself

            # Wrap around edges (toroidal array)
            neighbor_y = (y + i) % height
            neighbor_x = (x + j) % width

            count += grid[neighbor_y][neighbor_x]

    return count

def update_grid(grid):
    """Applies Conway's Game of Life rules to generate the next state."""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    new_grid = create_grid(width, height)

    for y in range(height):
        for x in range(width):
            neighbors = count_neighbors(grid, x, y)
            is_alive = grid[y][x] == 1

            # Rule 1: Underpopulation or Overpopulation -> Dies
            if is_alive and (neighbors < 2 or neighbors > 3):
                new_grid[y][x] = 0
            # Rule 2: Survival -> Lives
            elif is_alive and (neighbors == 2 or neighbors == 3):
                new_grid[y][x] = 1
            # Rule 3: Reproduction -> Becomes alive
            elif not is_alive and neighbors == 3:
                new_grid[y][x] = 1
            # Otherwise -> Stays dead
            else:
                new_grid[y][x] = 0

    return new_grid

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
    print("Shift complete. Handing over state to next agent.")

if __name__ == "__main__":
    main()
