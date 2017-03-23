#!/usr/bin/env python3
# chat.py
# author: Sebastien Combefis
# Modified by: Thierry Frycia & Mohamad Mroue
# version: March 23, 2017

import socket
import sys
import threading
import time

SERVERADDRESS = (socket.gethostname(), 6000)
username=''

class Chat():
    def __init__(self, host=socket.gethostname(), port=5000):
        try:
            global s
            s = socket.socket(type=socket.SOCK_DGRAM)
            s.settimeout(0.5)
            s.bind((host, port))
            if host == 'localhost' or host == '127.0.0.1':
                print('Please choose another Port or IP address.')
                quit()
            if host!=socket.gethostname() and port==5000:
                print('Please choose another Port or IP address.')
                quit()
            self.__s = s
            print('Hearing on {}:{}'.format(host, port))
            print('Use "/help" for help.')
        except OSError:
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
                    print("Error during command execution.")
            else:
                print('Unknown Command:', command)

    def _exit(self):
        self.__running = False
        self.__address = None
        self.__s.close()

    def _quit(self):
        self.__address = None

    def _join(self, param):
        if username=='':
            print("Error while joining, please use '/pseudo' to choose a username.")
        else:
            tokens = param.split(' ')
            if len(tokens) == 2:
                try:
                    self.__address = (socket.gethostbyaddr(tokens[0])[0], int(tokens[1]))
                    print('Connected to {}:{}'.format(*self.__address))
                    self._joining(" {} joined the port.".format(username))
                except OSError:
                    print("Error during command execution.")

    def _joining(self, param):
        if self.__address is not None:
            try:
                message = param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__address)
                    totalsent += sent
            except OSError:
                print('Error during joining.')

    def _send(self, param):
        if self.__address is not None:
            try:
                if username=='':
                    print("Error while sending, please use '/pseudo' to choose a username.")
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
                if data.decode()[:13]=='Online Users:' or data.decode()=='0 User Online.':
                    print(data.decode())
                else:
                    print("{}  sent at {} from IP:{}".format(data.decode(),localtime,address))
            except socket.timeout:
                pass
            except OSError:
                return

    def _pseudo(self, param):
       try:
           global username
           username=param
           User=str(param)+str(s.getsockname())
           EchoClient(str(User).encode()).run()
       except:
           print("Error : no active server.")
        
    def _help(self):
        print('Please type:')
        print('"/exit"', 'to exit the chat application.')
        print('"/quit"', 'to quit a chatroom.')
        print('"/join"', 'to join a chat room.')
        print('"/send"', 'to send a message to members of the same chatroom.')
        print('"/pseudo"', 'to chose a pseudo to chat.')
        print('"/list"', 'to show online users.')
        
    def _list(self):
        command = ":list:" + str(s.getsockname())
        EchoClient(str(command).encode()).run()

class EchoClient():
    def __init__(self, message):
        self.__message = message
        self.__s = socket.socket()

    def run(self):
        try:
            self.__s.connect(SERVERADDRESS)
            self._send()
            self.__s.close()
        except OSError:
            print("Server not found, impossible to connect.")

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
