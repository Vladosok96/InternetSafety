import PySimpleGUI as sg
import math


# Генератор BBS
def square_generator(length):
    bits_sequence = ''
    N = 65535
    d = 16311
    a = 11233
    c = 65537
    x1 = 169
    x2 = 0

    while len(bits_sequence) < length:
        x2 = (d * (x1 ** 2) + (a * x1) + c) % N
        x1 = x2
        bits_sequence += bin(x1)[2:]

    return bits_sequence[:length]


# Шифрующее преобразование ГОСТ 28147-89 в режиме простой замены
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


layout = [[sg.Text('Шифрование', font=("Helvetica", 14))],
          [sg.Text('Сообщение:'), sg.Input()],
          [sg.Text('Пароль:'), sg.Input()],
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
            password = values[1]

            M = []
            for n in range(math.ceil(len(password) / 32)):
                mn = bytes(password[n*32:(n+1)*32], 'utf-8')
                if len(mn) < 32:
                    mn += b'\x00' * (32 - len(mn))
                print(int.from_bytes(mn, byteorder='big'), len(mn) * 8, mn)
                M.append(int.from_bytes(mn, byteorder='big'))

            h = int(square_generator(256), 2)
            SUM = 0
            L = 0

            for i in range(len(M)):
                h = Ek(h, M[i])
                L += 256
                SUM += M[i]

            L += 256
            Mn = 0
            SUM += Mn

            output = h.to_bytes(32, 'big')
            print(h, len(output), output)

            h = f(h, Mn)
            h = f(h, L)
            h = f(h, SUM)

            output = h.to_bytes(32, 'big')
            print(h, len(output), output)

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



