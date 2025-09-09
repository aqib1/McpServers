from mcp.server.fastmcp import FastMCP
from random import choice

mcp = FastMCP("RandomServer")

def get_random_name(names: list = None) -> str:
    if names and isinstance(names, str):
        return choice(names)
    else:
        default_names = [
            "Steve", "Alex", "Herobrine", "Notch", "Creeper", "Enderman",
            "Zombie", "Skeleton", "Spider", "Villager", "Witch", "Ghast"
        ]
        return choice(default_names)

if __name__ == "__main__":
    mcp.run()
