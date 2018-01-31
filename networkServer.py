import threading
import socket
import networkClient
import queue

class server(threading.Thread):
    def __init__(self, in_q, out_q):
        super().__init__()
        self.in_q = in_q
        self.out_q = out_q
        self.stop = threading.Event()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = ("0.0.0.0", 10000)
        self.socket.bind(address)
        self.socket.listen(1)
        self.connections = {}
        self.inputs = {}
        self.outputs = {}
    def run(self):
        while not self.stop.isSet():
            try:
                self.socket.settimeout(.5)
                connection, clAddress = self.socket.accept()
            except socket.timeout:
                remove = []
                for key in self.outputs.keys():
                    if self.connections[key].isAlive():
                        while not self.outputs[key].empty():
                            out = self.outputs[key].get()
                            self.out_q.put(out)
                            print("Output: ",out)
                    else:
                        remove.append(key)
                for key in remove:
                    self.connections.pop(key, False)
                    self.inputs.pop(key, False)
                    self.outputs.pop(key, False)

                while not self.in_q.empty():
                    msg = self.in_q.get()
                    for key in self.inputs.keys():
                        self.inputs[key].put(msg)
            except:
                raise
            else:
                print(clAddress)
                self.inputs[clAddress] = queue.Queue()
                self.outputs[clAddress] = queue.Queue()
                self.connections[clAddress] = networkClient.client(self.inputs[clAddress], self.outputs[clAddress],connection)
                self.connections[clAddress].start()
                print(len(self.connections.keys()))

    def join(self, timeout = None):
        self.stop.set()
        for key in self.connections.keys():
            self.connections[key].join()
        self.socket.close()
        super().join(timeout)
#inq = queue.Queue()
#outq = queue.Queue()
#s = server(inq, outq)
#s.start()
#cmd = input()
#while cmd != "":
#    inq.put(cmd.encode('utf-8'))
#    while not outq.empty():
#        print("Output: ",outq.get().decode('utf-8'))
#    cmd = input()
#s.join()
