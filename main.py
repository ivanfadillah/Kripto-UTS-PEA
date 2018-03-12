from pea import PEA

def ECB(text, key, decrypt=False):
    fullbits = text_to_bits(text)

    pea = PEA(key)
    bits_encrypt = []
    for i in range(int(len(fullbits)/256)):
        bits = fullbits[(i*256):((i+1)*256)]
        bits_encrypt.extend(pea.encrypt(bits, decrypt))

    return bits_to_text(bits_encrypt)

def CBC(text, key, init_vector, decrypt=False):
    fullbits = text_to_bits(text)

    pea = PEA(key)
    last_bits = init_vector
    bits_encrypt = []
    for i in range(int(len(fullbits)/256)):
        if not decrypt:
            bits = fullbits[(i*256):((i+1)*256)]
            bits = [x^y for (x,y) in zip(bits, last_bits)]
            res = pea.encrypt(bits, decrypt)
            last_bits = res
            bits_encrypt.extend(res)
        else:
            bits = fullbits[(i*256):((i+1)*256)]
            res = pea.encrypt(bits, decrypt)
            res = [x^y for (x,y) in zip(res, last_bits)]
            last_bits = bits
            bits_encrypt.extend(res)

    return bits_to_text(bits_encrypt)

def CFB(text, key, init_vector, nbits, decrypt=False):
    '''
        nbits: encryption length
    '''
    if 256 % nbits != 0:
            raise Exception('Length of nbits must be a factor of 256!')
    fullbits = text_to_bits(text)

    pea = PEA(key)
    qbits = init_vector
    bits_encrypt = []
    for i in range(int(len(fullbits)/nbits)):
        if not decrypt:
            bits = fullbits[(i*nbits):((i+1)*nbits)]
            enc_res = pea.encrypt(qbits, False)
            res = [x^y for (x,y) in zip(bits, enc_res[:nbits])]
            bits_encrypt.extend(res)
            qbits = qbits[nbits:] + res
        else:
            bits = fullbits[(i*nbits):((i+1)*nbits)]
            enc_res = pea.encrypt(qbits, False)
            res = [x^y for (x,y) in zip(bits, enc_res[:nbits])]
            bits_encrypt.extend(res)
            qbits = qbits[nbits:] + bits

    return bits_to_text(bits_encrypt)

def OFB(text, key, init_vector, nbits, decrypt=False):
    '''
        nbits: encryption length
    '''
    if 256%nbits != 0:
            raise Exception('Length of nbits must be a factor of 256!')
    fullbits = text_to_bits(text)

    pea = PEA(key)
    qbits = init_vector
    bits_encrypt = []
    for i in range(int(len(fullbits)/nbits)):
        if not decrypt:
            bits = fullbits[(i*nbits):((i+1)*nbits)]
            enc_res = pea.encrypt(qbits, False)
            res = [x^y for (x,y) in zip(bits, enc_res[:nbits])]
            bits_encrypt.extend(res)
            qbits = qbits[nbits:] + enc_res[:nbits]
        else:
            bits = fullbits[(i*nbits):((i+1)*nbits)]
            enc_res = pea.encrypt(qbits, False)
            res = [x^y for (x,y) in zip(bits, enc_res[:nbits])]
            bits_encrypt.extend(res)
            qbits = qbits[nbits:] + enc_res[:nbits]

    return bits_to_text(bits_encrypt)

def CTR(text, key, decrypt=False):
    fullbits = text_to_bits(text)

    pea = PEA(key)
    bits_encrypt = []
    count = create_ctr_start(key)
    for i in range(int(len(fullbits)/256)):
        if not decrypt:
            bits = fullbits[(i*256):((i+1)*256)]
            cbits = int_to_bits(count)
            enc_res = pea.encrypt(cbits, False)
            res = [x^y for (x,y) in zip(bits, enc_res)]
            bits_encrypt.extend(res)
        else:
            bits = fullbits[(i*256):((i+1)*256)]
            cbits = int_to_bits(count)
            enc_res = pea.encrypt(cbits, False)
            res = [x^y for (x,y) in zip(bits, enc_res)]
            bits_encrypt.extend(res)
        count += 1

    return bits_to_text(bits_encrypt)

def create_ctr_start(key):
    bits = text_to_bits(key)
    sum = 0
    for bit in bits:
        sum += bit
    return sum

def int_to_bits(n):
    bits = [int(digit) for digit in bin(n)[2:]]
    if len(bits) < 256:
        return ([0] * (256-len(bits))) + bits
    return bits[256:]

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
    text = 'onika tanya maraj'
    bits = text_to_bits(text)
    print(bits)
    print(bits_to_text(bits))

    print('\CTR:')
    enc = CTR(text, text)
    print(enc)
    print(CTR(enc, text, True))

    print('\nECB:')
    enc = ECB(text, text)
    print(enc)
    print(ECB(enc, text, True))

    print('\nCBC:')
    iv = [1] * 256
    enc = CBC(text, text, iv)
    print(enc)
    print(CBC(enc, text, iv, True))

    print('\nCFB:')
    iv = [1] * 256
    enc = CFB(text, text, iv, 256)
    print(enc)
    print(CFB(enc, text, iv, 256, True))

    print('\nOFB:')
    iv = [1] * 256
    enc = OFB(text, text, iv, 256)
    print(enc)
    print(OFB(enc, text, iv, 256, True))
