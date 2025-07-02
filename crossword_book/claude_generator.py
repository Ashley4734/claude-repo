import os
import json
from typing import List

import anthropic

from .pdf_book import Puzzle


def generate_puzzles_with_claude(theme: str, num: int, size: int = 13) -> List[Puzzle]:
    """Generate crossword puzzles using Anthropic's Claude API.

    The function sends a prompt asking Claude to create ``num`` crossword grids
    related to ``theme``. Claude is instructed to respond with JSON like:

    ``{"puzzles": [{"grid": [["A", ""], ...], "words": ["WORD", ...]}, ...]}``
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")

    client = anthropic.Anthropic(api_key=api_key)
    prompt = (
        f"Generate {num} crossword puzzles on the theme '{theme}'. "
        "Return JSON with a 'puzzles' list where each item has 'grid' (a 2D "
        "array of letters, using empty strings for blanks) and 'words' used."
    )

    msg = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    content = msg.content
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Claude response was not valid JSON") from exc

    puzzles: List[Puzzle] = []
    for item in data.get("puzzles", []):
        grid = item.get("grid")
        words = item.get("words", [])
        if isinstance(grid, list) and all(isinstance(row, list) for row in grid):
            puzzles.append(Puzzle(grid=grid, words=words))
    return puzzles
