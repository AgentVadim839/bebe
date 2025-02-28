import os
from socket import *

server_socket = socket(AF_INET, SOCK_STREAM)
port = int(os.environ.get('PORT', 12345))
server_socket.bind(('0.0.0.0', port))

server_socket.listen(5)
server_socket.setblocking(0)

clients = []
print("Server started.")
while True:
    try:
        connection, address = server_socket.accept()
        connection.setblocking(0)
        name_client = connection.recv(1024).decode().strip()
        print(f"{name_client} подключился за {address}")
        if name_client:
            connection.send(f'Вітаю {name_client} в консольному чаті!'.encode())
            clients.append([connection, name_client])
    except:
        pass

    for client in clients[:]:
        try:
            message = client[0].recv(1024).decode().strip()
            for c in clients:
                if client != c:
                    c[0].send(f'{client[1]}: {message}'.encode())
                    print(f'{client[1]}: {message}')
        except BlockingIOError:
            pass
        except:
            print(f'Клієнт {client[1]} відключився.')
            client[0].close()
            clients.remove(client)
