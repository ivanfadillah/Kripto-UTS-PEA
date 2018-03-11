import numpy as np

from permute import MatrixPermute
from keygen import KeyGenerator

class Feistel():
    def __init__(self, lmatrix, rmatrix, subkeys):
        self.lmatrix = lmatrix
        self.rmatrix = rmatrix
        self.subkeys = subkeys
        
    def reduce_subkey(self, subkey):
        _subkey = []
        for i in range(8):
            seedkey = subkey[(i*12):((i+1)*12)]
            sbox = KeyGenerator.get_sbox(sum(seedkey))
            seedkey_str = ''.join([str(x) for x in seedkey])
            row, col = int(seedkey_str[6], 2), int(seedkey_str[6:12], 2)
            _subkey.append('{:08b}'.format(sbox[row][col]))
        return [int(c) for x in _subkey for c in x]

if __name__=='__main__':
    k = KeyGenerator('hello adelle')
    f = Feistel(None, None, k.get_subkeys())    
    subkey = f.reduce_subkey(f.subkeys[0])
    print(subkey)