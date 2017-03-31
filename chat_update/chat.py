#!/usr/bin/env python3
# chat.py
# author: Sebastien Combefis
# Modified by: Thierry Frycia & Mohamad Mroue
# version: March 31, 2017

import socket
import sys
import threading
import time

SERVERADDRESS = (socket.gethostname(), 6000)
s = socket.socket(type=socket.SOCK_DGRAM)
username=''

class Chat():
    def __init__(self, host=socket.gethostname(), port=5000):
        try:
            s.settimeout(0.5)
            s.bind((host, port))
            self.__s = s
            print('Listening on {}:{}'.format(host, port))
            print('''Use "/pseudo" to choose a pseudonym.
Use "/help" for help.''')
        except OSError:
            print('Please choose another Port or IP address.')
            quit()
        except:
            print('Please choose another Port or IP address.')
            quit()

    def run(self):
        handlers = {
            '/exit': self._exit,
            '/quit': self._quit,
            '/join': self._join,
            '/send': self._send,
            '/pseudo': self._pseudo,
            '/list':self._list,
            '/help': self._help
        }
        self.__running = True
        self.__address = None
        threading.Thread(target=self._receive).start()
        while self.__running:
            line = sys.stdin.readline().rstrip() + ' '
            # Extract the command and the param
            command = line[:line.index(' ')]
            param = line[line.index(' ')+1:].rstrip()
            # Call the command handler
            if command in handlers:
                try:
                    handlers[command]() if param == '' else handlers[command](param)
                except:
                    print("Error while command execution.")
            else:
                print('Unknown Command:', command)

    def _exit(self):
        self._connection("{} leaved the port.".format(username))
        try:
            EchoClient((": delete :"+str(username)+str(s.getsockname())).encode()).run()
        except:
            pass
        self.__running = False
        self.__address = None
        self.__s.close()
        
    def _quit(self):
        self._connection("{} leaved the port.".format(username))
        self.__address = None
        try:
            EchoClient((": delete :"+str(username)+str(s.getsockname())).encode()).run()
        except:
            pass

    def _join(self, param):
        if username=='':
            print('Error while joining, please use "/pseudo" to choose a username.')
        else:
            tokens = param.split(' ')
            if len(tokens) == 2:
                try:
                    self.__address = (socket.gethostbyaddr(tokens[0])[0], int(tokens[1]))
                    print('Connected to {}:{}'.format(*self.__address))
                    self._connection("{} joined the port.".format(username))
                except OSError:
                    print("Error during command execution.")
            else:
                print('''Error during command execution.
Please type Port and Ip address. Example: /join localhost 5001''')
                
    def _connection(self, param):
        if self.__address is not None:
            try:
                message = param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__address)
                    totalsent += sent
            except OSError:
                print('Error during command execution.')

    def _send(self, param):
        if self.__address is not None:
            try:
                if username=='':
                    print('Error while sending, please use "/pseudo" to choose a username.')
                else:
                    param = username + " : " + param
                    message = param.encode()
                    totalsent = 0
                    print(self.__address)
                    while totalsent < len(message):
                        sent = self.__s.sendto(message[totalsent:], self.__address)
                        totalsent += sent
                    print("Message sent.")
            except OSError:
                print('Error during command execution.')
        else:
            print("No port joined yet.")

    def _receive(self):
        while self.__running:
            try:
                data, address = self.__s.recvfrom(1024)
                localtime = time.asctime(time.localtime(time.time()))
                if data.decode()[1:4]==' : ':
                    print("{}  sent at {}.".format(data.decode(),localtime))
                else:
                    print(data.decode())
                    try:
                        n = data.decode().split(' ')
                        if n[1] =='joined':
                            EchoClient(("{}{}".format(data.decode()[:-17], address)).encode()).run()
                        if n[1] =='leaved':
                            EchoClient((": delete :{}{}".format(data.decode()[:-17], address)).encode()).run()
                    except:
                        pass
            except socket.timeout:
                pass
            except OSError:
                return

    def _pseudo(self, param):
        tokens = param.split(' ')
        if len(tokens) == 1:
            try:
                global username
                username=param
                print('Your pseudo has been saved.')
                EchoClient((str(param)+str(s.getsockname())).encode()).run()
            except:
                pass
        else:
            print('Invalid pseudo.')

    def _list(self):
        try:
            command = ": list :" + str(s.getsockname())
            EchoClient(str(command).encode()).run()
        except:
            print("Server not found, impossible to connect.")        
        
    def _help(self):
        print('''Please type:
      "/exit" to exit the chat application.
      "/quit" to quit a chatroom.
      "/join" to join a chat room.
      "/send" to send a message to members of the same chatroom.
      "/pseudo" to chose a pseudo to chat.
      "/list" to show online users.''')

class EchoClient():
    def __init__(self, message):
        self.__message = message
        self.__s = socket.socket()

    def run(self):
        self.__s.connect(SERVERADDRESS)
        self._send()
        self.__s.close()

    def _send(self):
        totalsent = 0
        msg = self.__message
        try:
            while totalsent < len(msg):
                sent = self.__s.send(msg[totalsent:])
                totalsent += sent
        except OSError:
            print("Error while sending message.")

if __name__ == '__main__':
    if len(sys.argv) == 3:
        Chat(sys.argv[1], int(sys.argv[2])).run()
    else:
        Chat().run()
