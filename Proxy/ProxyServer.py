#!usr/bin/env python
# -*- coding: utf-8 -*-

# Usage: 1. python ProxyServer.py server_ip 
#           (e.g. python ProxyServer.py localhost)
#        2. open http://[server_ip]:[server_port]/[website] in your browser
#           (e.g. http://localhost:8888/www.tutorialspoint.com)
#
# A small web proxy server which is able to cache web pages
#
# Author: yatbear <sapphirejyt@gmail.com>
#         2016-03-05

from socket import *
import sys

if len(sys.argv) <= 1:
    print 'Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server]'
    sys.exit(2)
    
DEST_IP = sys.argv[1]
PORT = 8888
    
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((DEST_IP, PORT))
tcpSerSock.listen(5)

while 1:
    # Start receiving data from the client
    print 'Ready to serve...'
    tcpCliSock, addr = tcpSerSock.accept()
    print 'Received a connection from:', addr
    message = tcpCliSock.recv(1024)    
    if not message:
        tcpCliSock.close()
        continue
    print message 
    # Extract the filename from the given message
    print message.split()[1]
    filename = message.split()[1].partition('/')[2]
    print filename
    fileExist = False
    filetouse =  '/' + filename
    print filetouse
    try:
        # Check wether the file exist in the cache
        f = open(filetouse[1:], 'r')
        outputdata = f.readlines()
        fileExist = True
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send('HTTP/1.0 200 OK\r\n')
        tcpCliSock.send('Content-Type:text/html\r\n')
        for i in range(len(outputdata)):
            tcpCliSock.send(outputdata[i])
        print 'Read from cache'
    # Error handling for file not found in cache
    except IOError:
        if fileExist == False:
            # Create a socket on the proxyserver 
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace('www.', '', 1)
            print hostn
            try:
                # Connect to the socket to port 80
                c.connect((hostn, 80))
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('r', 0)
                fileobj.write('GET http://' + hostn + ' HTTP/1.0\n\n')
                # Read the response into buffer
                buffer = fileobj.readlines()
                # Create a new file in the cache for the requested file
                tmpFile = open('./' + filename, 'wb')
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                for i in range(len(buffer)):
                    tcpCliSock.send(buffer[i])
                    tmpFile.write(buffer[i])
                tmpFile.close()
            except:
                print 'Illegal request'   
        else:
            # HTTP response message for file not found 
            print 'HTTP 404 - File Not Found'
    # Close the client socket
    tcpCliSock.close()
# Close the server socket
tcpSerSock.close()
