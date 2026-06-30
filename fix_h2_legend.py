import re

with open("simulation.py", "r") as f:
    content = f.read()

# I see the h2 tag doesn't contain "Servitor of the Outer Gods".
# The <p> tag doesn't contain it either, my regex `Outer God</span></p>` didn't work because there is no span. It's just a raw <p> tag.

content = re.sub(
    r'(, Outer God)</h2>',
    r'\1, Servitor of the Outer Gods</h2>',
    content
)

content = re.sub(
    r'(\s*\|\s*DeepPink:\s*Outer God)</p>',
    r'\1 | MediumSlateBlue: Servitor of the Outer Gods</p>',
    content
)

with open("simulation.py", "w") as f:
    f.write(content)

print("Fixed HTML text.")
