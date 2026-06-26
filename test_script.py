import re
with open("simulation.py", "r") as f:
    text = f.read()

import json
print(re.findall(r"elif current_state == \d+:", text))
