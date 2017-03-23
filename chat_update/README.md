## Quick start

To run the server, just launch:

    > ./echo.py

You can then launch the chat script by default (localhost, port=5000):

    > ./chat.py

You can now run different terminal to be able to chat with 2 or more example:

    > ./chat.py 0.0.0.0 5001

Choose a username with "/pseudo" example:
/pseudo Cmb.

Use method /list to get the list of online users (to use on defalt chat script).
Use method /join to connect to another user example:
/join 0.0.0.0 5001

In case of problem use /help.

The communication protocol to use between the server and the client is TCP,
Adequate for communication between server and client.

Features of the Transmission Control Protocol:
Reliable transfer (receipt and guaranteed order),
With connection (heavy protocol),
Adapted to client/server architecture.

The communication protocol used between user and user is UDP adequate for communication between computer especially locally:
Characteristics of the User Datagram Protocol:
Unreliable transfer (receipt and order not guaranteed),
Without connection (lightweight protocol),
Suitable for peer-to-peer architecture.

## Contributors

- Mohamad Mroue
- Thierry Frycia
