import socket
import os
import mimetypes
import threading
import argparse
# import time

def handle_client(client_connection, client_address, semaphore):
    # time.sleep(1)
    try:
        request_data = client_connection.recv(
            1024).decode('utf-8', errors='ignore')
        if not request_data:
            return

        lines = request_data.split('\r\n')
        if len(lines) < 1:
            return

        first_line = lines[0]
        parts = first_line.split()
        if len(parts) < 2:
            return

        _, path = parts[0], parts[1]

        path = path.split('?')[0]

        file_path = os.path.join(os.getcwd(), path.lstrip('/'))

        if os.path.exists(file_path) and os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            
            with open(file_path, 'rb') as f:
                content = f.read()

            response_headers = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Type: {mime_type}\r\n"
                f"Content-Length: {len(content)}\r\n"
                "Connection: close\r\n"
                "\r\n"
            ).encode('utf-8')

            client_connection.sendall(response_headers + content)
            print(f"200 OK: {path} ({mime_type})")
        else:
            not_found_msg = b"<h1>404 Not Found</h1>"
            response_headers = (
                "HTTP/1.1 404 NOT FOUND\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(not_found_msg)}\r\n"
                "Connection: close\r\n"
                "\r\n"
            ).encode('utf-8')
            client_connection.sendall(response_headers + not_found_msg)
            print(f"404 Not Found: {path}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_connection.close()
        semaphore.release()


def run_server(host='127.0.0.1', port=8080):
    parser = argparse.ArgumentParser()
    parser.add_argument("concurrency_level", type=int)
    
    args = parser.parse_args()
    
    semaphore = threading.Semaphore(args.concurrency_level)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    while True:
        client_connection, client_address = server_socket.accept()
        
        semaphore.acquire()
        client_thread = threading.Thread(
            target=handle_client,
            args=(client_connection, client_address, semaphore)
        )
        
        client_thread.start()
        

if __name__ == "__main__":
    run_server()
