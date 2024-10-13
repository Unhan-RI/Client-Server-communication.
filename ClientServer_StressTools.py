import socket
import threading
import time

# Fungsi client untuk mengirim dan menerima pesan serta mencatat waktu
def client_send_message(client_id, server_host, server_port, message, result_list):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((server_host, server_port))  # Koneksi ke server

            # Kirim pesan ke server
            send_time = time.time()
            s.sendall(message.encode())

            # Terima balasan dari server
            response = s.recv(1024).decode()

            # Terima konfirmasi bahwa pesan diterima
            confirmation = s.recv(1024).decode()

            # Hitung waktu round-trip
            receive_time = time.time()
            round_trip_time = receive_time - send_time

            # Estimasi latency sebagai setengah dari round-trip time
            latency = round_trip_time / 2

            print(f"[Client {client_id}] Round-trip time: {round_trip_time:.4f} seconds, Latency: {latency:.4f} seconds")

            # Simpan hasil ke result_list
            result_list.append((client_id, round_trip_time, latency))

        except Exception as e:
            print(f"[Client {client_id}] Failed: {e}")

# Fungsi untuk menjalankan simulasi dengan banyak klien
def simulate_multiple_clients(num_clients, server_host, server_port, message):
    threads = []
    result_list = []  # Menyimpan hasil tiap klien
    start_time = time.time()

    # Membuat dan menjalankan thread untuk setiap klien
    for i in range(num_clients):
        client_thread = threading.Thread(
            target=client_send_message, 
            args=(i + 1, server_host, server_port, message, result_list)
        )
        client_thread.start()
        threads.append(client_thread)

    # Tunggu semua thread selesai
    for t in threads:
        t.join()

    end_time = time.time()
    total_duration = end_time - start_time

    # Tampilkan hasil detail dari tiap klien
    print("\n--- Detailed Results ---")
    for client_id, rt, lat in result_list:
        print(f"Client {client_id}: Round-trip time = {rt:.4f} s, Latency = {lat:.4f} s")

    # Hitung statistik performa
    if result_list:
        total_round_trip_time = sum(rt for _, rt, _ in result_list)
        total_latency = sum(lat for _, _, lat in result_list)

        avg_round_trip_time = total_round_trip_time / len(result_list)
        avg_latency = total_latency / len(result_list)
        throughput = num_clients / total_duration if total_duration > 0 else 0

        print("\n--- Summary ---")
        print(f"Total Round-trip Time: {total_round_trip_time:.4f} seconds")
        print(f"Total Latency: {total_latency:.4f} seconds")
        print(f"Average Round-trip Time: {avg_round_trip_time:.4f} seconds")
        print(f"Average Latency: {avg_latency:.4f} seconds")
        print(f"Throughput: {throughput:.2f} requests per second")
        print(f"Total Duration: {total_duration:.4f} seconds")
    else:
        print("No successful client connections.")

# Main function untuk menjalankan pengujian
if __name__ == "__main__":
    # Input konfigurasi server dan pesan
    server_host = input("Enter server IP: ").strip()
    server_port = int(input("Enter server port: ").strip())
    num_clients = int(input("Enter the number of clients to simulate: ").strip())
    message = input("Enter the message to send: ").strip()

    # Mulai simulasi
    simulate_multiple_clients(num_clients, server_host, server_port, message)
