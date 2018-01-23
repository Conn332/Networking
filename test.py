import threading
import socket
import networkClient
import queue

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.0.3.165",10000))


inq = queue.Queue()
outq = queue.Queue()
c = networkClient.client(inq,outq,s)

c.start()

class checkOutput(threading.Thread):
    def __init__(self,queue):
        self.queue = queue
        self.stop = threading.Event()
        super().__init__()
    def run(self):
        while not self.stop.isSet():
            while not self.queue.empt():
                print("Output: ",queue.get().decode('utf-8'))
    def join(self, timeout = None):
        super().join(timeout)
        self.stop.set()

client = checkOutput(outq)
client.start()


cmd = input()
while cmd != "":
    if cmd.split(' ')[0] == "add":
        f = open(cmd.split(' ')[2],"r")
        cmd = ' '.join(cmd.split(' ')[:2])+" "+f.read()
        f.close()
    inq.put(cmd.encode('utf-8'))
    cmd = input()
if c.isAlive():
    c.join()
client.join()
