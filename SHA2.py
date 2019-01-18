#--------------------CONSTANT VALUES--------------------#
constants = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

keys = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
]

 #------------------------METHODS------------------------#


def Add(h1, h2):
    sum_up = hex(h1 + h2).replace("L", "")
    if len(sum_up[2:]) > 8:
        step = "0x" + sum_up[-8:]
    else:
        step = sum_up
    return int(step, base=0)


def Not(h1):
    return 0xffffffff - h1


def rightRotate(h1, steps):
    factor = steps % 32
    binword = bin(h1)[2:].zfill(32)
    return int(binword[-factor:] + binword[:-factor], base=2)


def messageCreator(object):
    string = str(object)
    init = "".join([bin(ord(char))[2:].zfill(8) for char in string])
    init_len = bin(len(init))[2:].zfill(64)
    if len(init) % 512 < 447:
        zeros = 447 - len(init) % 512
    else:
        zeros = 959 - len(init) % 512
    binMessage = init + "1" + "0"*zeros + init_len
    return binMessage


def wordsCreator(message):
    words = []
    for x in xrange(16):
        words.append(int(message[(32*x):(32+32*x)], base=2))
    for i in xrange(16, 64):
        s0 = (rightRotate(words[i-15], 7) ^
              rightRotate(words[i-15], 18)) ^ (words[i-15] >> 3)
        s1 = (rightRotate(words[i-2], 17) ^
              rightRotate(words[i-2], 19)) ^ (words[i-2] >> 10)
        created_word = Add(Add(Add(words[i-16], s0), words[i-7]), s1)
        words.append(created_word)
    return words


def bowelsLoop(words):
    a, b, c, d, e, f, g, h = keys
    for i in xrange(64):
        s0 = (rightRotate(e, 6) ^ rightRotate(e, 11)) ^ rightRotate(e, 25)
        ch = (e & f) ^ (Not(e) & g)
        t0 = Add(Add(Add(Add(h, s0), ch), constants[i]), words[i])
        s1 = (rightRotate(a, 2) ^ rightRotate(a, 13)) ^ rightRotate(a, 22)
        maj = (a & b) ^ (a % c) ^ (b & c)
        t1 = Add(s1, maj)
        h, g, f, e, d, c, b, a = g, f, e, Add(d, t0), c, b, a, Add(t0, t1)
    blockExitValues = [a, b, c, d, e, f, g, h]
    return blockExitValues


def digest():
    result = "".join([hex(key)[2:].replace("L", "").zfill(8) for key in keys])
    return "0x" + result


 #---------------------MAIN FUNCTION---------------------#


def Hash(object):
    """ Hash(object) -> str
     Returns a string of hash value for object object"""

    global keys
    binMessage = messageCreator(object)
    blocks = len(binMessage)/512
    for index in xrange(blocks):
        binMessage_block = binMessage[512*index: 512*index+512]
        words = wordsCreator(binMessage_block)
        blockExitValues = bowelsLoop(words)
        for i in xrange(8):
            keys[i] = Add(keys[i], blockExitValues[i])
    result = digest()
    keys = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]
    return result


def Test():
    user_input = raw_input("Type in string to hash: ").strip()
    print Hash(user_input)


if __name__ == "__main__":
    Test()