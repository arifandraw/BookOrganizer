import csv
import json
from operator import itemgetter
from pathlib import Path
from typing import Any

from extras.operations import (
    add_book,
    filter_by_genre,
    get_unique_genres,
    group_by_genre,
    remove_book,
    search_books,
    summarize_books,
)
from extras.storage import (
    deduplicate_books,
    load_books_from_file,
    save_books_to_file,
)


def print_menu() -> None:
    print(
        "\n========================================\n"
        "              BOOK ORGANIZER\n"
        "========================================\n"
        "  1. Show All Books\n"
        "  2. Add a Book\n"
        "  3. Remove a Book\n"
        "  4. Search Books\n"
        "  5. Filter by Genre\n"
        "  6. Deduplicate Books\n"
        "  7. Recap & Statistics Summary\n"
        "  8. Load Books from data/ (JSON/CSV)\n"
        "  9. Save Books to data/ (JSON/CSV)\n"
        " 10. Exit\n"
        "  0. Show Menu Again\n"
        "========================================"
    )


def display_books(books: list[dict[str, Any]], heading: str = "BOOK LIST") -> None:
    print(f"\n--- {heading} ({len(books)}) ---")
    if not books:
        print("\033[3mNo books to display.\033[0m")
        return
    for b in books:
        genres_str = ", ".join(b.get("genres", []))
        print(
            f"{b['id']:<6} | "
            f"{b['title']:<26} | "
            f"{b['author']:<18} | "
            f"{genres_str:<26} | "
            f"\033[2m{b['year']} | * {b['rating']}\033[0m"
        )


def _prompt_int(prompt: str) -> int | None:
    raw = input(prompt).strip()
    try:
        return int(raw)
    except ValueError:
        print("\033[3mInvalid whole number input.\033[0m")
        return None


def _prompt_float(prompt: str) -> float | None:
    raw = input(prompt).strip()
    try:
        return float(raw)
    except ValueError:
        print("\033[3mInvalid decimal/number input.\033[0m")
        return None


def run_cli(
    initial_books: list[dict[str, Any]],
    data_dir: Path,
    save_dir: Path,
) -> None:
    books = [dict(b, genres=list(b.get("genres", []))) for b in initial_books]
    print_menu()

    while True:
        choice = input("\nChoose an option (0-10): ").strip()

        if choice == "0":
            print_menu()

        elif choice == "1":
            sorted_books = sorted(books, key=itemgetter("id"))
            display_books(sorted_books, "ALL BOOKS")

        elif choice == "2":
            book_id = input("Book ID (e.g., B006): ").strip()
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            genres_raw = input("Genres (comma-separated, e.g. Sci-Fi, Adventure): ").strip()
            year = _prompt_int("Publication Year (e.g., 2024): ")
            rating = _prompt_float("Rating (0.0 - 5.0): ")
            if year is not None and rating is not None:
                books, msg = add_book(books, book_id, title, author, genres_raw, year, rating)
                print(msg)

        elif choice == "3":
            display_books(sorted(books, key=itemgetter("id")), "CURRENT BOOKS")
            identifier = input("Enter Book ID or exact Title to remove: ").strip()
            books, removed = remove_book(books, identifier)
            if removed:
                print(f"Removed '{removed['title']}' ({removed['id']}).")
            else:
                print("\033[3mNo matching book found to remove.\033[0m")

        elif choice == "4":
            keyword = input("Enter search keyword: ").strip()
            results = search_books(books, keyword)
            display_books(results, f"SEARCH RESULTS FOR '{keyword}'")

        elif choice == "5":
            unique_genres = sorted(get_unique_genres(books))
            print("Available genres:", ", ".join(unique_genres) if unique_genres else "None")
            selected_genres = input("Enter genre(s) to filter (comma-separated): ").strip()
            filtered = filter_by_genre(books, selected_genres)
            display_books(filtered, f"GENRE(S): {selected_genres}")
            grouped = group_by_genre(books)
            print("Counts per genre:", {g: len(items) for g, items in sorted(grouped.items())})

        elif choice == "6":
            books, removed_count = deduplicate_books(books)
            print(f"Deduplication complete. Removed {removed_count} duplicate record(s).")

        elif choice == "7":
            summary = summarize_books(books)
            print("\n--- RECAP & SUMMARY ---")
            print(f"Total books        : \033[2m{summary['total_books']}\033[0m")
            print(f"Unique genres      : \033[2m{summary['unique_genre_count']}\033[0m")
            print(f"Average rating     : \033[2m{summary['avg_rating']}\033[0m")
            print(f"Highest rating     : \033[2m{summary['highest_rating']}\033[0m")
            print(f"Lowest rating      : \033[2m{summary['lowest_rating']}\033[0m")
            print(f"Books by genre     : \033[2m{summary['count_by_genre']}\033[0m")

        elif choice == "8":
            filename = input(f"Enter filename inside (default: books_list1.json): ").strip() or "books_data.json"
            target_path = Path(filename) if Path(filename).is_absolute() else data_dir / filename
            try:
                loaded, warnings = load_books_from_file(str(target_path))
                books = loaded
                print(f"Loaded {len(books)} valid book(s) from '{target_path}'.")
                for w in warnings:
                    print(f"\033[3mWarning: {w}\033[0m")
            except (FileNotFoundError, ValueError, json.JSONDecodeError, csv.Error) as exc:
                print(f"\033[3mFailed to load file: {exc}\033[0m")

        elif choice == "9":
            filename = input(f"Enter output filename inside (example: book_list3.json): ").strip() or "books_saved.json"
            target_path = Path(filename) if Path(filename).is_absolute() else save_dir / filename
            try:
                saved_path = save_books_to_file(books, str(target_path))
                print(f"Saved {len(books)} book(s) to '{saved_path}'.")
            except (ValueError, OSError) as exc:
                print(f"\033[3mFailed to save file: {exc}\033[0m")

        elif choice == "10":
            print("\033[3m- Thank you, Program Closed -\033[0m\n")
            break

        else:
            print("\033[3mInvalid choice. Enter 0-10.\033[0m")
