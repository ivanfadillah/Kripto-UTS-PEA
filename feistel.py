class Feistel():
    def __init__(self, sbox1, sbox2):
        self.lbox = sbox1
        self.rbox = sbox2