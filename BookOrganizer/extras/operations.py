from typing import Any
from extras.storage import parse_genres

def add_book(
    books: list[dict[str, Any]],
    book_id: str,
    title: str,
    author: str,
    genres_input: str | list[str],
    year: int,
    rating: float = 0.0,
) -> tuple[list[dict[str, Any]], str]:
    norm_id = book_id.strip().upper()
    clean_title = title.strip()
    clean_author = author.strip()
    clean_genres = parse_genres(genres_input)

    if not (norm_id and clean_title and clean_author and clean_genres):
        return list(books), "Error: ID, title, author, and at least one genre are required."
    if any(b["id"].upper() == norm_id for b in books):
        return list(books), f"Error: A book with ID '{norm_id}' already exists."
    if year < 1000 or year > 2100 or not (0.0 <= rating <= 5.0):
        return list(books), "Error: Year must be 1000-2100 and rating must be 0.0-5.0."

    updated = [dict(b, genres=list(b.get("genres", []))) for b in books]
    updated.append({
        "id": norm_id,
        "title": clean_title,
        "author": clean_author,
        "genres": clean_genres,
        "year": int(year),
        "rating": round(float(rating), 2),
    })
    return updated, f"Added '{clean_title}' ({norm_id}) with genres: {', '.join(clean_genres)}."


def remove_book(books: list[dict[str, Any]], identifier: str) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    target = identifier.strip().lower()
    if not target:
        return list(books), None

    removed_item: dict[str, Any] | None = None
    remaining: list[dict[str, Any]] = []

    for book in books:
        if removed_item is None and (
            book["id"].lower() == target or book["title"].lower() == target
        ):
            removed_item = dict(book, genres=list(book.get("genres", [])))
        else:
            remaining.append(dict(book, genres=list(book.get("genres", []))))

    return remaining, removed_item


def search_books(books: list[dict[str, Any]], keyword: str) -> list[dict[str, Any]]:
    q = keyword.strip().lower()
    if not q:
        return []
    return [
        b for b in books
        if q in b["id"].lower()
        or q in b["title"].lower()
        or q in b["author"].lower()
        or any(q in g.lower() for g in b.get("genres", []))
    ]


def filter_by_genre(books: list[dict[str, Any]], genre_query: str) -> list[dict[str, Any]]:
    targets = {g.lower() for g in parse_genres(genre_query)}
    if not targets:
        return []
    return [
        b for b in books
        if any(g.lower() in targets for g in b.get("genres", []))
    ]


def group_by_genre(books: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for book in books:
        for genre in book.get("genres", []):
            grouped.setdefault(genre, []).append(dict(book, genres=list(book.get("genres", []))))
    return grouped


def get_unique_genres(books: list[dict[str, Any]]) -> set[str]:
    return {
        genre.strip()
        for book in books
        for genre in book.get("genres", [])
        if genre.strip()
    }


def summarize_books(books: list[dict[str, Any]]) -> dict[str, Any]:
    if not books:
        return {
            "total_books": 0,
            "unique_genre_count": 0,
            "avg_rating": 0.0,
            "highest_rating": None,
            "lowest_rating": None,
            "count_by_genre": {},
        }

    grouped = group_by_genre(books)
    ratings = [b["rating"] for b in books]
    count_by_genre = {genre: len(items) for genre, items in sorted(grouped.items())}

    return {
        "total_books": len(books),
        "unique_genre_count": len(get_unique_genres(books)),
        "avg_rating": round(sum(ratings) / len(ratings), 2),
        "highest_rating": max(ratings),
        "lowest_rating": min(ratings),
        "count_by_genre": count_by_genre,
    }
