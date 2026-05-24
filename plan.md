1. **Define State 22 (Pandora)**
   - Color: Deep Pink (`#ff1493`)
   - Add state 22 to `create_grid` (0.01% chance on initialization).
   - Add state 22 spawning logic in Void to `update_grid` (0.01% chance).
   - Add state 22 description and visualization in `generate_html`.

2. **Implement Pandora interactions in `update_grid`**
   - Identify Pandora cells during the O(N) pre-computation pass.
   - Keep Pandora cells completely still. (No movement logic needed).
   - Check if Pandora is touched by any Kaiju (Godzilla, Jaeger, Mothra, MechaGodzilla, Omega, Reaper, Phoenix, Nidhogg). We can check for a collision by seeing if the Pandora cell is targeted by any Kaiju.
   - If Pandora is touched, trigger the catastrophic opening:
     - The Pandora cell becomes a Wormhole (`9`).
     - A 5x5 area around the Pandora cell is randomized with all 22 states.
   - To implement the 5x5 explosion smoothly without messing up nested iteration order, we will create a `pandora_explosions` list/set to store targets that will be hit by an open Pandora box. Then we process these explosions safely. We must also update `teleportation_targets` filtering. Wait, actually, the 5x5 explosion can just be handled when processing Pandora collisions, by adding to a global dictionary like `pandora_targets = {}` mapping `(y, x)` to random states, overriding almost everything else. Let's do that!

3. **Modify `agent_handover.md`**
   - Document the shift (Shift 20) and the creation of Pandora.

4. **Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.**

5. **Submit changes.**
