from modules.base_module import BaseModule

class FMS(BaseModule):
    def __init__(self, bus):
        super().__init__(bus, label=202, sdi=2, ssm=1, interval=1.2)
