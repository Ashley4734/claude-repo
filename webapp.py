import random
from io import BytesIO

from flask import Flask, request, render_template_string, send_file

from crossword_book.word_provider import fetch_theme_words
from crossword_book.crossword import generate_crossword
from crossword_book.pdf_book import CrosswordPDFBook, Puzzle

app = Flask(__name__)

INDEX_HTML = """
<!doctype html>
<title>Crossword Puzzle Generator</title>
<h1>Create Crossword Puzzles</h1>
<form method="post" action="/generate">
  Theme: <input name="theme" required><br>
  Number of puzzles: <input type="number" name="num" value="1" min="1" max="10"><br>
  <button type="submit">Generate</button>
</form>
"""

PUZZLE_HTML = """
<!doctype html>
<title>Puzzles for {{theme}}</title>
<h1>Puzzles for {{theme}}</h1>
{% for grid in grids %}
<table border="1" style="border-collapse: collapse; margin-bottom:20px">
  {% for row in grid %}
  <tr>
    {% for cell in row %}
    <td style="width:20px;height:20px;text-align:center">{{cell}}</td>
    {% endfor %}
  </tr>
  {% endfor %}
</table>
{% endfor %}
<form method="post" action="/pdf">
  <input type="hidden" name="theme" value="{{theme}}">
  <input type="hidden" name="num" value="{{num}}">
  <button type="submit">Download PDF</button>
</form>
"""

@app.route("/")
def index():
    return INDEX_HTML


@app.route("/generate", methods=["POST"])
def generate():
    theme = request.form.get("theme", "").strip()
    try:
        num = int(request.form.get("num", 1))
    except ValueError:
        num = 1
    if not theme:
        return "Theme required", 400

    words = fetch_theme_words(theme, max_words=100)
    if not words:
        return "Could not fetch words for theme", 400

    grids = []
    for _ in range(num):
        sample = random.sample(words, min(len(words), 10))
        grid = generate_crossword(sample)
        grids.append(grid)
    return render_template_string(PUZZLE_HTML, theme=theme, grids=grids, num=num)


@app.route("/pdf", methods=["POST"])
def pdf():
    theme = request.form.get("theme", "")
    try:
        num = int(request.form.get("num", 1))
    except ValueError:
        num = 1

    words = fetch_theme_words(theme, max_words=100)
    if not words:
        return "Could not fetch words for theme", 400

    puzzles = []
    for _ in range(num):
        sample = random.sample(words, min(len(words), 10))
        grid = generate_crossword(sample)
        puzzles.append(Puzzle(grid=grid, words=sample))

    book = CrosswordPDFBook(theme, puzzles)
    buffer = BytesIO()
    book.build(buffer)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="crossword_book.pdf", mimetype="application/pdf")


if __name__ == "__main__":
    app.run(debug=True)
