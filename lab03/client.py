import socket
import argparse
import sys

def start_client():
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("port", type=int)
    parser.add_argument("filename")

    args = parser.parse_args()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((args.host, args.port))

        resource = args.filename if args.filename.startswith('/') else '/' + args.filename
        
        request = (
            f"GET {resource} HTTP/1.1\r\n"
            f"Host: {args.host}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
    
        client_socket.sendall(request.encode('utf-8'))

        response = b""
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            response += chunk
            
        print(response.decode('utf-8'))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()