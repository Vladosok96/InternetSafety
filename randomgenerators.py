import random


# Квадратичный генератор
def square_generator(length: int):
    bits_sequence = ''
    N = 65535
    d = 16311
    a = 11233
    c = 65537
    x1 = random.randint(1, 100000000)
    x2 = 0

    while len(bits_sequence) < length:
        x2 = (d * (x1 ** 2) + (a * x1) + c) % N
        x1 = x2
        bits_sequence += bin(x1)[2:]

    return int(bits_sequence[:length], 2)
