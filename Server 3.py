import socket
import threading
import time
import logging

# Konfigurasi logging untuk mencatat ke file dan juga print di layar
logger = logging.getLogger('server_logger')
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    file_handler = logging.FileHandler('server_log.log')
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Konfigurasi server
HOST = '127.0.0.1'  # Gunakan IP yang sesuai dengan jaringan
PORT = 8003         # Port yang digunakan untuk mendengarkan koneksi

# Fungsi untuk menangani koneksi dari client
def handle_client(conn, addr):
    logger.info(f"Client connected from {addr}")
    with conn:
        while True:
            try:
                # Menerima pesan dari client
                message = conn.recv(1024).decode()
                if not message:
                    break

                logger.info(f"Received message from {addr}: {message}")
                send_time = time.time()  # Waktu pengiriman pesan

                # Membalas pesan ke client
                response = f"Server received: {message}"
                conn.sendall(response.encode())

                # Mengirim pesan bahwa pesan telah diterima
                confirmation = "Message has been received."
                conn.sendall(confirmation.encode())

                receive_time = time.time()  # Waktu penerimaan balasan
                round_trip_time = receive_time - send_time

                logger.info(f"Response sent to {addr}, round-trip time: {round_trip_time:.4f} seconds")
            except Exception as e:
                logger.error(f"Error handling client {addr}: {e}")
                break

# Fungsi utama untuk menjalankan server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    logger.info(f"Server started, listening on {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()
