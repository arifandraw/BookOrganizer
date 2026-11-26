# Book Organizer

Aplikasi CLI (Command-Line Interface) berbasis Python untuk mengelola koleksi buku pribadi atau perpustakaan kecil dengan dukungan **multi-genre** per buku, pencarian, filtering, pengelompokan, deduplikasi, rekapitulasi statistik, serta pemrosesan file JSON dan CSV.

## Masalah, Target Pengguna, Input-Output & Fitur Utama

* **Permasalahan & Tujuan:** Pengguna sering kesulitan mencatat metadata buku, mengelompokkan buku dengan banyak genre, menghindari data ganda, dan menyimpan perubahan secara terstruktur. Aplikasi ini menyediakan menu interaktif di terminal untuk mengelola data buku secara rapi.
* **Target Pengguna:** Pembaca individu, mahasiswa, atau pengelola koleksi buku skala kecil yang menggunakan terminal Python.
* **Format Input & Output:** Input interaktif melalui terminal serta file **JSON** (`.json`) dan **CSV** (`.csv`, dengan multi-genre dipisahkan titik koma `;`). Output ditampilkan dalam format tabel teks di CLI dan dapat disimpan ke file JSON/CSV di folder `data/`.
* **Fitur Utama:**
  * Menampilkan daftar buku terurut berdasarkan ID serta menambah atau menghapus buku.
  * Mencari buku berdasarkan kata kunci (ID, judul, penulis, atau genre) dan memfilter/mengelompokkan berdasarkan satu atau beberapa genre.
  * Menghapus data duplikat, menampilkan ringkasan statistik, serta memuat dan menyimpan data ke file JSON/CSV.

## Struktur Folder & Alur Modul

```text
book_organizer/
├── README.md
├── src/
│   └── main.py
├── data/
│   ├── current_books.py
│   ├── current_books.csv
│   └── books_data.json
└── extras/
    ├── __init__.py
    ├── cli.py
    ├── operations.py
    └── storage.py
