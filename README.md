##Book Organizer CLI
Aplikasi pengolahan data koleksi buku berbasis command line yang dibangun di Python. Aplikasi ini membantu pembaca maupun pengelola koleksi kecil untuk mencatat buku, mengelola banyak genre per buku, mencari dan memfilter data, menghapus data duplikat, melihat ringkasan statistik, serta memuat atau menyimpan data dalam format JSON dan CSV.

#1. Analisis Masalah dan Rancangan
Permasalahan: Mencatat metadata buku, berbagai genre/kategori, data ganda (duplikat), serta rekapitulasi koleksi secara manual di catatan terpisah sering kali membuat data tidak rapi dan sulit ditelusuri.

Tujuan Aplikasi: Menyediakan menu interaktif di terminal untuk menambah, menghapus, mencari, memfilter, mengelompokkan, menduplikasi/membersihkan data ganda, merangkum statistik, serta mengimpor/mengekspor data buku (id, title, author, genres, year, rating).

Target Pengguna: Pembaca individu, mahasiswa, atau pengelola koleksi buku skala kecil yang terbiasa menjalankan program melalui command line.

Format Input dan Output:
CLI Interaktif: Pilihan menu (0–10) serta prompt input teks dan angka.
File (data/): Format JSON (.json) dan CSV (.csv, menggunakan tanda ; untuk memisahkan beberapa genre di dalam satu kolom).
Minimal Tiga Fitur Utama:
Menampilkan seluruh buku terurut berdasarkan ID (1) serta menambah dan menghapus data buku (2, 3).
Mencari buku berdasarkan kata kunci pada ID, judul, penulis, atau genre (4), serta memfilter dan mengelompokkan buku berdasarkan satu atau beberapa genre (5).
Menghapus data duplikat (6), menampilkan rekapitulasi statistik (7), serta memuat dan menyimpan file JSON atau CSV (8, 9).

#2. Struktur Proyek dan Dependensi

book_organizer/
├── README.md
├── src/
│   └── main.py
├── data/
│   ├── current_books.py
│   ├── current_books.csv
│   ├── books_data.json
│   └── books_saved.json
└── extras/
    ├── __init__.py
    ├── cli.py
    ├── operations.py
    └── storage.py


Dependensi: Menggunakan Python 3.10+ dan Python Standard Library saja (csv, json, sys, pathlib, typing, operator). Tidak memerlukan instalasi package pihak ketiga (pip).

#3. Struktur Data dan Alur Antar-Module

list: Menyimpan urutan koleksi buku, hasil pencarian/filter, daftar genre pada tiap buku (genres bertipe list[str]), serta daftar nilai rating untuk perhitungan rekapitulasi.

dict: Merepresentasikan setiap data buku (id, title, author, genres, year, rating), pengelompokan buku per genre, jumlah buku per genre, dan ringkasan statistik.

set: Mengambil daftar genre unik dari seluruh koleksi serta melacak kunci (id, title) yang sudah dinormalisasi saat menghapus data duplikat.

Alur Dependensi dan Pemanggilan Antar-Module:

src/main.py menentukan direktori root proyek, mencoba membaca CURRENT_BOOKS dari data/current_books.py terlebih dahulu, lalu beralih ke fallback data/books_data.json atau data/current_books.csv apabila data utama tidak tersedia atau kosong.

src/main.py mengirimkan data buku dan path folder data/ ke fungsi run_cli() di dalam extras/cli.py.

extras/cli.py meneruskan pilihan menu ke fungsi-fungsi khusus pada extras/operations.py (tambah, hapus, cari, filter, kelompokkan, deduplikasi, rekapitulasi) dan extras/storage.py (baca, validasi, simpan, parse genre).

#4. Cara Menjalankan Aplikasi

Buka terminal di folder utama book_organizer/, lalu jalankan perintah berikut:

python src/main.py


#5. Exception Handling, Edge Case, dan Catatan Debugging

Defensive Programming dan Exception Handling: Input angka (year, rating) divalidasi tipe data dan rentangnya (year antara 1000 dan 2100, rating antara 0.0 dan 5.0). Proses baca/tulis file menangani FileNotFoundError, ValueError, json.JSONDecodeError, csv.Error, dan OSError agar aplikasi tidak berhenti mendadak.

Edge Case yang Ditangani: Menangani koleksi kosong (mengembalikan jumlah 0 dan nilai min/maks None secara aman), entri buku duplikat, input genre kosong atau hanya tanda koma, serta data lama berformat "genre" tunggal yang dinormalisasi menjadi "genres".

Skenario Debugging (Baris Tidak Valid dan Duplikat): Saat memuat file JSON atau CSV yang mengandung baris tidak valid (misalnya tahun bukan angka atau rating di luar rentang), storage.py melewati baris bermasalah tersebut dan menampilkan peringatan tanpa menggagalkan seluruh proses muat; data ganda kemudian dapat dibersihkan langsung lewat menu nomor 6 (Deduplicate).
