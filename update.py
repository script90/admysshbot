#!/usr/bin/env python3
# encoding: utf-8
import socket, threading, time
from os import system
system("clear")
#connnection
PORT = 1122
PASS = ''
RESPONSE = 'HTTP/1.1 200 OK\r\nContent-Length: '

 
class Server(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.running = False
        self.host = host
        self.port = port
        self.threads = []
        self.threadsLock = threading.Lock()
        self.logLock = threading.Lock()
        self.soc = ''

    def run(self):
        self.soc = socket.socket(socket.AF_INET)
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.soc.settimeout(2)
        self.soc.bind((self.host, self.port))
        self.soc.listen(1)
        self.running = True

        try:                    
            while self.running:
                try:
                    c, addr = self.soc.accept()
                    c.setblocking(1)
                except socket.timeout:
                    continue
                
                conn = ConnectionHandler(c, self, addr)
                conn.start();
                self.addConn(conn)
        finally:
            self.running = False
            self.soc.close()
            
    def printLog(self, log):
        self.logLock.acquire()
        print(log)
        self.logLock.release()
	
    def addConn(self, conn):
        try:
            self.threadsLock.acquire()
            if self.running:
                self.threads.append(conn)
        finally:
            self.threadsLock.release()
                    
    def removeConn(self, conn):
        try:
            self.threadsLock.acquire()
            if conn in self.threads:
                self.threads.remove(conn)
        finally:
            self.threadsLock.release()
                
    def close(self):
        try:
            self.running = False
            self.threadsLock.acquire()
            
            threads = list(self.threads)
            for c in threads:
                c.close()
        finally:
            self.threadsLock.release()
			

class ConnectionHandler(threading.Thread):
    def __init__(self, socClient, server, addr):
        threading.Thread.__init__(self)
        self.clientClosed = False
        
        self.client = socClient
        self.client_buffer = ''
        self.server = server
        self.log = 'Connection: ' + str(addr)

    def close(self):
        try:
            if not self.clientClosed:
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
        except:
            pass
        finally:
            self.clientClosed = True

    def run(self):
        try:
            file = open("update.txt","r")
            updatetxt = file.read()
#            tmp = RESPONSE + str(len(updatetxt)) + "\r\n\r\n"
#            self.client.send(tmp.encode())
            self.client.send(updatetxt.encode())
        except Exception as e:
            self.log += ' - error: ' + str(e)
            self.server.printLog(self.log)
            
        finally:
            self.close()
            self.server.removeConn(self)

def main():
    print ("\033[0;34m━"*8,"\033[1;32m UPDATE SERVER","\033[0;34m━"*8,"\n")
    
    print ("\033[1;33mPORTA:\033[1;32m " + str(PORT) + "\n")
    print ("\033[0;34m━"*10,"\033[1;32m AUTO UPDATE","\033[0;34m━\033[1;37m"*11,"\n")
    server = Server('127.0.0.1',PORT)
    server.start()
    while True:
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            print ('\nParando...')
            server.close()
            break
if __name__ == '__main__':
    main()
