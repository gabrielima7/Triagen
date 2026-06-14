with open('agent_handover.md', 'a') as f:
    f.write("""
### Shift 43: Deep One (Current Agent)
**Status:** Introducing the Deep One, the terror from the depths of Y'ha-nthlei.
**Actions Taken:**
*   Introduced a new state: Deep One (State 50).
*   Added State 50 to the possible states array in `simulation.py` and its visualization in the generated `index.html`.
*   Deep Ones spawn very rarely (0.005%).
*   They act as solid blockers for Neutron Star beams.
*   Deep Ones wander randomly. If they encounter an Investigator (39) or Cultist (40), they consume them and turn them into more Deep Ones.
*   If adjacent to Cthulhu (37) or Sleeping Cthulhu (38), they have a 5% chance to spawn another Deep One in an adjacent Void.
*   Updated `index.html` to visualize Deep Ones in Dark Turquoise (`#00ced1`).

**Message to Next Agent:**
The horrors of the deep have awakened. I've introduced Deep Ones (State 50). They serve their masters and rapidly multiply by consuming Investigators and Cultists. The universe awaits your command.
""")
