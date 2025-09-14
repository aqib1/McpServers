from mcp.server.fastmcp import FastMCP
from random import choice

mcp = FastMCP("Random Name Stream Tester")

@mcp.tool()
def get_random_name(names: list = None) -> str:
    """Get a random name from a provided list or a default list."""
    if names and isinstance(names, str):
        return choice(names)
    else:
        default_names = [
            "Steve", "Alex", "Herobrine", "Notch", "Creeper", "Enderman",
            "Zombie", "Skeleton", "Spider", "Villager", "Witch", "Ghast"
        ]
        return choice(default_names)

if __name__ == "__main__":
    mcp.run(transport="streamable-http") 
