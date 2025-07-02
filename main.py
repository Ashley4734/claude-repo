from crossword_book.word_provider import fetch_theme_words
from crossword_book.crossword import generate_crossword
from crossword_book.pdf_book import CrosswordPDFBook, Puzzle
import argparse
import random


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a crossword puzzle book for KDP")
    parser.add_argument("theme", help="Theme for the crossword puzzles")
    parser.add_argument("num_puzzles", type=int, help="Number of puzzles to generate")
    parser.add_argument("--size", default="6x9", choices=["6x9", "8x11"], help="Book size")
    parser.add_argument("--output", default="crossword_book.pdf", help="Output PDF filename")
    args = parser.parse_args()

    words = fetch_theme_words(args.theme, max_words=100)
    if not words:
        raise SystemExit("Could not fetch words for theme")


    book = CrosswordPDFBook(args.theme, puzzles, size=args.size)
    book.build(args.output)
    print(f"Book saved to {args.output}")


if __name__ == "__main__":
    main()
