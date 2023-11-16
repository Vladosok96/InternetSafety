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


# Шифрующее преобразование ГОСТ 28147-89 в режиме простой замены
def Ek(M_value, Key_value):

    h = 0
    for j in range(4):
        Si = (M_value >> (j * 64)) & 0xFFFFFFFF
        h = h << 64

        A0 = Si & 0xFFFF
        B0 = (Si >> 32) & 0xFFFF

        # Разделение 256-битного числа на 8 32-битных чисел
        K = []
        for i in range(0, 256, 32):
            K.append(((Key_value >> i) & 0xFFFF))

        # Создание нового списка из 32-битных чисел
        X = []

        # Добавление первых 24 чисел (циклическое повторение чисел K)
        for _ in range(3):
            X.extend(K)

        # Добавление оставшихся 8 чисел (числа K в обратном порядке)
        X.extend(reversed(K))

        A = [A0]
        B = [B0]

        for Xi in range(32):
            A.append(B[-1] ^ f(A[-1], X[Xi]))
            B.append(A[-2])

        A = A[1:]
        B = B[1:]

        h += (B[-1] << 32) | A[-1]

    h %= 2 ** 256

    return h


layout = [[sg.Text('Шифрование', font=("Helvetica", 14))],
          [sg.Text('Сообщение:'), sg.Input()],
          [sg.Text('Пароль:'), sg.Input()],
          [sg.Button('Зашифровать')],
          [sg.Text('Результат: '), sg.Input(disabled=True, key='-encryption-')],
          [sg.HorizontalSeparator()],
          [sg.Text('Дешифрование', font=("Helvetica", 14))],
          [sg.Text('Сообщение:'), sg.Input()],
          [sg.Text('Пароль:'), sg.Input()],
          [sg.Button('Дешифровать')],
          [sg.Text('Результат: '), sg.Input(disabled=True, key='-decryption-')],
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
            message = values[0]
            password = values[1]
            print(message)

            message_pieces = []
            for n in range(math.ceil(len(message) / 32)):
                mn = bytes(message[n*32:(n+1)*32], 'utf-8')
                if len(mn) < 32:
                    mn += b'\x00' * (32 - len(mn))
                # print(int.from_bytes(mn, byteorder='big'), len(mn) * 8, mn)
                message_pieces.append(int.from_bytes(mn, byteorder='big'))

            M = []
            for n in range(math.ceil(len(password) / 32)):
                mn = bytes(password[n*32:(n+1)*32], 'utf-8')
                if len(mn) < 32:
                    mn += b'\x00' * (32 - len(mn))
                # print(int.from_bytes(mn, byteorder='big'), len(mn) * 8, mn)
                M.append(int.from_bytes(mn, byteorder='big'))

            K = int(square_generator(256), 2)
            SUM = 0
            L = 0

            M_hash = []

            for i in range(len(M)):

                h = Ek(M[i], K)

                L += 256
                SUM += M[i]

                L += 256
                Mn = 0
                SUM += Mn

                h = Ek(h, Mn)
                h = Ek(h, L)
                h = Ek(h, SUM)

                M_hash.append(h)
                K = h

            print(M_hash)

            result_message = ''
            for i in range(len(message_pieces)):
                message_pieces[i] ^= M_hash[i]
                result_message += hex(message_pieces[i])[2:]

            window['-encryption-'].update(result_message)

            # output = h.to_bytes(32, 'big')
            # print(h, len(output), output)

        # Запуск алгоритма дешифрования
        if event == 'Дешифровать':
            message = values[3]
            password = values[4]

            message_pieces = []
            for n in range(math.ceil(len(message) / 32)):
                message_pieces.append(int(message[n*32:(n+1)*32], 16))

            M = []
            for n in range(math.ceil(len(password) / 32)):
                mn = bytes(password[n * 32:(n + 1) * 32], 'utf-8')
                if len(mn) < 32:
                    mn += b'\x00' * (32 - len(mn))
                # print(int.from_bytes(mn, byteorder='big'), len(mn) * 8, mn)
                M.append(int.from_bytes(mn, byteorder='big'))

            for i in range(len(message_pieces) - len(M)):
                M.append(0)

            K = int(square_generator(256), 2)
            SUM = 0
            L = 0

            M_hash = []

            for i in range(len(M)):
                h = Ek(M[i], K)

                L += 256
                SUM += M[i]

                L += 256
                Mn = 0
                SUM += Mn

                h = Ek(h, Mn)
                h = Ek(h, L)
                h = Ek(h, SUM)

                M_hash.append(h)
                K = h

            print(M_hash)

            result_message = ''
            for i in range(len(message_pieces)):
                message_pieces[i] ^= M_hash[i]
                result_message += hex(message_pieces[i])[2:]

            byte_object = bytes.fromhex(result_message)

            window['-decryption-'].update(byte_object.decode('utf-8'))

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



