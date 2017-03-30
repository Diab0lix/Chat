# chat.py

## Quick start

To run the server, just launch:

    > ./python echo.py

You can then launch the chat script by default ('localhost', port=5000):

    > ./python chat.py

Choose a username with "/pseudo". Example:

    > ./pseudo Cmb.

Use method /list to get the list of online users (to use on defalt chat script).

    > ./list
	
You can now run different terminal to be able to chat with 2 or more. Example:

    > ./python chat.py 0.0.0.0 5001

Use method /join to connect to another user. Example:

    > ./join localhost 5001

In case of problem use /help.

The communication protocol used between the server and the client is TCP,
adequate for communication between server and client.

Features of the Transmission Control Protocol:
Reliable transfer (receipt and guaranteed order),
With connection (heavy protocol),
Adapted to client/server architecture.

The communication protocol used between different user is UDP,
adequate for communication between computer especially locally.

Characteristics of the User Datagram Protocol:
Unreliable transfer (receipt and order not guaranteed),
Without connection (lightweight protocol),
Suitable for peer-to-peer architecture.

## Contributors

- Mohamad Mroue
- Thierry Frycia

Tested on Windows and Mac OS
