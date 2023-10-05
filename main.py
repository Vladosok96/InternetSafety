import PySimpleGUI as sg
from random import choice
import math


layout = [[sg.Text('Длина последовательности:'), sg.Slider(orientation='h', range=(1000, 100000), resolution=1000, default_value=1000)],
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
          [sg.Button('Запуск', key="-begin_deviation-")],
         ]


def r(k, arr):
    if arr[k] != arr[k + 1]:
        return 1
    return 0


if __name__ == '__main__':

    # Общие переменные
    bits_sequence = ''

    window = sg.Window('Тестирование псевдослучайных последовательностей', layout, size=(600, 600))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            runGame = False
            break

        # Генерация последовательности нулей и единиц
        if event == 'Генерация':
            bits_sequence = ''
            for i in range(int(values[0])):
                bits_sequence += choice(['0', '1'])
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
            for i in range(3):
                for j in range(6):
                    if counter != 0:
                        Yj = abs(states[counter] - L)
                        Yj /= pow(2 * L * (4 * abs(counter) - 2), 0.5)
                        result += f'{counter}= {Yj:.2f}, '
                    counter += 1
                if i < 2:
                    result += '\n'
            window['-deviation_statistics-'].update(f'Статистики: {result}')


