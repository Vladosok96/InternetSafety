# Квадратичный генератор
def square_generator(length, x1=123):
    bits_sequence = ''
    N = 65535
    d = 16311
    a = 11233
    c = 65537
    x2 = 0

    while len(bits_sequence) < length:
        x2 = (d * (x1 ** 2) + (a * x1) + c) % N
        x1 = x2
        bits_sequence += bin(x1)[2:]

    return bits_sequence[:length]