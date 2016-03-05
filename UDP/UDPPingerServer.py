#!usr/bin/env python
# -*- coding: utf-8 -*-

# Usage: python [files]
#
# Pinger Server
#
# Author: yatbear <sapphirejyt@gmail.com>
#         2016-02-17

import random # to generate randomized lost packets
from socket import *

LOCAL_HOST = '127.0.0.1'
PORT_NUMBER = 12000

# Create a UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM) # SOCK_DGRAM for UDP packets
# Assign IP address and port number to socket
serverSocket.bind((LOCAL_HOST, PORT_NUMBER))

while True:
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)
    # Receive client packet along with the address it is coming from 
    message, address = serverSocket.recvfrom(1024)
    # Capitalize the message from the client
    message = message.upper()
    # If rand is less than 4, consider the packet lost do not respond
    if rand < 4:
        continue
    # Otherwise, the server responds
    serverSocket.sendto(message, address)
    