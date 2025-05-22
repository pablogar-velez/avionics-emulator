from modules.base_module import BaseModule

class Autopilot(BaseModule):
    def __init__(self, bus):
        super().__init__(bus, label=404, sdi=4, ssm=3, interval=1.8)
