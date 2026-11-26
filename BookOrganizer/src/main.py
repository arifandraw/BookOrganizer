import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from extras.cli import run_cli
from extras.storage import _validate_book_record, load_books_from_file

DATA_DIR = ROOT_DIR / "data"


def _load_books():
    try:
        from data.current_books import CURRENT_BOOKS
        valid = [c for b in CURRENT_BOOKS if (c := _validate_book_record(b))] if isinstance(CURRENT_BOOKS, list) else []
        if valid:
            return valid
    except Exception:
        pass

    for fallback in (DATA_DIR / "books_data.json", DATA_DIR / "current_books.csv"):
        try:
            books, _ = load_books_from_file(str(fallback))
            if books:
                return books
        except Exception:
            continue

    return []


if __name__ == "__main__":
    run_cli(_load_books(), DATA_DIR, DATA_DIR)
