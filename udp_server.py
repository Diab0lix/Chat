import socket
import sys


class Server:
    def __init__(self, port=8888, host=''):
        
        self._host = host
        self._port = port
        self._clients = []
        self._addr = ''
        self._pseudo = ''

        # UDP socket
        try :
            self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print('Socket created')
        except (socket.error, msg):
            print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()


        # Bind socket to local host and port
        self._s.bind((self._host, self._port))

        print('Socket bind complete')
        print('listening on ' + self._host + ':' + str(self._port))

    def run(self):
        # now keep talking with the client
        while True:
            # receive data from client (data, addr)
            d = self._s.recvfrom(1024)
            data = d[0]
            self._addr = d[1]

            # don't continue if we didn't receive anything
            if not data:
                break

            err_msg = 'Commande inconnue, écrivez /join pour vous ajouter à la liste des clients disponibles ou /clients pour consulter cette liste.\n'
            
            
            if data.decode() == '/join':
                if self._pseudo == '':
                    self._s.sendto('Veuillez définir vortre pseudo avec /pseudo <nom> avant de rejoindre le serveur'.encode(), self._addr)
                else:
                    self._join()
            elif data.decode() == '/clients':
                message = str(self._clients) + '\n'
                self._s.sendto(message.encode(), self._addr)
            elif '/pseudo' in data.decode():
                try:
                    self._pseudo = data.decode().split()[1]
                except:
                    self._s.sendto('Veuillez définir vortre pseudo avec /pseudo <nom>.'.encode(), self._addr)
                confirm = 'Votre pseudo, ' + self._pseudo + ', a bien été enregistré.'
                self._s.sendto(confirm.encode(), self._addr)
            else:
                self._s.sendto(err_msg.encode(), self._addr)

            # log all messages
            print('Message[' + self._addr[0] + ':' + str(self._addr[1]) + '] - ' + data.decode().strip())

    def _join(self):
        if self._pseudo in self._clients:
            reply = 'Vous êtes déjà dans la liste des clients disponibles\nÉcrivez /clients pour voir la liste des clients disponibles\n' 
        else:
            self._clients.append(self._pseudo)
            reply = 'Vous avez été ajouté à la liste des clients disponibles\nÉcrivez /clients pour voir la liste des clients disponibles\n'

        self._s.sendto(reply.encode(), self._addr)


if __name__ == '__main__':
    if len(sys.argv) > 1 and type(sys.argv[1]):
        try:
            Server(int(sys.argv[1])).run()
        except:
            print('Please enter a port number')
    else: 
        Server().run()
