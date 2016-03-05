#!usr/bin/env python
# -*- coding: utf-8 -*-

# Usage: python [files]
#
# Pinger Client
#
# Author: yatbear <sapphirejyt@gmail.com>
#         2016-02-17

from socket import *
import time

LOCAL_HOST = '127.0.0.1'
PORT_NUMBER = 12000
TIMEOUT = 1 

# Create a UDP socket
socketClient = socket(AF_INET, SOCK_DGRAM)
# Set the timeout value on a datagram socket
socketClient.settimeout(TIMEOUT)

sequence_number = 0
lost = 10.0 
RTTs = list()

for sequence_number in range(1, 10):
    tic = time.clock()
    try:
        # Try to ping the server
        message = 'PING ' + str(sequence_number) + ' ' + time.ctime()
        socketClient.sendto(message, (LOCAL_HOST, PORT_NUMBER))
        # Look for response
        while True:
            message = socketClient.recv(1024)
            print message
            toc = time.clock()
            RTT = toc - tic
            RTTs.append(RTT)
            lost -= 1
            print 'RTT = %f seconds' % RTT
    except:
         print 'Request timed out'
         
[minRTT, maxRTT, avgRTT] = [min(RTTs), max(RTTs), sum(RTTs) / len(RTTs)] \
                            if RTTs else [0] * 3
loss_rate = 100 * lost / 10.0

print '\nThe minimum, maximum, and average RTTs are %fs, %fs, %fs.' \
        % (minRTT, maxRTT, avgRTT)
print 'Packet loss rate is ' + str('%.2f' % loss_rate) + '%.'
        