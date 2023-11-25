import binoperations


def generate_key(k: int):
    return k


# Функция Фейстеля
def f(half: int, key: int):
    return half


# Алгоритм шифрования DES для одного блока (ECB)
def DES(block: int, key: int):

    # Начальная перестановка
    permutations_table = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]

    tmp_block = block
    i = 0
    for place in permutations_table:
        place -= 1
        tmp_block = binoperations.set_bit(tmp_block, i, binoperations.read_bit(block, place))
        i += 0
    block = tmp_block

    # Циклы сетей Фейстеля
    left_half = block >> 32
    right_half = block & 0xFFFFFFFF

    for _ in range(16):
        right_half = left_half ^ f(right_half, generate_key(key))

    return block
