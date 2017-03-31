#!/usr/bin/env python3
# echo.py
# author: Sebastien Combefis
# Modified by: Thierry Frycia & Mohamad Mroue
# version: March 30, 2017

import socket
import sys

SERVERADDRESS = (socket.gethostname(), 6000)
Clientlist=[]

class EchoServer():
    def __init__(self):
        self.__s = socket.socket()
        self.__s.bind(SERVERADDRESS)
        print('You can now launch the chat script.')        

    def run(self):
        self.__s.listen(0)
        while True:
            client, addr = self.__s.accept()
            try:
                user = self._receive(client).decode().rstrip()
                if ":list:" in user:
                    ADDRESS = user.rsplit(':')[2]
                    self._send(ADDRESS)
                if user not in Clientlist and ":list:" not in user :
                     Clientlist.append(user)
                client.close()
            except OSError:
                print('Error while receiving message.')

    def _receive(self, client):
        chunks = []
        finished = False
        while not finished:
            data = client.recv(1024)
            chunks.append(data)
            finished = data == b''
        return b''.join(chunks)

    def _send(self, address):
        totalsent = 0
        if len(Clientlist)==0:
            msg = '0 User Online.'
        else:
            msg = 'Online Users:\n'
        for i in Clientlist:
            msg += i + '\n'

        t=socket.socket(type=socket.SOCK_DGRAM)
        t.bind(SERVERADDRESS)
        
        n=address[1:][:-1]
        Ip=n.split(',')[0][1:][:-1]
        Port=int(n.split(',')[1])
        try:
            while totalsent < len(msg):
                sent = t.sendto(msg[totalsent:].encode(), (Ip, Port))
                totalsent += sent
            t.close()
        except OSError:
            print('Error while sending message.')
            t.close()

EchoServer().run()
