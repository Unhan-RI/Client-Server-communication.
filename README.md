# Sistem Client Server dengan load balancing + Stress tools
# Pendahuluan
Dokumen ini memberikan gambaran tentang sistem Client server yang memiliki beberapa server, load balancing, dan kemampuan uji stres. Sistem ini dirancang untuk menangani banyak klien secara bersamaan, memastikan kinerja dan ketersediaan melalui distribusi beban yang efisien.

# 1. client.py
File client.py berisi kode sisi klien yang bertugas mengirim pesan ke server dan menerima balasan. Kode ini juga mencatat waktu respons round-trip dan latensi untuk setiap koneksi dengan server.
Fungsi Utama:
- client_send_message(): Membuka koneksi socket, mengirim pesan, dan menerima dua balasan: pesan utama dan konfirmasi.
- Mengukur waktu round-trip dan memperkirakan latensi.
# 2. ClientServer_StressTools.py
Script ini berfungsi sebagai alat uji stres dengan membuat banyak klien yang mengirim permintaan secara bersamaan ke server. Menggunakan threading untuk memastikan eksekusi paralel dan mengukur metrik performa seperti throughput dan latensi.
# 3. File Server (Server 1, Server 2, Server 3)
Setiap file server berfungsi sebagai server sederhana yang mendengarkan koneksi masuk, menerima pesan dari klien, dan mengirimkan balasan. Server-server ini dapat digunakan secara independen atau bersama dengan load balancer.
# 4. Load_Balancer.py
Script Load_Balancer.py bertugas mendistribusikan permintaan klien di antara beberapa server untuk memastikan tidak ada satu server yang kelebihan beban. Load balancer juga mendukung ketersediaan tinggi dengan mengalihkan lalu lintas jika salah satu server gagal.
# 5. client_log.log
Log klien ini mencatat semua aktivitas yang dilakukan oleh klien, termasuk waktu pengiriman pesan, penerimaan balasan, dan perhitungan waktu round-trip. Log ini membantu memonitor performa klien dan mendiagnosis masalah konektivitas.
# 6. server_log.log
Log server ini mencatat setiap koneksi yang dibuat dengan klien, termasuk pesan yang diterima dan balasan yang dikirim. Log ini memberikan wawasan tentang kinerja server dan membantu mengidentifikasi potensi masalah dalam menangani permintaan.
# Ringkasan dan Kesimpulan
Sistem Client Server dengan load balancing ini menunjukkan kemampuan untuk menangani koneksi klien secara bersamaan dengan efisien. Dengan beberapa server yang dikelola oleh load balancer, sistem ini memastikan ketersediaan tinggi dan distribusi beban yang baik. Alat uji stres memberikan wawasan berharga tentang performa sistem melalui metrik seperti latensi, waktu round-trip, dan throughput.

