from pea import PEA

def ECB(text, key, decrypt=False):
    fullbits = text_to_bits(text)
    
    pea = PEA(key)
    bits_encrypt = []
    for i in range(int(len(fullbits)/256)):
        bits = fullbits[(i*256):((i+1)*256)]    
        bits_encrypt.extend(pea.encrypt(bits, decrypt))
        
    return bits_to_text(bits_encrypt)
        
def text_to_bits(text):
    bits_str = ''.join(['{:08b}'.format(ord(c)) for c in text])
    fullbits = [int(c) for c in bits_str]
    while (len(fullbits) % 256) != 0:
        fullbits.append(0)
    
    return fullbits

def bits_to_text(bits):
    text = ''
    for i in range(int(len(bits)/8)):
        byte = ''.join([str(x) for x in bits[(i*8):(i+1)*8]])
        text += chr(int(byte, 2))
    
    return text

if __name__=='__main__':
    text = 'onika maraj'
    bits = text_to_bits(text)
    print(bits)
    print(bits_to_text(bits))
    
    enc = ECB(text, text)
    print(enc)
    print(ECB(enc, text, True))