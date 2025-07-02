import requests


def fetch_theme_words(theme: str, max_words: int = 50) -> list[str]:
    """Fetch words related to a theme from the Datamuse API."""
    url = "https://api.datamuse.com/words"
    params = {"ml": theme, "max": max_words}
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        words = [item["word"] for item in data]
        return [w.upper() for w in words if w.isalpha()]
    except Exception:
        return []
