import socket
import time
import logging

# Konfigurasi logging untuk mencatat ke file dan juga print di layar
logger = logging.getLogger('client_logger')
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    file_handler = logging.FileHandler('client_log.log')
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Konfigurasi client
SERVER_HOST = '127.0.0.1'  # IP server
SERVER_PORT = 8000         # Port yang digunakan server

# Fungsi client untuk mengirim dan menerima pesan
def client_send_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, SERVER_PORT))

        # Kirim pesan ke server
        send_time = time.time()
        s.sendall(message.encode())
        logger.info(f"Message sent: {message}, send time: {send_time}")

        # Terima balasan dari server
        response = s.recv(1024).decode()
        logger.info(f"Received response: {response}")

        # Terima konfirmasi bahwa pesan diterima
        confirmation = s.recv(1024).decode()
        logger.info(f"Received confirmation: {confirmation}")

        receive_time = time.time()
        round_trip_time = receive_time - send_time

        logger.info(f"Total round-trip time: {round_trip_time:.4f} seconds")

if __name__ == "__main__":
    while True:
        user_input = input("Enter message to send to server: ")
        client_send_message(user_input)
