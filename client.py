'''
Created on Mar 20, 2013

@author: bpudream
'''
import socket
import threading
from random import getrandbits
import random, base64
import string
import signal
import sys

class Sender(threading.Thread):

    def __init__(self,socket,secret):
        
        threading.Thread.__init__(self)
        self.sender = socket
        self.secret = secret
        #self.data = message
  
    def run(self):              
        while 1:
            message = raw_input()
            secretMessage = encrypt(message,str(self.secret))
            self.sender.sendall(secretMessage)

class Receiver(threading.Thread):

    def __init__(self,socket,name,secret):
        
        threading.Thread.__init__(self)
        self.receiver = socket
        self.friendName = name
        self.secret = secret
        #self.data = message
  
    def run(self):      
        while 1:
            secretMessage = self.receiver.recv(4096)
            message = decrypt(secretMessage,str(self.secret))
            print '\n' + self.friendName +": " + message
            
def signal_handler(signal, frame):
    print 'intrrupt!'
    clientSocket.close()
    sys.exit(0)
    
class Client:
    def __init__(self):
        self.host = raw_input("input host IP:")
        self.port = input("input port number:")
        #self.host = '127.0.0.1'
        #self.port = 19527
        # generate g & prime
        self.g = 2
        self.prime = 17
        bits = 32
        self.a = getrandbits(bits)
        self.A = pow(self.g, self.a, self.prime)

    def start(self):
        #connecting
        clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        address = (self.host,self.port)
        clientSocket.connect(address)
        
        #receive connection information
        connectInfo1 = clientSocket.recv(4096)
        myid = string.atol(clientSocket.recv(4096))
        print connectInfo1
        print "your id is: ",myid
        
        # exchange name
        myname = raw_input("input your name: ")
        print "waiting for your friend's name..."
        clientSocket.sendall(myname)
        friendName = clientSocket.recv(4096)
        print "Conversation started. You are talking to ",friendName
        #while 1:
        #    message = raw_input("["+name+"]: ")
        #    clientSocket.sendall(message)
        #    recvMessage = clientSocket.recv(4096)
        #    print recvMessage
        #clientSocket.close()
        
        # Deffie-Hellman exchange
        if myid == 1:
            clientSocket.sendall(str(self.A))
            B = string.atol(clientSocket.recv(4096))
            secret = pow(B, self.a, self.prime)
        else:
            B = string.atol(clientSocket.recv(4096))
            secret = pow(B, self.a, self.prime)
            clientSocket.sendall(str(self.A))
        
        # create two threads for sending and receiving
        print '\n'
        sender = Sender(clientSocket,secret)
        recver = Receiver(clientSocket,friendName,secret)
        sender.start()
        recver.start()
                
# RC4
__all__ = ['crypt', 'encrypt', 'decrypt']
def crypt(data, key):
    """RC4 algorithm"""
    x = 0
    box = range(256)
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    x = y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))

    return ''.join(out)

def encrypt(data, key, encode=base64.standard_b64encode, salt_length=8):
    """RC4 encryption with random salt and final encoding"""
    salt = ''
    for n in range(salt_length):
        salt += chr(random.randrange(256))
    data = salt + crypt(data, key + salt)
    if encode:
        data = encode(data)
    return data

def decrypt(data, key, decode=base64.standard_b64decode, salt_length=8):
    """RC4 decryption of encoded data"""
    if decode:
        data = decode(data)
    salt = data[:salt_length]
    return crypt(data[salt_length:], key + salt)

if __name__ == '__main__':
    client = Client()
    signal.signal(signal.SIGINT, signal_handler)
    client.start()
