import urllib2
import sys

TARGET = 'http://crypto-class.appspot.com/po?er='
CIPHERTEXT = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'

# http://mdickens.me/typing/letter_frequency.html
# treats capitals as rare (bug)
def build_letter_frequencies():
    letters = """SPC e t a o i n s r h l d c u m f g p y w ENT b , . v k - " _ ' x ) ( ; 0 j 1 q = 2 : z / * ! ? $ 3 5 > { } 4 9 [ ] 8 6 7 \ + | & < % @ # ^ ` ~"""
    common = [ord(x) for x in letters.replace(" ", "").replace("SPC", " ").replace("ENT", "\n")]
    rare = list(set(range(0, 256)) - set(common))
    return common + rare
ASCII = build_letter_frequencies()
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:          
            print "We got: %d" % e.code       # Print response code
            if e.code == 404:
                return True # good padding
            return False # bad padding

def in_blocks(text, block_size):
    return [text[i*block_size:(i+1)*block_size] for i in range(0, len(text) / block_size)]

def determine_padding(cipher, oracle):
    c_blocks = in_blocks(cipher, 16)
    prefix = c_blocks[0:-2]
    penultimate = c_blocks[-2]
    last = c_blocks[-1]
    valid = None
    for g in range(0x01, 0xff + 1):
        guess = prefix + [str_xor(guess_block(chr(g)), penultimate), last]
        if oracle.query("".join(guess).encode('hex')):
            valid = g
            break
    if valid is None:
        raise Exception('no valid padding found')
    return valid

def guess_block(end):
    return ('\0' * (16 - len(end))) + str_xor(end, chr(len(end)) * len(end))

def str_xor(x, y):
    return "".join([chr(ord(i) ^ ord(j)) for (i, j) in zip(x, y)])

def decode_last_block(c_blocks, oracle, suffix=''):
    while len(suffix) < 16:
        prefix = c_blocks[0:-2]
        penultimate = c_blocks[-2]
        last = c_blocks[-1]
        for g in ASCII:
            guess = prefix + [str_xor(guess_block(chr(g) + suffix), penultimate), last]
            if oracle.query("".join(guess).encode('hex')):
                valid = g
                break
        if valid is None:
            raise Exception('no valid padding found')
        suffix = chr(valid) + suffix
    return suffix

def decode_cipher(cipher, oracle):
    c_blocks = in_blocks(cipher, 16)
    plain_blocks = []
    padding = determine_padding(cipher, oracle)
    plain_blocks.append(decode_last_block(c_blocks, oracle, chr(padding) * padding)[0:-padding])
    for b in range(len(c_blocks) - 1, 1, -1):
        plain_blocks.insert(0, decode_last_block(c_blocks[0:b], oracle))
    return "".join(plain_blocks)

if __name__ == "__main__":
    po = PaddingOracle()
    print decode_cipher(CIPHERTEXT.decode('hex'), po)
