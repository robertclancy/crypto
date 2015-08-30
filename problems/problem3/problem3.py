from Crypto.Hash import SHA256
import os
import sys

def hash(block):
    h = SHA256.new()
    h.update(block)
    return h.digest()

def each_block_reverse(f, block_size):
    f.seek(0, os.SEEK_END)
    size = f.tell()
    last_block_size = size % block_size
    if last_block_size > 0:
        f.seek(-last_block_size, os.SEEK_CUR)
        yield f.read(last_block_size)
        f.seek(-last_block_size, os.SEEK_CUR)
    while f.tell() > 0:
        f.seek(-block_size, os.SEEK_CUR)
        yield f.read(block_size)
        f.seek(-block_size, os.SEEK_CUR)

if __name__ == "__main__":
    h = ''
    with open(sys.argv[1], 'rb') as f:
        for b in each_block_reverse(f, 1024):
            h = hash(b + h)
    print h.encode('hex')
