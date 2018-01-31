import threading
import pigpio
class Hello(threading.Thread):
    def __init__(self,in_q,out_q):
        super().__init__()
        self.stop = threading.Event()
        self.pi = pigpio.pi()
        self.in_q = in_q
        self.out_q = out_q
    def run(self):
        while not self.stop.isSet():
            while not self.in_q.empty():
                inp = self.in_q.get().split(" ")
                self.pi.set_PWM_dutycycle(2,int(inp[0]))
                self.pi.set_PWM_dutycycle(3,int(inp[1]))
                self.pi.set_PWM_dutycycle(4,int(inp[2]))
                self.out_q.put("set lights to R:"+inp[0]+" G:"+inp[1]+" B:"+inp[2])
    def join(self, timeout=None):
        self.stop.set()
        super().join(timeout)
