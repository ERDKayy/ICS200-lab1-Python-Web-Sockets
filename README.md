# ICS200-lab1
Web-socket programming in python

Simple python UDP client and server.

Client:
    Takes commandline arguments formatted as followed.

    #python client.python PORT# OPERATOR INT, INT, INT, ... etc

Port: The port number your client and server will be using.
Operator: +, -, and '*' ( * must have parentheses)
INT: 0-15, maximum 10 values.

Client packs arguments as pairs of 4bit integers into a byte array to be sent to the server.

Server:
    Takes a single command line argument.

    #python server.py PORT#

Server stays open waiting to receive data from the client. Then it will unpack arguments using masks and perform specified operator on each integer in sequence. Returns the sum as a 4bit integer to the client.


    