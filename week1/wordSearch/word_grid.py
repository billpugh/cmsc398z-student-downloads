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

    def find_at(self, word: str, row: int, col: int, dir: 'Dir') -> bool:
        """
        Check if a word exists in the grid starting at (row, col) and moving in the given direction.

        Args:
            word (str): The word to search for.
            row (int): Starting row index.
            col (int): Starting column index.
            dir (Dir): Direction to search (Dir.UP, Dir.DOWN, Dir.LEFT, Dir.RIGHT).

        Returns:
            bool: True if the word exists, False otherwise.

        Example:
            >>> grid = WordGrid(["XCATX"])
            >>> grid.find_at("CAT", 0, 1, Dir.RIGHT)
            True
            >>> grid.find_at("CAT", 0, 1, Dir.LEFT)
            False
        """
        for i, ch in enumerate(word):
            if ch != self.__grid[row + i * dir.deltaR][col + i * dir.deltaC]:
                return False
        return True

    def find(self, word: str):
        """
        Search the grid for all occurrences of the word in any direction.

        Args:
            word (str): The word to search for.

        Returns:
            list[tuple[int, int, Dir]]: List of (row, col, direction) tuples where the word is found.

        Example:
            >>> grid = WordGrid(["XCATX"])
            >>> grid.find("CAT")
            [(0, 1, <Dir.RIGHT: (0, 1)>)]
        """
        results = []
        for row in range(self.__rows):
            for col in range(self.__cols):
                for direction in Dir:
                    if self.find_at(word, row, col, direction):
                        results.append((row, col, direction))
        return results
