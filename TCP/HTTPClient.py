#!usr/bin/env python
# -*- coding: utf-8 -*-

# Usage: python client.py server_host server_port filename
#        Default: python client.py 127.0.0.1 6789 HelloWorld.html
#
# HTTP Client
#
# Author: yatbear <sapphirejyt@gmail.com>
#         2016-02-07

import sys
from socket import *

[server_host, server_port, filename] = sys.argv[1:] \
    if len(sys.argv) == 4 else ['127.0.0.1', 6789, 'HelloWorld.html']
server_port = int(server_port)

# Create a TCP/IP socket
socketClient = socket(AF_INET, SOCK_STREAM)

# Connect the socket to the port where the server is listening 
server_addr = (server_host, server_port)
socketClient.connect(server_addr)

try:
    # Send an HTTP request to the server 
    message = 'GET %s HTTP/1.1\n\n' % filename
    socketClient.sendall(message)
    data = ''

    # Look for respondse
    while True:
        message = socketClient.recv(1024)
        if len(message) == 0:
            break
        data += message

    # Display the server response as an output
    print data

finally:
    socketClient.close()
