import PySimpleGUI as sg
from random import randint
import math
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
import hashlib


def find_coprime(n):
    coprime = randint(1, n)  # Можете начать с 2 или любого другого числа
    while math.gcd(n, coprime) != 1:
        coprime += 1
    return coprime


# Генератор BBS
def bbs_generator(length):
    bits_sequence = ''
    p = 0
    q = 1
    while p % 4 != q % 4 or q % 4 != 3 % 4:
        p = randint(0, 2 ** 160)
        q = randint(0, 2 ** 160)
    N = p * q
    s = find_coprime(N)
    u0 = s ** 2 % N
    for _ in range(length):
        u1 = u0 ** 2 % N
        u0 = u1
        bits_sequence += bin(u0)[-1]

    return bits_sequence


def f(Ai, Xi):
    # Сложение по модулю 2^32
    result = (Ai + Xi) % (2 ** 32)

    # Разбиение на восемь 4-битовых подпоследовательностей
    sub_sequences = [(result >> i) & 0xF for i in range(0, 32, 4)]

    # S-блоки
    s_box = [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12]

    # Применение S-блоков к каждой подпоследовательности
    s_box_results = [s_box[sub_sequence] for sub_sequence in sub_sequences]

    # Объединение результатов S-блоков в 32-битное слово
    combined_result = sum((s_box_result << i) for i, s_box_result in enumerate(s_box_results))

    # Циклический сдвиг влево на 11 битов
    final_result = ((combined_result << 11) | (combined_result >> (32 - 11))) % (2 ** 32)

    return final_result


def Ek(A, Key):
    A0 = A & 0xFFFFFFFF
    B0 = (A >> 32) & 0xFFFFFFFF

    # Разделение 256-битного числа на 8 32-битных чисел
    K = [((Key >> i) & 0xFFFFFFFF) for i in range(0, 256, 32)]

    # Создание нового списка из 32-битных чисел
    X = []

    # Добавление первых 24 чисел (циклическое повторение чисел K)
    for _ in range(3):
        X.extend(K)

    # Добавление оставшихся 8 чисел (числа K в обратном порядке)
    X.extend(reversed(K))

    for Xi in range(32):
        A0 = B0 ^ f(A0, Xi)
        B0 = A0

    return (B0 << 32) | A0


# layout = [[sg.Text('Шифрование', font=("Helvetica", 14))],
#           [sg.Text('Сообщение:'), sg.Input()],
#           [sg.Button('Зашифровать')],
#           [sg.Text('Результат: ', key='-encryption-')],
#           [sg.Text('Открыть файл:'), sg.FileBrowse()],
#           [sg.Button('Запись'), sg.Button('Чтение')],
#           [sg.HorizontalSeparator()],
#           [sg.Text('Дешифрование', font=("Helvetica", 14))],
#           [sg.Text('Сообщение:'), sg.Input()],
#           [sg.Button('Дешифровать')],
#           [sg.Text('Результат: ', key='-encryption-')],
#          ]

layout = [[sg.Text('Шифрование', font=("Helvetica", 14))],
          [sg.Text('Сообщение:'), sg.Input()],
          [sg.Button('Зашифровать')],
          [sg.Text('Результат: ', key='-encryption-')],
          [sg.HorizontalSeparator()],
          [sg.Text('Дешифрование', font=("Helvetica", 14))],
          [sg.Text('Сообщение:'), sg.Input()],
          [sg.Button('Дешифровать')],
          [sg.Text('Результат: ', key='-encryption-')],
         ]


def r(k, arr):
    if arr[k] != arr[k + 1]:
        return 1
    return 0


if __name__ == '__main__':

    window = sg.Window('Тестирование псевдослучайных последовательностей', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            runGame = False
            break

        # Запуск алгоритма шифрования
        if event == 'Зашифровать':
            input_message = values[0]

            M = []
            for n in range(math.ceil(len(input_message) / 32)):
                mn = bytes(input_message[n*32:(n+1)*32], 'utf-8')
                if len(mn) < 32:
                    mn += b'\x00' * (32 - len(mn))
                print(int.from_bytes(mn, byteorder='big'), len(mn) * 8)
                M.append(int.from_bytes(mn, byteorder='big'))

            h = bbs_generator(256)
            SUM = 0
            L = 0

            for i in range(len(M)):
                h = f(h, M[i])
                L += 256
                SUM += M[i]

            L += 256
            Mn = 0
            SUM += Mn
            h = f(h, Mn)
            h = f(h, L)
            H = f(h, SUM)


        # Запуск алгоритма дешифрования
        if event == 'Дешифровать':
            pass

        # Запись сгенерированной последовательности в файл
        if event == 'Запись':
            if values['Browse'] != '' and bits_sequence != '':
                f = open(values['Browse'], mode='w')
                f.write(bits_sequence)
                f.close()

        # Чтение готовой последовательности из файла
        if event == 'Чтение':
            if values['Browse'] != '':
                f = open(values['Browse'], 'r')
                bits_sequence = f.read()
                short_sequence = bits_sequence[:10] + '...' + bits_sequence[-10:]
                window['-sequence-'].update(f'Последовательность: {short_sequence}')

        # Выполнение частотного теста
        if event == '-begin_frequency-':
            X_sequence = []
            Sn = 0
            for character in bits_sequence:
                X_sequence.append(2 * int(character) - 1)
                Sn += X_sequence[-1]
            result = abs(Sn) / math.sqrt(len(X_sequence))
            window['-frequency-'].update(f'Результат: {result}')

        # Выполнение теста на последовательность одинаковых бит
        if event == '-begin_same_bits-':
            ones_count = 0
            Vn = 1

            for i in range(len(bits_sequence)):
                ones_count += int(bits_sequence[i])
                if i < len(bits_sequence) - 1:
                    Vn += r(i, bits_sequence)
            frequency = ones_count / len(bits_sequence)

            S = abs(Vn - 2 * len(bits_sequence) * frequency * (1 - frequency))
            S /= 2 * pow(2 * len(bits_sequence), 0.5) * frequency * (1 - frequency)

            window['-ones_frequency-'].update(f'Частота единиц: {frequency}')
            window['-Vn-'].update(f'Vn: {Vn}')
            window['-statistics-'].update(f'Статистика: {S}')

        # Выполнение расширенного теста на произвольные отклонения
        if event == '-begin_deviation-':
            X_sequence = []
            sum_sequence = [0]
            Sn = 0
            states = {}

            for character in bits_sequence:
                X_sequence.append(2 * int(character) - 1)
                sum_sequence.append(sum_sequence[-1] + X_sequence[-1])
            sum_sequence.pop(0)

            short_sequence = str(sum_sequence[:5]) + '...' + str(sum_sequence[-5:])
            window['-sums-'].update(f'Суммы последовательностей: {short_sequence}')

            sum_sequence.insert(0, 0)
            sum_sequence.append(0)

            L = -1
            for i in sum_sequence:
                if i == 0:
                    L += 1
            window['-L-'].update(f'Количество нулей: {L}')

            for i in range(-9, 10):
                if i != 0:
                    states[i] = 0
            for element in sum_sequence:
                if -10 < element < 10 and element != 0:
                    states[element] += 1

            result = ''
            counter = -9
            max_statistics = 0
            for i in range(3):
                for j in range(6):
                    if counter != 0:
                        Yj = abs(states[counter] - L)
                        Yj /= pow(2 * L * (4 * abs(counter) - 2), 0.5)
                        result += f'{counter}= {Yj:.2f}, '
                        max_statistics = max(Yj, max_statistics)
                    counter += 1
                if i < 2:
                    result += '\n'
            window['-deviation_statistics-'].update(f'Статистики: {result}')
            window['-maximum_statistics-'].update(f'Максимальное: {max_statistics}')


