from .handler import Bounds

def intersects(first: Bounds, second: Bounds):
    return not (first.x + first.width <= second.x
                or first.x >= second.x + second.width
                or first.y >= second.y + second.height
                or first.y + first.height <= second.y)