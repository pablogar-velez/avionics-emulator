import threading
import time
import random

class BaseModule(threading.Thread):
    def __init__(self, bus, label, sdi, ssm, interval):
        super().__init__()
        self.bus = bus
        self.label = label
        self.sdi = sdi
        self.ssm = ssm
        self.interval = interval
        self.running = True

    def run(self):
        while self.running:
            data = random.randint(100000, 999999)
            msg = f"Label:{self.label} SDI:{self.sdi} Data:{data} SSM:{self.ssm}"
            self.bus.transmit(msg)
            time.sleep(self.interval)

    def stop(self):
        self.running = False
