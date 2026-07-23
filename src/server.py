import socket

HOST="0.0.0.0"
PORT=2009
KEY="parola"

def xor_tranform(data:bytes, key:str) -> bytes:
    key_bytes = key.encode("utf-8")
    return bytes(byte ^ key_bytes[i % len(key_bytes)] for i, byte in enumerate(data))

def encrypt(text:str, key:str) -> bytes:
    return xor_tranform(text.encode("utf-8"), key)

def decrypt(data:bytes, key:str) -> str:
    return xor_tranform(data, key).decode("utf-8")

def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST,PORT))
        server_socket.listen(1)
        print(f"Server is listening on {HOST}:{PORT}")

        conn, addr = server_socket.accept()
        # to do c++ swap() in python you can do a,b=b,a

        with conn:
            print(f"Connection from {addr}")
            encrypted_data = conn.recv(4096)
            message = decrypt(encrypted_data, KEY)

            print(f"Received from client: {message}")

            response = f"Echo: {message}"
            conn.sendall(encrypt(response, KEY))

            print("Sent encrypted message!")

if __name__ == "__main__":
    main()