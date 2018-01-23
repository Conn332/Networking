import threading
import queue
import socket

class client(threading.Thread):
    def __init__(self, in_q, out_q, socket):
        super().__init__()
        self.in_q = in_q
        self.out_q = out_q
        self.socket = socket
        self.stop = threading.Event()
    def run(self):
        print("Thread Running!")
        while not self.stop.isSet():
            if self.checkStatus():
                if self.in_q.empty():
                    out = self.receive()
                    if out:
                        self.out_q.put(out)
                else:
                    print("Send queue not empty")
                    self.send(self.in_q.get())
        self.socket.close()
    def send(self, msg): #takes msg as bytes object
        totalsent = 0
        print("Sending: ",msg)
        while totalsent < len(msg):
            sent = self.socket.send(msg[totalsent:])
            if sent == 0:
                self.join()
            totalsent += sent
            print("sent: ",msg[:totalsent])
    def receive(self):
        chunks = b''
        try:
            self.socket.settimeout(.5)
            data = self.socket.recv(16)
        except socket.timeout:
            pass
        except ConnectionAbortedError:
            print("Connection Aborted. Shutting Down thread.")
            self.socket.close()
            self.stop.set()
        except:
            raise
        else:
            while data:
                chunks+=data
                try:
                    data = self.socket.recv(16)
                    print(data)
                except socket.timeout:
                    data = None
                except ConnectionAbortedError:
                    print("Connection Aborted. Shutting Down thread.")
                    self.socket.close()
                    self.stop.set()
                except:
                    raise
            if chunks == b'':
                return None
            return chunks
    def checkStatus(self):
        try:
            self.socket.settimeout(.0001)
            data = self.socket.recv(1)
        except socket.timeout:
            return True
        except ConnectionAbortedError:
            print("Connection Aborted. Shutting Down thread.")
            self.socket.close()
            self.stop.set()
            return False
        except:
            raise
    def join(self, timeout = None):
        self.stop.set()
        super().join(timeout)
