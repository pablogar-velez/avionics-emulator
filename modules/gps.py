from modules.base_module import BaseModule

class GPS(BaseModule):
    def __init__(self, bus):
        super().__init__(bus, label=101, sdi=1, ssm=0, interval=1.0)
