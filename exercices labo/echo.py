#!/usr/bin/env python3
# echo.py
# author: Sébastien Combéfis
# version: February 15, 2016

import socket
import sys
import struct

class EchoServer:
    def __init__(self, host=socket.gethostname(), port=6000):
        self.__s = socket.socket()
        self.__s.bind((host, port))
        self.__clients = []
        self.__host = host
        self.__port = port

    def run(self):
        handlers = {
            '/join': self._join,
            '/client': self._client
        }
        self.__s.listen()
        print("Serveur à l'écoute sur {}:{}".format(self.__host, self.__port))
        while True:
            client, addr = self.__s.accept()
            #try:
            message = self._receive(client).decode()
            if message in handlers:
                handlers[message]()
            print(message)
            #client.close()
            #except OSError:
                #print('Erreur lors de la réception du message.')
    
    def _join(self):
        self.__clients.append(self.__host)
        self.__s.sendto('Vous avez rejoint le serveur'.encode(), (self.__host, self.__port))

    def _client(self):
        print(self.__clients)
        self.__s.sendto(self.__clients.encode(), (self.__host, self.__port))
        self.__s.close()

    def _receive(self, client):
        chunks = []
        finished = False
        while not finished:
            data = client.recv(1024)
            chunks.append(data)
            finished = data == b''
        return b''.join(chunks)


class EchoClient:
    def __init__(self, message, host=socket.gethostname(), port=8888):
        self.__message = message
        self.__s = socket.socket()
        self.__host = host
        self.__port = port
    
    def run(self):
        try:
            self.__s.connect((self.__host, self.__port))
            self._send()
            self.__s.close()
        except OSError:
            print('Serveur introuvable, connexion impossible.')
    
    def _send(self):
        totalsent = 0
        msg = self.__message
        try:
            while totalsent < len(msg):
                sent = self.__s.send(msg[totalsent:])
                totalsent += sent
        except OSError:
            print("Erreur lors de l'envoi du message.")

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'server':
        EchoServer().run()
    elif len(sys.argv) == 3 and sys.argv[1] == 'client':
        EchoClient(sys.argv[2].encode()).run()
