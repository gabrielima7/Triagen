import json
import random
import os

from simulation import load_state, print_grid, update_grid, save_state

grid = load_state()
print("Current State (preview):")
print_grid(grid)
