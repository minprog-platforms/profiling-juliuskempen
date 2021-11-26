from __future__ import annotations
from typing import Iterable, List


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        self._grid: List[List[int]] = []
        self._columns: List[List[int]] = []
        self._blocks: List[Iterable[int]] = []

        # Saving the grid by row.
        for puzzle_row in puzzle:
            row = []
            for element in puzzle_row:
                row.append(int(element))
            self._grid.append(row)

        # Saving the grid by column.
        for x in range(9):
            column = []
            for y in range(9):
                column.append(self._grid[y][x])
            self._columns.append(column)

        # Saving the grid by block.
        for i in range(9):
            values = []
            x_start = (i % 3) * 3
            y_start = (i // 3) * 3
            for x in range(x_start, x_start + 3):
                for y in range(y_start, y_start + 3):
                    values.append(self.value_at(x, y))
            self._blocks.append(values)

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        self._grid[y][x] = value
        self._columns[x][y] = value

        # Get the index of the block based from x,y.
        block_index = (y // 3) * 3 + x // 3

        # Replace the old block with the new.
        self._blocks[block_index] = self.block_values(block_index)

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        self.place(0, x, y)

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        return self._grid[y][x]

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""
        options = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # Remove all values that are cointained in the row.
        options = list(set(options) - set(self._grid[y]))

        # Remove all values that are cointained in the column.
        options = list(set(options) - set(self._columns[x]))

        # Get the index of the block based on x,y.
        block_index = (y // 3) * 3 + x // 3

        # Remove all values that are cointained in the block.
        options = list(set(options) - set(self._blocks[block_index]))

        return options

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        next_x, next_y = -1, -1

        for y in range(9):
            for x in range(9):
                if self.value_at(x, y) == 0:
                    return x, y

        return next_x, next_y

    def row_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th row."""
        return self._grid[i]

    def column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""
        return self._columns[i]

    def block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        values = []

        x_start = (i % 3) * 3
        y_start = (i // 3) * 3

        for x in range(x_start, x_start + 3):
            for y in range(y_start, y_start + 3):
                values.append(self.value_at(x, y))

        return values

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        for i in range(9):
            if list(set(values) - set(self._grid[i])):
                return False
            if list(set(values) - set(self._columns[i])):
                return False
            if list(set(values) - set(self._blocks[i])):
                return False

        return True

    def __str__(self) -> str:
        """Convert list of intergers for every row to a string"""
        representation = ""

        for row in range(9):
            for i in range(9):
                representation += str(self._grid[row][i])
            representation = representation + "\n"

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[str] = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")

            puzzle.append(line)

    return Sudoku(puzzle)
