# LAPORAN ANALISIS PRAKTIKUM
## Integrasi Sistem Enterprise Application Integration (EAI)

### 1. Analisis Pola Arsitektur

**Pertanyaan:** Mengapa rancangan tersebut termasuk Adapter Pattern dalam EAI? Apa keuntungan yang didapat klien web?

**Jawaban:**

Rancangan tersebut termasuk Adapter Pattern karena menggunakan adapter berbasis Python sebagai perantara antara klien web dan sistem legacy yang dibuat menggunakan bahasa C. Adapter bertugas menerjemahkan permintaan HTTP dan data XML menjadi operasi yang dapat diproses oleh sistem legacy, termasuk membaca dan menulis data pada file `students_db.txt`.

Keuntungan bagi klien web adalah dapat mengakses dan menambahkan data mahasiswa melalui protokol HTTP dengan format XML tanpa harus memahami cara kerja internal sistem legacy. Adapter juga membantu mengurangi ketergantungan antara klien dan sistem legacy sehingga pemeliharaan serta pengembangan aplikasi menjadi lebih mudah.

### 2. Analisis Overhead Serialisasi Data

**Pertanyaan:** Hitung jumlah byte data aktual, total byte respons XML, dan persentase overhead.

**Jawaban:**

Data mahasiswa yang digunakan sebagai contoh adalah sebagai berikut:

| Data | Jumlah Byte |
|---|---:|
| NIM: 2415354001 | 10 |
| Nama: I Made Sujana | 13 |
| Jurusan: Teknologi Informasi | 19 |
| Status: ACTIVE | 6 |
| **Total data aktual** | **48** |

Respons XML memiliki ukuran 182 byte berdasarkan hasil perhitungan pada jobsheet, termasuk deklarasi XML dan karakter baris baru setelah deklarasi.

Perhitungan overhead:

Overhead = Total byte XML − Data aktual

Overhead = 182 − 48 = 134 byte

Persentase overhead dihitung dengan rumus:

Persentase overhead = (Overhead / Data aktual) × 100%

Persentase overhead = (134 / 48) × 100% = 279,17%

Dengan demikian, overhead XML adalah 134 byte atau 279,17% dari ukuran data aktual. XML memiliki ukuran lebih besar karena terdapat deklarasi, tag pembuka, tag penutup, dan struktur elemen yang digunakan untuk menjelaskan data.

Catatan: ukuran 182 byte perlu dipastikan kembali dengan menghitung langsung hasil XML dari program. Header HTTP tidak termasuk dalam perhitungan ini.

### 3. Prediksi Keterbatasan Integrasi

**Pertanyaan:** Apa yang terjadi jika 500 permintaan POST datang bersamaan, dan mengapa Message Broker dibutuhkan?

**Jawaban:**

Jika terdapat 500 permintaan POST dalam waktu yang hampir bersamaan, server perlu memproses banyak permintaan penambahan data mahasiswa. Apabila menggunakan `HTTPServer` standar Python yang menangani permintaan secara berurutan, permintaan lainnya harus menunggu hingga permintaan sebelumnya selesai diproses. Kondisi tersebut dapat meningkatkan waktu tunggu ketika beban permintaan tinggi.

Jika sistem dikembangkan agar beberapa proses dapat menulis data secara bersamaan, diperlukan mekanisme sinkronisasi untuk mencegah konflik penulisan dan menjaga konsistensi data.

Message Broker dapat digunakan untuk menerima dan mengantrekan permintaan sebelum diteruskan kepada komponen pemroses. Dengan antrean tersebut, permintaan dapat diproses secara teratur, beban server dapat dikendalikan, dan mekanisme percobaan ulang dapat diterapkan jika terjadi kegagalan.

Selain menggunakan Message Broker, sistem juga perlu menerapkan validasi data, pengendalian akses tulis, serta pemeriksaan duplikasi agar integritas data tetap terjaga.

### Kesimpulan

Adapter Pattern memudahkan integrasi antara aplikasi modern dan sistem legacy tanpa mengharuskan perubahan besar pada sistem lama. XML memberikan struktur data yang jelas, tetapi menambah ukuran payload. Sementara itu, Message Broker dapat membantu pengelolaan antrean dan beban permintaan ketika sistem berkembang dan menerima banyak permintaan secara bersamaan.