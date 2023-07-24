import socket

def startServer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(('localhost', 12345))
        server.listen(1)
        client, address = server.accept()
        with client:
            print(f"Connected by {address}")
            while True:
                data = client.recv(1024)
                if not data:
                    break
                message = data
                client.send(b"Recieved: " + message)

startServer()

            