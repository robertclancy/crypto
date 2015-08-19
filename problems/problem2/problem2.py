from Crypto.Cipher import AES
from struct import pack, unpack

def _strxor(a, b):
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b)])

def _split(line, block_size):
    return [line[i:i+block_size] for i in range(0, len(line), block_size)]

class CBC:
    def __init__(self, key):
        self.aes = AES.new(key, AES.MODE_ECB)

    def encrypt(self, iv, plain):
        pad_len = len(plain) % 16
        padding = None
        if pad_len == 0:
            padding = pack('B', 16) * 16
        else:
            padding = pack('B', pad_len) * pad_len
        blocks = _split(plain + padding, 16)
        b = iv
        e_blocks = [iv]
        for block in blocks:
            b = self.aes.encrypt(_strxor(b, block))
            e_blocks.append(b)
        return "".join(e_blocks)

    def decrypt(self, cipher):
        e_blocks = _split(cipher, 16)
        iv = e_blocks[0]
        c_blocks = e_blocks[1:]
        p_blocks = []
        b = iv
        for block in c_blocks:
            p_blocks.append(_strxor(self.aes.decrypt(block), b))
            b = block
        plain = "".join(p_blocks)
        pad_length = unpack('B', plain[-1])[0]
        return [iv, plain[:-pad_length]]

class CTR:
    def __init__(self, key):
        self.aes = AES.new(key, AES.MODE_ECB)

    @staticmethod
    def _increment_counter(counter, increment):
        high = counter[:8]
        low = counter[8:]
        n = pack('!Q', unpack('!Q', low)[0] + increment)
        return high + n

    def encrypt(self, iv, plain):
        p_blocks = _split(plain, 16)
        c_blocks = [iv]
        b = iv
        for block in p_blocks:
            c_blocks.append(_strxor(block, self.aes.encrypt(b)))
            b = self._increment_counter(b, 1)
        return "".join(c_blocks)

    def decrypt(self, cipher):
        iv = cipher[:16]
        e_blocks = cipher[16:]
        dec = self.encrypt(iv, e_blocks)
        return [dec[:16], dec[16:]]
