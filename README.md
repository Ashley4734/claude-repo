# Crossword Book Generator

This tool generates crossword puzzle books for Amazon KDP. Provide a theme and number of puzzles and it will create a PDF formatted for either a 6"x9" or 8"x11" book with two puzzles per page and answers in the back.

## Requirements
- Python 3.10+
- `requests`
- `reportlab`
- `anthropic` (optional, for Claude integration)

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
```
python main.py "animals" 20 --size 6x9 --output animals_book.pdf
```

To generate puzzles using Claude instead of the local generator, add the
`--use-claude` flag. This requires setting the `ANTHROPIC_API_KEY`
environment variable with your API key:

```
ANTHROPIC_API_KEY=<your_key> python main.py "animals" 20 --use-claude
```

This will create `animals_book.pdf` with 20 puzzles (two per page) and solutions at the end.

The script fetches words related to the theme using the Datamuse API.
