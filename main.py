from crossword_book.word_provider import fetch_theme_words
from crossword_book.crossword import generate_crossword
from crossword_book.pdf_book import CrosswordPDFBook, Puzzle
from crossword_book.claude_generator import generate_puzzles_with_claude
import argparse
import random


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a crossword puzzle book for KDP")
    parser.add_argument("theme", help="Theme for the crossword puzzles")
    parser.add_argument("num_puzzles", type=int, help="Number of puzzles to generate")
    parser.add_argument("--size", default="6x9", choices=["6x9", "8x11"], help="Book size")
    parser.add_argument("--output", default="crossword_book.pdf", help="Output PDF filename")
    parser.add_argument("--use-claude", action="store_true", help="Generate puzzles with Claude instead of the local generator")
    args = parser.parse_args()

    words = fetch_theme_words(args.theme, max_words=100)
    if not words:
        raise SystemExit("Could not fetch words for theme")

    if args.use_claude:
        puzzles = generate_puzzles_with_claude(args.theme, args.num_puzzles)
    else:
        puzzles = []
        for _ in range(args.num_puzzles):
            random_words = random.sample(words, min(len(words), 10))
            grid = generate_crossword(random_words)
            puzzles.append(Puzzle(grid=grid, words=random_words))

    book = CrosswordPDFBook(args.theme, puzzles, size=args.size)
    book.build(args.output)
    print(f"Book saved to {args.output}")


if __name__ == "__main__":
    main()
