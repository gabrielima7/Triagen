with open("agent_handover.md", "r") as f:
    lines = f.readlines()
    print("".join(lines[-30:]))
