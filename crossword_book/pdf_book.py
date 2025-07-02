from __future__ import annotations

from dataclasses import dataclass
from typing import List

from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors


PAGE_SIZES = {
    "6x9": (6 * inch, 9 * inch),
    "8x11": (8 * inch, 11 * inch),
}


def draw_grid(c: canvas.Canvas, grid: List[List[str]], x: float, y: float, size: float) -> None:
    cell_size = size / len(grid)
    for r, row in enumerate(grid):
        for c_idx, ch in enumerate(row):
            px = x + c_idx * cell_size
            py = y + (len(grid) - r - 1) * cell_size
            c.rect(px, py, cell_size, cell_size)
            if ch:
                c.drawCentredString(px + cell_size / 2, py + cell_size / 2 - 4, ch)


@dataclass
class Puzzle:
    grid: List[List[str]]
    words: List[str]


class CrosswordPDFBook:
    def __init__(self, theme: str, puzzles: List[Puzzle], size: str = "6x9"):
        if size not in PAGE_SIZES:
            raise ValueError(f"Unknown page size: {size}")
        self.page_width, self.page_height = PAGE_SIZES[size]
        self.theme = theme
        self.puzzles = puzzles

    def build(self, filename: str) -> None:
        c = canvas.Canvas(filename, pagesize=(self.page_width, self.page_height))
        title = f"Crossword Puzzle Book: {self.theme.title()}"
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(self.page_width / 2, self.page_height - 50, title)
        c.showPage()
        puzzle_area = self.page_height / 2
        for i, puzzle in enumerate(self.puzzles):
            if i % 2 == 0:
                ypos = puzzle_area
            else:
                ypos = 0
            draw_grid(c, puzzle.grid, 50, ypos + 50, self.page_width - 100)
            if i % 2 == 1 or i == len(self.puzzles) - 1:
                c.showPage()
        # Answers section
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(self.page_width / 2, self.page_height - 50, "Answers")
        c.showPage()
        for i, puzzle in enumerate(self.puzzles):
            if i % 2 == 0:
                ypos = puzzle_area
            else:
                ypos = 0
            draw_grid(c, puzzle.grid, 50, ypos + 50, self.page_width - 100)
            if i % 2 == 1 or i == len(self.puzzles) - 1:
                c.showPage()
        c.save()
