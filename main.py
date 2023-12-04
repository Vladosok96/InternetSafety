import PySimpleGUI as sg
import struct
import ElGamal


layout = [[sg.Text('Шифрование Эль-Гамаля', font=("Helvetica", 16))],
          [sg.HorizontalSeparator()],
          [sg.Text('Генератор ключей', font=("Helvetica", 14))],
          [sg.Text('Открытый ключ:')],
          [sg.Text('Y:'), sg.Input(key='-key_y-')],
          [sg.Text('g:'), sg.Input(key='-key_g-')],
          [sg.Text('p:'), sg.Input(key='-key_p-')],
          [sg.Text('Закрытый ключ:')],
          [sg.Text('X:'), sg.Input(key='-key_x-')],
          [sg.Button('Сгенерировать ключи', key='-generate_key-')],
          [sg.HorizontalSeparator()],
          [sg.Text('Шифрование файла', font=("Helvetica", 14))],
          [sg.Text('Файл:'), sg.FileBrowse(button_text='Выбрать файл', key='-encode_browse-')],
          [sg.SaveAs('Зашифровать в', file_types=(("ElGamal Files", "*.eg"),), change_submits=True, key='-encode_into-')],
          [sg.HorizontalSeparator()],
          [sg.Text('Дешифрование файла', font=("Helvetica", 14))],
          [sg.Text('Файл:'), sg.FileBrowse(button_text='Выбрать файл', file_types=(("ElGamal Files", "*.eg"),), key='-decode_browse-')],
          [sg.SaveAs('Расшифровать в', file_types=(("ALL Files", "*.* *"),), change_submits=True, key='-decode_into-')]]


if __name__ == '__main__':

    window = sg.Window('Шифрование файлов алгоритмом Эль-Гамаля', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            runGame = False
            break

        # Запуск алгоритма генерации ключей
        if event == '-generate_key-':
            y, g, p, x = ElGamal.generate_key()
            window['-key_y-'].update(y)
            window['-key_g-'].update(g)
            window['-key_p-'].update(p)
            window['-key_x-'].update(x)

        # Запуск алгоритма шифрования
        if event == '-encode_into-':
            filename = values['-encode_browse-']
            y = int(values['-key_y-'])
            g = int(values['-key_g-'])
            p = int(values['-key_p-'])

            file_blocks = []
            output_file_blocks = []

            # Чтение файла и разделение на блоки по 128 бит
            f = open(filename, 'rb')
            while True:
                file_block = f.read(16)
                if len(file_block) == 0:
                    break
                if len(file_block) < 16:
                    file_block += b'\x00' * (16 - len(file_block))
                int_file_blocks_64 = struct.unpack('QQ', file_block)
                int_file_block_128 = (int_file_blocks_64[0] << 64) + int_file_blocks_64[1]
                file_blocks.append(int_file_block_128)
            f.close()

            # Применение функции шифрования ElGamal
            progress = 0
            for block in file_blocks:
                encrypted_block = ElGamal.encode(block, y, g, p)
                output_file_blocks.append(encrypted_block)
                progress += 1
                print(f'processing: {progress}/{len(file_blocks)}')

            # Вывод в файл
            f = open(values['-encode_into-'], 'wb')
            for block in output_file_blocks:
                for i in range(len(block)):
                    int_data_right = block[i] & 0xFFFFFFFFFFFFFFFF
                    int_data_left = block[i] >> 64
                    packed_data_left = struct.pack('Q', int_data_left)
                    packed_data_right = struct.pack('Q', int_data_right)
                    f.write(packed_data_left)
                    f.write(packed_data_right)
            f.close()
            print(f"saved to: {values['-encode_into-']}")

        # Запуск алгоритма дешифрования
        if event == '-decode_into-':
            filename = values['-decode_browse-']
            x = int(values['-key_x-'])
            p = int(values['-key_p-'])

            file_blocks = []
            output_file_blocks = []

            # Чтение файла и разделение на блоки по 64 бит
            f = open(filename, 'rb')
            while True:
                file_block = f.read(32)
                if len(file_block) == 0:
                    break
                if len(file_block) < 32:
                    file_block += b'\x00' * (32 - len(file_block))
                int_file_blocks_64 = struct.unpack('QQQQ', file_block)
                int_file_block_128_a = (int_file_blocks_64[0] << 64) + int_file_blocks_64[1]
                int_file_block_128_b = (int_file_blocks_64[2] << 64) + int_file_blocks_64[3]
                file_blocks.append((int_file_block_128_a, int_file_block_128_b))
            f.close()

            # Применение функции дешифрования ElGamal
            progress = 0
            for block in file_blocks:
                decrypted_block = ElGamal.decode(block, x, p)
                output_file_blocks.append(decrypted_block)
                progress += 1
                print(f'processing: {progress}/{len(file_blocks)}')

            # Вывод в файл
            f = open(values['-decode_into-'], 'wb')
            counter = 0
            for block in output_file_blocks:
                int_data_right = block & 0xFFFFFFFFFFFFFFFF
                int_data_left = block >> 64
                packed_data_left = struct.pack('Q', int_data_left)
                packed_data_right = struct.pack('Q', int_data_right)
                packed_data = packed_data_left + packed_data_right
                if counter == len(output_file_blocks) - 1:
                    while packed_data[-1] == 0:
                        packed_data = packed_data[:-1]
                f.write(packed_data)
                counter += 1
            f.close()
            print(f"saved to: {values['-decode_into-']}")
