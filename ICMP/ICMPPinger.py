#!usr/bin/env python
# -*- coding: utf-8 -*-

# Usage: sudo python [files]
#
# A Ping application using ICMP request and reply messages
#
# Author: yatbear <sapphirejyt@gmail.com>
#         2016-04-11

import socket
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8

def checksum(str):
    csum = 0
    countTo = (len(str) / 2) * 2
    count = 0
    while count < countTo:
        thisVal = ord(str[count+1]) * 256 + ord(str[count])
        csum = csum + thisVal
        csum = csum & 0xffffffffL
        count = count + 2
    if countTo < len(str):
        csum = csum + ord(str[len(str) - 1])
        csum = csum & 0xffffffffL
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    RTTs = list()
    loss_num = 0
    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout
            return 'Request timed out.'
        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)
        # Fetch the ICMP header (8 bytes) from the IP packet
        header = recPacket[20:28] # The first 20 bytes is the IP header
        data = recPacket[28:]
        # Fetch useful information
        type, code, checksum, id, sequence = struct.unpack('bbHHh', header)   
        
        # Handle type 3 error 
        def handleType3(code):
            return {
                0:  'Destination Net Unreachable',
                1:  'Destination Host Unreachable',
                2:  'Protocol Unreachable',
                3:  'Port Unreachable',
                4:  'Fragmentation Needed and Don\'t Fragment was Set',
                5:  'Source Route Failed',
                6:  'Destination Network Unknown',
                7:  'Destination Host Unknown',
                8:  'Source Host Isolated',
                9:  'Communication with Destination Network is Administratively Prohibited',
                10: 'Communication with Destination Host is Administratively Prohibited',
                11: 'Destination Network Unreachable for Type of Service',
                12: 'Destination Host Unreachable for Type of Service',
                13: 'Communication Administratively Prohibited',
                14: 'Host Precedence Violation',
                15: 'Precedence cutoff in effect'
            }[code]
            
        if type == 3:
            errMsg = handleType3(code)
            print errMsg
            
        timeSent = struct.unpack('d', data)[0]
        if id == ID:
             return timeReceived - timeSent
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return 'Request timed out.'

def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0
    # Make a dummy header with a 0 checksum.
    # struct -- Interpret strings as packed binary data
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack('d', time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)
    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        myChecksum = socket.htons(myChecksum) & 0xffff
        # Convert 16-bit integers from host to network byte order.
    else:
        myChecksum = socket.htons(myChecksum)
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object

def doOnePing(destAddr, timeout):
    icmp = socket.getprotobyname('icmp') 
    # Create Socket here
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    myID = os.getpid() & 0xFFFF  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay
    
def ping(host, timeout=1, NPINGS=10):
    '''
    Args:
        timeout: number of seconds client waits for server's pong
        NPINGS: number of pings client sends to the server per ping round
    '''
    n_loss = 0
    RTTs = list()
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    dest = socket.gethostbyname(host)
    print 'Pinging ' + dest + ' (' + host + ') using Python:'
    # Send ping requests to a server separated by approximately one second
    for i in range(NPINGS):
        delay = doOnePing(dest, timeout)        
        # print delay
        if delay == 'Request timed out.':
            n_loss += 1
        else:
            RTTs.append(delay)
        time.sleep(1) # one second
    
    [minRTT, maxRTT, avgRTT] = [min(RTTs), max(RTTs), sum(RTTs) / len(RTTs)] \
                                if RTTs else ['N/A'] * 3
    loss_rate = 100.0 * n_loss / NPINGS
    print 'minimum RTT:', minRTT
    print 'maximum RTT:', maxRTT
    print 'average RTT:', avgRTT
    print 'Packet loss rate is ' + str('%.2f' % loss_rate) + '%.'

if __name__ == '__main__':
    # host = 'www.australia.gov.au'
    # host = 'www.inria.fr'
    # host = 'www.korea.net'
    host = 'www.jhu.edu'
    ping(host)