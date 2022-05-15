import sys
import threading
import json
import socket

new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
new_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = 8080

new_socket.bind(("192.168.1.15", port))
print("Binding successful!")

new_socket.listen(10)

list_of_clients = []


class ClientThread:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, connection, clientAddr):
        while self._running:
            try:
                originalData = connection.recv(2048, socket.MSG_PEEK)
                if originalData.decode() == "123":
                    dataSize = sys.getsizeof(originalData)
                    connection.recv(dataSize)
                    connection.send(str(len(list_of_clients)).encode())
                    continue
                originalData = connection.recv(2048)
                if originalData:
                    data = json.loads(originalData.decode())
                    if data:
                        message = data.get("message")
                        # Prints message in current room to console
                        print(f"{clientAddr} > {message}")

                        broadcast(originalData, connection)

                    else:
                        remove(connection)

            except socket.error:
                remove(connection)


def broadcast(message, connection):
    for clients in list_of_clients:
        if clients[0] != connection:
            try:
                clients[0].send(message)
            except socket.error:
                clients[0].close()
                remove(clients)


# Maybe a better way to implement this
def remove(connection):
    index = 0
    for con, thread, currAddr in list_of_clients:
        if conn == connection or thread == connection or currAddr == connection:
            print(f"Removing client: {currAddr}")
            formatStr = f"{currAddr} left."
            broadcast(formatStr.encode(), conn)
            list_of_clients.pop(index)
            thread.terminate()
        index += 1


while True:
    # Waits for a new connection to the server

    conn, addr = new_socket.accept()
    addr = addr[0]

    # Checks if the connection is already connected to the server. If so, remove it.
    for obj in list_of_clients:
        address = obj[2]
        if addr == address:
            remove(address)

    # prints the address of the user that just connected to console
    print(addr + " connected")
    broadcast(f"{addr} connected.".encode(), conn)
    # creates and individual thread for every user that connects
    # Adds the connection, thread, and address to the list of clients

    ct = ClientThread()
    currThread = threading.Thread(target=ct.run, args=(conn, addr))
    currThread.start()
    list_of_clients.append((conn, ct, addr))

conn.close()
new_socket.close()
