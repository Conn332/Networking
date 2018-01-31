#!/usr/bin/python3
import importlib
import os
import networkServer
import networkClient
import queue
import socket
import sys

in_q = queue.Queue()
out_q = queue.Queue()
server = networkServer.server(in_q,out_q)
server.start()

working = True

restart = False

running = {}
threadInQ = {}
threadOutQ = {}
while working:
    for key in threadOutQ.keys():
        while not threadOutQ[key].empty():
            in_q.put(threadOutQ[key].get())
    if not out_q.empty():
        inp = out_q.get().decode('utf-8').split(' ')
        print(inp)
        cmd = inp[0]
        if cmd == "add":
            functionName = inp[1]
            fileData = ' '.join(inp[2:])

            fN = open("commands/"+functionName+".py","w")
            fN.write(fileData)
            fN.close()
        elif cmd == "remove":
            os.remove("commands/"+inp[1]+".py")
        elif cmd == "kill":
            if inp[1] in running.keys():
                running.pop(inp[1]).join()
            else:
                print("threadNotAlive")
        elif cmd == "quit":
            working = False
        elif cmd == "echo":
            in_q.put(' '.join(inp[1:]).encode('utf-8'))
        elif cmd == "update":
            os.system("git pull --rebase network master")
            working = False
            in_q.put(b"Manual Update Required.")
        else:
            if inp[0] in running.keys():
                threadInQ[inp[0]].put(' '.join(inp[1:]))
            else:
                imp = importlib.import_module("commands."+inp[0])
                threadInQ[inp[0]] = queue.Queue()
                threadOutQ[inp[0]] = queue.Queue()
                running[inp[0]] = getattr(imp,[i for i in dir(imp) if i[0] != "_"][0])(threadInQ[inp[0]],threadOutQ[inp[0]])
                running[inp[0]].start()
for thread in running:
    thread.join()
server.join()
