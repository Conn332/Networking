import threading
import socket
import networkClient
import queue

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost",10000))


inq = queue.Queue()
outq = queue.Queue()
c = networkClient.client(inq,outq,s)

c.start()
cmd = input()
while cmd != "":
    if cmd.split(' ')[0] == "add":
        f = open(cmd.split(' ')[2],"r")
        cmd = ' '.join(cmd.split(' ')[:2])+" "+f.read()
        f.close()
    inq.put(cmd.encode('utf-8'))
    while not outq.empty():
        print("Output: ",outq.get().decode('utf-8'))
    cmd = input()
if c.isAlive():
    c.join()
