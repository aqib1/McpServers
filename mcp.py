from mcp.server.fastmcp import FastMCP
from random import choice

mcp = FastMCP("RandomServer")

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

@mcp.tool()
def calculate_distance(point1: tuple, point2: tuple) -> float:
    """Calculate the Euclidean distance between two points."""
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

if __name__ == "__main__":
    mcp.run()
