import _thread
import json
import socket

new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
new_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host_name = socket.gethostname()
print(f"host name is : {host_name}")

port = 8080

new_socket.bind(("192.168.1.15", port))
print("Binding successful!")

new_socket.listen(10)

list_of_clients = []


def clientThread(connection, address):
    while True:
        try:
            data = connection.recv(2048)
            data = json.loads(data.decode())
            if data:
                message = data.get("message")
                # Prints message in current room to console
                print(f"{address[0]} > {message}")

                broadcast(data, connection)

            else:
                """message may have no content if the connection
                is broken, in this case we remove the connection"""
                remove(connection)
                _thread.exit()

        except socket.error:
            remove(connection)
            _thread.exit()


def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message)
            except socket.error:
                clients.close()
                remove(clients)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    """Accepts a connection request and stores two parameters,
    conn which is a socket object for that user, and addr
    which contains the IP address of the client that just
    connected"""
    conn, addr = new_socket.accept()

    """Maintains a list of clients for ease of broadcasting
    a message to all available people in the chatroom"""
    list_of_clients.append(conn)

    # prints the address of the user that just connected to console
    print(addr[0] + " connected")

    # creates and individual thread for every user
    # that connects
    _thread.start_new_thread(clientThread, (conn, addr))




conn.close()
new_socket.close()
