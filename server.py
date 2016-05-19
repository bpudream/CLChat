'''
Created on Mar 20, 2013

@author: bpudream
'''
import socket
import threading
import signal
import sys

class Server:
    def __init__(self):
        self.host = None
        self.port = None
        self.serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.backlog = 2
        
    def start(self):
        #prepare for connection
        self.host = raw_input("input host IP:")
        self.port = int(input("input port number(after 1024):"))
        #self.host = '127.0.0.1'
        #self.host = '172.17.142.161'
        #self.port = 19527
        address = (self.host,self.port)
        self.serverSocket.bind(address)
  
        self.serverSocket.listen(self.backlog)
        print "server ready"
        
        print "waiting for client1"
        clientSocket1,clientAddress1 = self.serverSocket.accept()
        print "connected by",clientAddress1        
        print "waiting for client2"
        clientSocket2,clientAddress2 = self.serverSocket.accept()     
        print "connected by",clientAddress2
        
        client1 = Client(clientSocket1,clientSocket2)
        client1.start()
        client2 = Client(clientSocket2,clientSocket1)
        client2.start()

        #print clientSocket1.recv(4096)
        #connection = Connection(clientSocket1,clientSocket2)
        #connection.start()

        #clientSocket1.close()
        #serverSocket.close()

def signal_handler(signal, frame):
    print 'intrrupt!'
    socket1.close()
    server.serverSocket.close()
    sys.exit(0)
    
class Client(threading.Thread):
    #clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    counter = 0

    def __init__(self,socket1,socket2):
        self.__class__.counter = self.__class__.counter + 1
        threading.Thread.__init__(self)
        self.sender = socket1
        self.recver = socket2        
        self.id = self.__class__.counter
        
    def run(self):
        
        #connection information & id sending
        print "start running",self.id
        self.sender.send("server connected")
        self.sender.send(str(self.id))
        
        #exchange name
        name = self.sender.recv(4096)
        self.recver.send(name)        
                
        #receive A
        A = self.sender.recv(4096)
        self.recver.sendall(A)        
            
        print ""
        while 1:
            message = self.sender.recv(4096)
            print "sender: ",name,"data: ",message
            self.recver.send(message)
            #self.recver.send(str(self.id))
        
        
if __name__ == '__main__':
    server = Server()
    signal.signal(signal.SIGINT, signal_handler)
    server.start()

        
        
        
        
        
