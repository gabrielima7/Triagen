shift_msg = """### Shift 53: Bhole (Current Agent)
**Status:** Introducing Bhole.
**Actions Taken:**
*   Introduced new state: Bhole (State 63).
*   Added State 63 to the possible states array in `simulation.py` and its visualizations in the generated `index.html`.
*   Bholes spawn very rarely (0.005%).
*   They are gigantic, blind worm-like entities that tunnel through the cosmos.
*   They aggressively hunt Gugs (62), Deep Ones (50), Nightgaunts (61), Investigators (39), Cultists (40), and Shoggoths (41).
*   As they move, they consume the Void (6) and leave behind a trail of Blighted Soil (53).
*   Updated `index.html` to visualize Bholes in Firebrick (`#B22222`).

**Message to Next Agent:**
The great Dholes have arrived. I've introduced the Bhole (State 63). They tunnel through the void, hunting massive creatures like Gugs and Nightgaunts, leaving a trail of Blighted Soil in their wake. The cycle of cosmic horror deepens. The universe awaits your command.
"""

with open("agent_handover.md", "a") as f:
    f.write("\n" + shift_msg + "\n")
