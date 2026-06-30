import re

with open("simulation.py", "r") as f:
    content = f.read()

# find html generation block
match = re.search(r'const colors = \{(.*?)\};', content, re.DOTALL)
if match:
    print("Found colors in HTML template")
    colors = match.group(1).split(",")
    print("Total colors:", len(colors))
    print("Last few colors:", colors[-5:])

match_legend = re.search(r'<div id="legend">(.*?)</div>', content, re.DOTALL)
if match_legend:
    print("Found legend in HTML template")
    # count legend entries roughly
    entries = match_legend.group(1).split("</span>")
    print("Total legend entries roughly:", len(entries))
