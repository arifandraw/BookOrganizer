import csv
import json
from pathlib import Path
from typing import Any


def parse_genres(raw_genres: str | list[str]) -> list[str]:
    if isinstance(raw_genres, list):
        tokens = [str(g).strip() for g in raw_genres]
    elif isinstance(raw_genres, str):
        tokens = [part.strip() for part in raw_genres.replace(";", ",").split(",")]
    else:
        return []

    unique_genres: list[str] = []
    seen: set[str] = set()
    for token in tokens:
        if not token:
            continue
        key = token.lower()
        if key not in seen:
            seen.add(key)
            unique_genres.append(token)
    return unique_genres


def _validate_book_record(record: dict[str, Any]) -> dict[str, Any] | None:
    if not isinstance(record, dict):
        return None
    book_id = str(record.get("id", "")).strip().upper()
    title = str(record.get("title", "")).strip()
    author = str(record.get("author", "")).strip()

    raw_genres = record.get("genres") if "genres" in record else record.get("genre", "")
    genres = parse_genres(raw_genres)

    if not (book_id and title and author and genres):
        return None
    try:
        year = int(record.get("year"))
        rating = float(record.get("rating", 0.0))
    except (TypeError, ValueError):
        return None
    if year < 1000 or year > 2100 or not (0.0 <= rating <= 5.0):
        return None
    return {
        "id": book_id,
        "title": title,
        "author": author,
        "genres": genres,
        "year": year,
        "rating": round(rating, 2),
    }


def load_books_from_file(filepath: str) -> tuple[list[dict[str, Any]], list[str]]:
    path = Path(filepath)
    warnings: list[str] = []

    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File not found: {filepath}")

    suffix = path.suffix.lower()
    raw_records: list[dict[str, Any]] = []

    if suffix == ".json":
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, list):
            raise ValueError("JSON root must be a list of book objects.")
        raw_records = data
    elif suffix == ".csv":
        with path.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                raise ValueError("CSV file is missing a header row.")
            raw_records = list(reader)
    else:
        raise ValueError(f"Unsupported file format '{suffix}'. Use .json or .csv.")

    valid_books: list[dict[str, Any]] = []
    for idx, item in enumerate(raw_records, start=1):
        cleaned = _validate_book_record(item)
        if cleaned is None:
            warnings.append(f"Skipped invalid record #{idx}: {item}")
        else:
            valid_books.append(cleaned)

    return valid_books, warnings


def save_books_to_file(books: list[dict[str, Any]], filepath: str) -> str:
    path = Path(filepath)
    if path.parent and not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)

    suffix = path.suffix.lower()
    if suffix == ".json":
        with path.open("w", encoding="utf-8") as handle:
            json.dump(books, handle, indent=2)
    elif suffix == ".csv":
        fieldnames = ["id", "title", "author", "genres", "year", "rating"]
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for b in books:
                row = dict(b)
                row["genres"] = ";".join(b.get("genres", []))
                writer.writerow(row)
    else:
        raise ValueError(f"Unsupported output format '{suffix}'. Use .json or .csv.")

    return str(path)


def deduplicate_books(books: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    seen_keys: set[tuple[str, str]] = set()
    unique_books: list[dict[str, Any]] = []
    removed_count = 0

    for book in books:
        key = (book["id"].strip().upper(), book["title"].strip().lower())
        if key in seen_keys:
            removed_count += 1
        else:
            seen_keys.add(key)
            copy_book = dict(book)
            copy_book["genres"] = list(book.get("genres", []))
            unique_books.append(copy_book)

    return unique_books, removed_count
