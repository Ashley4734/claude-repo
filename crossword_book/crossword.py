from __future__ import annotations

import random
from typing import List, Optional, Tuple


def create_empty_grid(size: int) -> List[List[str]]:
    return [["" for _ in range(size)] for _ in range(size)]


def can_place_word(grid: List[List[str]], word: str, row: int, col: int, direction: str) -> bool:
    size = len(grid)
    if direction == "across":
        if col + len(word) > size:
            return False
        for i, ch in enumerate(word):
            cell = grid[row][col + i]
            if cell not in ("", ch):
                return False
    else:  # down
        if row + len(word) > size:
            return False
        for i, ch in enumerate(word):
            cell = grid[row + i][col]
            if cell not in ("", ch):
                return False
    return True


def place_word(grid: List[List[str]], word: str, row: int, col: int, direction: str) -> None:
    if direction == "across":
        for i, ch in enumerate(word):
            grid[row][col + i] = ch
    else:
        for i, ch in enumerate(word):
            grid[row + i][col] = ch


def find_place_for_word(grid: List[List[str]], word: str) -> Optional[Tuple[int, int, str]]:
    size = len(grid)
    indices = list(range(size))
    random.shuffle(indices)
    for row in indices:
        for col in indices:
            for direction in ("across", "down"):
                if can_place_word(grid, word, row, col, direction):
                    return row, col, direction
    return None


def generate_crossword(words: List[str], size: int = 13) -> List[List[str]]:
    grid = create_empty_grid(size)
    for word in words:
        pos = find_place_for_word(grid, word)
        if pos:
            row, col, direction = pos
            place_word(grid, word, row, col, direction)
    return grid
