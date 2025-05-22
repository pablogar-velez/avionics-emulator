class ARINC429Message:
    def __init__(self, label: int, sdi: int, data: int, ssm: int):
        self.label = label
        self.sdi = sdi
        self.data = data
        self.ssm = ssm
