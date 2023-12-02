from RabinMiller import rabin_miller_generator
import random


# Функция генерации публичного ключа
def generate_key():
    p = rabin_miller_generator()
    g = rabin_miller_generator()
    if p < g:
        _ = p
        p = g
        g = _
    x = random.randint(2, p - 2)
    y = pow(g, x, p)
    return y, g, p, x


# Шифрование
def encode(M: int, y: int, g: int, p: int):

    # 1. Вычисляется сессионный ключ.
    k = p
    while k > p - 2:
        k = rabin_miller_generator()

    # 2. Вычисляются числа a и b.
    a = pow(g, k, p)
    b = (M * pow(y, k, p)) % p

    return a, b


# Дешифрование
def decode(ab, x: int, p: int):
    a, b = ab

    s = pow(a, x, p)

    s_1 = pow(s, -1, p)

    M = (b * s_1) % p

    return M
