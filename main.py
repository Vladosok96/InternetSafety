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


layout = [[sg.Drop(('Квадратичный конгруэнтный генератор', 'Генератор BBS', 'Yarrow-160'), key='-generator_type-')],
          [sg.Text('Длина последовательности:'), sg.Slider(orientation='h', range=(1000, 10000), resolution=1000, default_value=1000)],
          [sg.Text('Последовательность: ', key='-sequence-')],
          [sg.Button('Генерация')],
          [sg.Text('Открыть файл:'), sg.FileBrowse()],
          [sg.Button('Запись'), sg.Button('Чтение')],
          [sg.HorizontalSeparator()],
          [sg.Text('Частотный тест')],
          [sg.Text('Результат: ', key='-frequency-')],
          [sg.Button('Запуск', key="-begin_frequency-")],
          [sg.HorizontalSeparator()],
          [sg.Text('Последовательность одинаковых бит')],
          [sg.Text('Частота единиц: ', key='-ones_frequency-')],
          [sg.Text('Vn: ', key='-Vn-')],
          [sg.Text('Статистика: ', key='-statistics-')],
          [sg.Button('Запуск', key="-begin_same_bits-")],
          [sg.HorizontalSeparator()],
          [sg.Text('Тест на произвольные отклонения')],
          [sg.Text('Суммы последовательностей: ', key='-sums-')],
          [sg.Text('Количество нулей: ', key='-L-')],
          [sg.Text('Статистики: ', key='-deviation_statistics-')],
          [sg.Text('Максимальное: ', key='-maximum_statistics-')],
          [sg.Button('Запуск', key="-begin_deviation-")],
         ]


def r(k, arr):
    if arr[k] != arr[k + 1]:
        return 1
    return 0


if __name__ == '__main__':

    # Общие переменные
    bits_sequence = ''

    window = sg.Window('Тестирование псевдослучайных последовательностей', layout, size=(600, 640))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            runGame = False
            break

        # Генерация последовательности нулей и единиц
        if event == 'Генерация':
            print(values)
            bits_sequence = ''

            if values['-generator_type-'] == 'Квадратичный конгруэнтный генератор':
                N = 65535
                d = 16311
                a = 11233
                c = 65537
                x1 = randint(1, N)
                x2 = 0

                while len(bits_sequence) < values[0]:
                    x2 = (d * (x1 ** 2) + (a * x1) + c) % N
                    x1 = x2
                    bits_sequence += bin(x1)[2:]
            if values['-generator_type-'] == 'Генератор BBS':
                p = 0
                q = 1
                while p % 4 != q % 4 or q % 4 != 3 % 4:
                    p = randint(0, 2**160)
                    q = randint(0, 2**160)
                N = p * q
                s = find_coprime(N)
                u0 = s**2 % N
                for _ in range(int(values[0])):
                    u1 = u0**2 % N
                    u0 = u1
                    bits_sequence += bin(u0)[-1]
            if values['-generator_type-'] == 'Yarrow-160':
                n = 64
                k = 64
                K = get_random_bytes(k // 8)
                Pg = 10
                Pt = 20
                t = 0
                curC = 350
                curPg = Pg
                curPt = Pt

                while len(bits_sequence) < int(values[0]):
                    if curPg == 0:
                        t += 1

                        # G(i)
                        curC = (curC + 1) % (2 ** n)
                        plaintext = curC.to_bytes(n // 8, byteorder='big')

                        cipher = DES.new(K, DES.MODE_ECB)
                        K = cipher.encrypt(plaintext)

                        curPg = Pg
                    if curPt == 0:
                        v = int.from_bytes(get_random_bytes(k // 8), byteorder='big')
                        v0 = hashlib.sha1((v | t).to_bytes(n // 8, byteorder='big')).digest()
                        vi = v0
                        for i in range(t):
                            vi = (int.from_bytes(vi, byteorder='big') | int.from_bytes(v0, byteorder='big') | i) % (2 ** 64)
                            vi = hashlib.sha1(vi.to_bytes(n // 8, byteorder='big')).digest()

                        # H(s, k)
                        s0 = (int.from_bytes(vi, byteorder='big') | int.from_bytes(K, byteorder='big')) % (2 ** 64)
                        s0 = hashlib.sha1(s0.to_bytes(n // 8, byteorder='big')).digest()
                        s = [int.from_bytes(s0, byteorder='big')]
                        for i in range(t):
                            s.append(s[0])
                            for j in range(len(s) - 1):
                                s[-1] |= s[j]
                            s[-1] %= (2 ** 64)
                            s[-1] = hashlib.sha1(s[-1].to_bytes(n // 8, byteorder='big')).digest()
                            s[-1] = int.from_bytes(s[-1], byteorder='big')
                        tmpK = s[0]
                        for i in range(1, len(s)):
                            tmpK |= s[i]
                        K = int(bin(tmpK)[2:k+2], 2).to_bytes(n // 8, byteorder='big')

                        plaintext = (0).to_bytes(n // 8, byteorder='big')
                        cipher = DES.new(K, DES.MODE_ECB)
                        curC = int.from_bytes(cipher.encrypt(plaintext), byteorder='big')

                        curPt = Pt
                        curPg = Pg
                        t += 1

                    # G(i)
                    t += 1
                    curC = (curC + 1) % (2 ** n)
                    plaintext = curC.to_bytes(n // 8, byteorder='big')

                    cipher = DES.new(K, DES.MODE_ECB)
                    bits_sequence += bin(int.from_bytes(cipher.encrypt(plaintext), byteorder='big'))[2:]

                    curPg -= 1
                    curPt -= 1

            short_sequence = bits_sequence[:10] + '...' + bits_sequence[-10:]
            window['-sequence-'].update(f'Последовательность: {short_sequence}')

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


