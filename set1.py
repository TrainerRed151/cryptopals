import base64
import csv
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
def english_score(sentence):
    score = 0
    word_list = sentence.split()
    for word in word_list:
        if word in english_words:
            score += 1

    return score/len(word_list)


def _single_xor_hex(h, c):
    b = bytes.fromhex(h)

    x = b''
    for char in b:
        x += bytes([char ^ c])

    return x


def single_xor_hex(h):
    score_tuples = []
    for i in range(256):
        b = _single_xor_hex(h, i)
        try:
            sentence = b.decode().strip()
            if sentence.isprintable():
                score_tuples.append((english_score(sentence), sentence))
        except UnicodeDecodeError:
            continue

    score_tuples.sort()
    #for score, sen in score_tuples:
    #    print(f'{score}: {sen}')

    return score_tuples


# challenge 4
def single_xor_file():
    score_tuples = []
    xor_lines = []
    with open('set1-ex4.txt', 'r') as f:
        csv_lines = csv.reader(f)
        for row in csv_lines:
            xor_lines.append(row[0])

    for line in xor_lines:
        for line_tuples in single_xor_hex(line.strip()):
            score_tuples.append((line_tuples[0], line_tuples[1], line.strip()))

    score_tuples.sort()
    for score, sen, line in score_tuples:
        print(f'{score}: {sen} ({line})')


# challenge 5
def repeating_key_xor(f, key):
    with open(f, 'r') as myfile:
        data = myfile.read()

    b_string = data.strip().encode()
    b_key = key.encode()
    key_pos = 0
    cipher = b''
    for b in b_string:
        cipher += bytes([b ^ b_key[key_pos]])
        key_pos = (key_pos + 1) % len(b_key)

    return cipher.hex()


if __name__ == '__main__':
    english_words = []
    with open('words.txt', 'r') as f:
        csv_lines = csv.reader(f)
        for word in csv_lines:
            english_words.append(word[0])

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

    elif sys.argv[1] == '5':
        print(repeating_key_xor(sys.argv[2], sys.argv[3]))
