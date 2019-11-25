import base64
import sys


# challenge 1
def hex_to_base64(h):
    return base64.b64encode(base64.b16decode(h.upper()))


# challenge 2
def hex_xor_hex(h1, h2):
    b1 = bytes.fromhex(h1)
    b2 = bytes.fromhex(h2)
    assert len(b1) == len(b2)

    x = b''
    for i in range(len(b1)):
        x += bytes([b1[i] ^ b2[i]])

    return format(int.from_bytes(x, 'big'), 'X')


# challenge 3
def _single_xor_hex(h, c):
    b = bytes.fromhex(h)

    x = b''
    for char in b:
        x += bytes([char ^ c])

    return x


def single_xor_hex(h):
    for i in range(256):
        b = _single_xor_hex(h, i)
        try:
            if b.decode().strip().isprintable():
                print('{}: {}'.format(chr(i), b))
        except UnicodeDecodeError:
            continue


# challenge 4
def single_xor_file():
    for line in sys.stdin:
        print(line.strip())
        single_xor_hex(line.strip())


if __name__ == '__main__':
    if sys.argv[1] == '1':
        print(hex_to_base64(sys.argv[2]).decode())
        # b"I'm killing your brain like a poisonous mushroom"

    elif sys.argv[1] == '2':
        print(hex_xor_hex(sys.argv[2], sys.argv[3]))
        # b"the kid don't play"

    elif sys.argv[1] == '3':
        single_xor_hex(sys.argv[2])
        # X: b"Cooking MC's like a pound of bacon"

    elif sys.argv[1] == '4':
        single_xor_file()
        # 7b5a4215415d544115415d5015455447414c155c46155f4058455c5b523f
        # 5: b'Now that the party is jumping\n'
