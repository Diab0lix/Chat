import socket

s = socket.socket()
s.connect(('www.vinci.be', 80))
data = "GET /shit HTTP/1.0\n\n".encode()
sent = s.send(data)
response = s.recv(512).decode()
print(response)
