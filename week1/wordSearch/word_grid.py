import enum
from enum import Enum

class Dir(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def __init__(self, deltaR, deltaC):
        self.deltaR = deltaR
        self.deltaC = deltaC
        
class WordGrid:
    def __init__(self, grid: list[str]):
        self.__cols = len(grid[0]) if grid else 0  # number of columns is original length
        # Add a space at the end of each string
        self.__grid = [row + ' ' for row in grid]
        # Add an additional row of spaces (cols+1)
        self.__grid.append(' ' * (self.__cols + 1))
        self.__rows = len(grid)
