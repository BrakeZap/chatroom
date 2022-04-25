import select, socket, _thread

new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
new_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host_name = socket.gethostname()
s_ip = socket.gethostbyname(host_name)

port = 8080

new_socket.bind((host_name, port))
print("Binding successful!")

new_socket.listen(10)

list_of_clients = []


def clientThread(connection, address):
    while True:
        try:
            message = connection.recv(2048)
            if message:

                # Prints message in current room to console
                print(f"{address[0]} > {message}")

                broadcast(message, connection)

            else:
                """message may have no content if the connection
                is broken, in this case we remove the connection"""
                remove(connection)

        except socket.error:
            continue


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
