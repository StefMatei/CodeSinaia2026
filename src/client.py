import socket

HOST="127.0.0.1"
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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST,PORT))

        message = "Hello World"
        client_socket.sendall(encrypt(message, KEY))

        print(f"Sent {message}")

        encrypted_response = client_socket.recv(4096)
        print ("DECODED message: ", decrypt(encrypted_response, KEY))

if __name__ == "__main__":
    main()