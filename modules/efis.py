from modules.base_module import BaseModule

class EFIS(BaseModule):
    def __init__(self, bus):
        super().__init__(bus, label=303, sdi=3, ssm=2, interval=1.5)
