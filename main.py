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
          [sg.Text('Результат: ', key='-same_bits-')],
          [sg.Button('Запуск', key="-begin_same_bits-")],
          [sg.HorizontalSeparator()],
          [sg.Text('Тест на произвольные отклонения')],
          [sg.Text('Результат: ', key='-deviation-')],
          [sg.Button('Запуск', key="-begin_deviation-")],
         ]


if __name__ == '__main__':

    # Общие переменные
    bits_sequence = ''

    window = sg.Window('Тестирование псевдослучайных последовательностей', layout)

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