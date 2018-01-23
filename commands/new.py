import threading
class Hello(threading.Thread):
    def __init__(self):
        super().__init__()
        self.stop = threading.Event()
    def run(self):
        count = 0
        while not self.stop.isSet():
            count += 1
        print(str(count)+". hello")
    def join(self, timeout=None):
        self.stop.set()
        super().join(timeout)
