Tabel Hasil Pengujian Benchmark

=================================================================
Data Count   | XML (Bytes)  | JSON (Bytes) | Efisiensi (%)  
=================================================================
10           | 1438         | 1166         | 18.92%
50           | 7058         | 5826         | 17.46%
100          | 14084        | 11652        | 17.27%
500          | 70684        | 58652        | 17.02%
=================================================================

Analisis Pertanyaan Kritis

1. Analisis struktur payload

XML menghasilkan ukuran data yang lebih besar karena menggunakan tag pembuka dan tag penutup pada setiap elemen. Contohnya, XML menggunakan format <nama>Dewi Sartika</nama>, sedangkan JSON cukup menggunakan "nama":"Dewi Sartika".
XML juga membutuhkan struktur elemen bertingkat, seperti <response>, <students>, dan <student>. Tag-tag tersebut menambah jumlah karakter yang dikirim melalui jaringan. JSON menggunakan pasangan key-value dan tanda kurung kurawal sehingga sintaksnya lebih ringkas. Akibatnya, JSON umumnya memiliki ukuran payload lebih kecil dibandingkan XML untuk data yang sama.

2. Analisis deserialisasi atau parsing di sisi klien

JSON dapat diproses oleh JavaScript menggunakan JSON.parse() atau secara otomatis melalui response.json() pada Fetch API. Hasilnya berupa objek atau array JavaScript yang dapat langsung digunakan untuk menampilkan data.
Sementara itu, XML biasanya diproses menggunakan DOMParser dengan tipe dokumen application/xml. Setelah diproses, aplikasi perlu menelusuri elemen dan mengambil isi tag untuk mendapatkan nilai yang dibutuhkan.
Ekosistem web modern banyak menggunakan JSON karena sintaksnya lebih ringkas, mudah dipadukan dengan JavaScript, dan umumnya membutuhkan lebih sedikit data untuk ditransmisikan. Hal ini membuat JSON praktis untuk komunikasi antara front-end dan REST API.

3. Bottleneck arsitektur RESTful synchronous

Pada komunikasi sinkron, setiap klien menunggu respons dari server sampai proses yang diperlukan selesai. Jika sistem legacy membutuhkan waktu untuk melakukan file locking dan menulis data, permintaan POST lainnya dapat tertunda atau mengantre ketika berebut akses ke file tersebut.
Jika jumlah permintaan terus meningkat, waktu respons akan semakin panjang. Koneksi dan thread yang menunggu dapat menggunakan sumber daya server sehingga berpotensi menimbulkan bottleneck atau kehabisan sumber daya (resource exhaustion).
gRPC yang menggunakan HTTP/2 mendukung multiplexing, sehingga beberapa aliran komunikasi dapat berlangsung melalui satu koneksi. Hal ini membantu mengurangi keterbatasan pengiriman permintaan secara berurutan pada HTTP/1.1, meskipun tidak otomatis menghilangkan antrean pada file legacy.
Sementara itu, Asynchronous Message Broker memungkinkan permintaan diterima dan dimasukkan ke antrean untuk diproses oleh pekerja secara terpisah. Klien tidak harus menunggu seluruh operasi penulisan legacy selesai sebelum proses penerimaan pesan berakhir. Namun, jika penyimpanan legacy tetap lambat, antrean masih bisa menumpuk dan perlu dikelola.