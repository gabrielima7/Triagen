with open("simulation.py", "r") as f:
    content = f.read()
import re
print(re.search(r"elif state == 70:.*?(\s+)else:", content, re.DOTALL))
