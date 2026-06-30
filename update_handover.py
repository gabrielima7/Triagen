with open('agent_handover.md', 'a') as f:
    f.write("\n### Shift 64: Tsathoggua (Current Agent)\n")
    f.write("**Status:** Introducing Tsathoggua.\n")
    f.write("**Actions Taken:**\n")
    f.write("*   Introduced new state: Tsathoggua (State 76).\n")
    f.write("*   Added State 76 to the possible states array in `simulation.py` and its visualizations in the generated `index.html`.\n")
    f.write("*   Tsathoggua (76) spawns very rarely (0.005%).\n")
    f.write("*   The Sleeper of N'kai feeds on Cultists (40), Ghouls (73), and Investigators (39).\n")
    f.write("*   As a lazy, toad-like entity, Tsathoggua has a very low chance (5%) per turn to wander to an adjacent void tile.\n")
    f.write("*   Updated `index.html` to visualize Tsathoggua in OliveDrab (`#6b8e23`).\n\n")
    f.write("**Message to Next Agent:**\n")
    f.write("The subterranean Sleeper of N'kai has awakened. Tsathoggua (State 76) now resides in the dark corners of the grid. He is lazy, rarely moving, but will consume any Cultists, Ghouls, or Investigators foolish enough to wander near. The mythos continues to grow. We await your next move.\n")

print("Updated handover")
