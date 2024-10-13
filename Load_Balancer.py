import socket
import threading

# Daftar server yang tersedia untuk menangani permintaan
servers = [
    ('127.0.0.1', 8001),
    ('127.0.0.1', 8002),
    ('127.0.0.1', 8003)
]

# Index untuk round robin
current_server = 0
lock = threading.Lock()

# Fungsi untuk mendistribusikan permintaan ke server yang tersedia
def forward_to_server(client_conn, client_addr):
    global current_server
    lock.acquire()

    # Pilih server berikutnya berdasarkan round-robin
    server_host, server_port = servers[current_server]
    current_server = (current_server + 1) % len(servers)

    lock.release()

    # Buat koneksi ke server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        try:
            server_socket.connect((server_host, server_port))
            print(f"Forwarding client {client_addr} to server {server_host}:{server_port}")

            # Terima pesan dari client dan teruskan ke server
            message = client_conn.recv(1024)
            server_socket.sendall(message)

            # Terima respon dari server dan kirimkan kembali ke client
            response = server_socket.recv(1024)
            client_conn.sendall(response)

            confirmation = server_socket.recv(1024)
            client_conn.sendall(confirmation)

        except Exception as e:
            print(f"Failed to connect to server {server_host}:{server_port}: {e}")
    
    client_conn.close()

# Fungsi untuk menjalankan coordinator (load balancer)
def start_coordinator():
    # Konfigurasi coordinator (Load Balancer)
    coordinator_host = '127.0.0.1'
    coordinator_port = 8000

    coordinator_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    coordinator_socket.bind((coordinator_host, coordinator_port))
    coordinator_socket.listen(5)
    print(f"Coordinator is listening on {coordinator_host}:{coordinator_port}")

    while True:
        client_conn, client_addr = coordinator_socket.accept()
        print(f"Client connected from {client_addr}")
        client_thread = threading.Thread(target=forward_to_server, args=(client_conn, client_addr))
        client_thread.start()

if __name__ == "__main__":
    start_coordinator()
