import socket
import sys

HOST = ''    # Symbolic name meaning all available interfaces
PORT = 8888    # Arbitrary non-privileged port

# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Socket created')
except (socket.error, msg):
    print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()


# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except (socket.error, msg):
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print('Socket bind complete')


clients = []

def join():
    if addr in clients:
        reply = 'Vous êtes déjà dans la liste des clients disponibles\n' 
    else:
        clients.append(addr)
        reply = 'Vous avez été ajouté à la liste des clients disponibles\n'

    s.sendto(reply.encode(), addr)
    s.sendto('Écrivez /clients pour voir la liste des clients disponibles\n'.encode(), addr)

# now keep talking with the client
while True:
    # receive data from client (data, addr)
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]

    # don't continue if we didn't receive anything
    if not data:
        break

    err_msg = 'Commande inconnue, écrivez /join pour vous ajouter à la liste des clients disponibles ou /clients pour consulter cette liste.\n'
    
    
    if data.decode() == '/join\n':
        join()
    elif data.decode() == '/clients\n':
        s.sendto(str(clients).encode(), addr)
        s.sendto('\n'.encode(), addr)
    else:
        s.sendto(err_msg.encode(), addr)

    # log all messages
    print('Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.decode().strip())

#s.close()
