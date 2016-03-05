#!usr/bin/env python
# -*- coding: utf-8 -*-

# Usage: python server.py
#
# Web Server
#
# Author: yatbear <sapphirejyt@gmail.com>
#         2016-02-04

import os
from socket import *

# Create an INET, STREAMing socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverSocket.bind(('127.0.0.1', 6789)) 
serverSocket.listen(5)

while True:
    # Establish the connection
    print 'Ready to serve...'
    connectionSocket, addr = serverSocket.accept()   
    
    try:
        message = connectionSocket.recv(128)
        print message

        filename = message.split()[1]
        f = open(os.getcwd() + '/' + filename)
        outputdata = f.read()
        
        # Send one HTTP header line into socket
        connectionSocket.send('HTTP/1.1 200 OK\nContent-Type: text/html\n\n')
        
        # Send the content of the requested file to the client
        for i in range(len(outputdata)):
            connectionSocket.send(outputdata[i])     
        connectionSocket.close()
   
    except IOError:
        # Send response messsage for file not found
        connectionSocket.send('404 Not Found')
        # Close client socket
        connectionSocket.close()

serverSocket.close()
