import random
import randomgenerators
import binoperations


# Тест Рабина-Миллера
def rabin_miller(p: int, a: int):
    # 1. Число делений p-1 на 2. Затем вычисляется m, такое что p = 1 + 2b * m.
    m = p - 1
    b = 0
    while m % 2 == 0:
        m //= 2
        b += 1

    # 2. Установка j = 0 и z = a^m mod p.
    j = 0
    z = pow(a, m, p)

    while True:

        # 3. Если z = 1 или если z = p - 1, то p проходит проверку и может быть простым числом.
        if z == 1 or z == p - 1:
            return True

        # 4. Если j > 0 и z = 1, то p не является простым числом.
        if j > 0 and z == 1:
            return False

        # 5. Установите j = j + 1. Если j < b и z ≠ p - 1, установите z = z^2 mod p и вернитесь на этап (3).
        j += 1
        if j < b and z != p - 1:
            z = (z ** 2) % p
            continue

        # 6. Если z = p - 1, то p проходит проверку и может быть простым числом.
        if z == p - 1:
            return True

        # 7. Если j = b и z ≠ p - 1, то p не является простым числом.
        if j >= b and z != p - 1:
            return False


# Пять проверок Рабина-Миллера
def rabin_miller_test(num: int):
    for i in range(5):
        random_num = random.randint(1, min(num, 200000))
        if rabin_miller(num, random_num) == False:
            return False
    return True


# Генератор простого чисел на основе теста Рабина-Миллера
def rabin_miller_generator():

    while True:
        # 1. Сгенерируйте случайное n-битовое число p
        p = randomgenerators.square_generator(128)

        # 2. Установите старший и младший биты равными 1.
        p = binoperations.set_bit(p, 127, 1)
        p = binoperations.set_bit(p, 0, 1)

        if rabin_miller_test(p):
            return p
