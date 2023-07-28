import socket
import threading

client_sockets = []

try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost',19855))
    server_socket.listen(2)

    print("Server is ready to accept connections...")

    def handle_client_connection(client_socket, client_address):
        print(f"New connection from {client_address}")
        try:
            while True:
                message = client_socket.recv(1024)
                client_socket.send(b"++\n")
                if not message:
                    break
                print(f"Received message from {client_address}")
                print(f"Received: {str(message.decode('utf-8'))}")
                for client in client_sockets:
                    if client[0] != client_socket:
                        client[0].send(f"{str(message.decode('utf-8'))}".encode('utf-8'))

            print(f"Connection from {client_address} closed.")
            client_socket.close()
            client_sockets.pop(client_sockets.index((client_socket, client_address)))
        except Exception as e:
            print(f"An error occured: {e}")
        finally:
            client_socket.close()

    while True:
        client_socket, client_address = server_socket.accept()
        client_sockets.append((client_socket, client_address))
        client_thread = threading.Thread(target=handle_client_connection, args=(client_socket, client_address))
        client_thread.start()

except Exception as e:
    print(f"An error occured: {e}")

finally:
    for client_socket, _ in client_sockets:
        client_socket.close()
    server_socket.close()

            