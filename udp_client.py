import socket   #for sockets
import sys      #for exit

class Client:
    def __init__(self, port=8888, host='localhost'):
        
        self._host = host
        self._port = port

        # UDP socket
        try:
                self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
                print('Failed to create socket')
                sys.exit()

    def run(self):
        while True:
            msg = input().encode()
                
            #Set the whole string
            self._s.sendto(msg, (self._host, self._port))
                    
            # receive data from client (data, addr)
            d = self._s.recvfrom(1024)
            reply = d[0]
            addr = d[1]
                    
            print(reply.decode())

if __name__ == '__main__':
    if len(sys.argv) > 1 and type(sys.argv[1]):
        try:
            Client(int(sys.argv[1])).run()
        except:
            print('Please enter a port number')
    else: 
        Client().run()

