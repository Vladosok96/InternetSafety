import PySimpleGUI as sg
import DES
import struct


layout = [[sg.Text('Шифрование DES-EEE3', font=("Helvetica", 14))],
          [sg.Text('Файл:'), sg.FileBrowse(button_text='Выбрать файл', key='-encode_browse-')],
          [sg.Text('Пароль:'), sg.Input(key='-encode_password-')],
          [sg.SaveAs('Зашифровать в', file_types=(("ALL Files", "*.des"),), change_submits=True, key='-encode_into-')],
          [sg.HorizontalSeparator(), sg.Button()],
          [sg.Text('Дешифрование', font=("Helvetica", 14))],
          [sg.Text('Файл:'), sg.FileBrowse(button_text='Выбрать файл', key='-decode_browse-')],
          [sg.Text('Пароль:'), sg.Input(key='-decode_password-')],
          [sg.SaveAs('Расшифровать в', file_types=(("ALL Files", "*.* *"),), change_submits=True, key='-decode_into-')]]


if __name__ == '__main__':

    window = sg.Window('Шифрование файлов алгоритмом DES', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            runGame = False
            break

        # Запуск алгоритма шифрования
        if event == '-encode_into-':
            filename = values['-encode_browse-']
            password = values['-encode_password-']

            file_blocks = []
            output_file_blocks = []

            # Чтение файла и разделение на блоки по 64 бит
            f = open(filename, 'rb')
            while True:
                file_block = f.read(8)
                if len(file_block) == 0:
                    break
                if len(file_block) < 8:
                    file_block += b'\x00' * (8 - len(file_block))
                int_file_block = struct.unpack('Q', file_block)[0]
                file_blocks.append(int_file_block)
            f.close()

            # Чтение пароля перевод в 7-ми байтовое число
            password = bytes(password[:7], 'utf-8')
            int_password = int.from_bytes(password, 'big')

            # Применение функции шифрования DES на каждый блок в отдельности (ECB)
            for block in file_blocks:
                encrypted_block = DES.DES(block, int_password, DES.ENCRYPTION)
                output_file_blocks.append(encrypted_block)

            # Вывод в файл
            f = open(values['-encode_into-'], 'wb')
            for block in output_file_blocks:
                packed_data = struct.pack('Q', block)
                f.write(packed_data)
            f.close()
            print(f"saved to: {values['-encode_into-']}")

        # Запуск алгоритма дешифрования
        if event == '-decode_into-':
            filename = values['-decode_browse-']
            password = values['-decode_password-']

            file_blocks = []
            output_file_blocks = []

            # Чтение файла и разделение на блоки по 64 бит
            f = open(filename, 'rb')
            while True:
                file_block = f.read(8)
                if len(file_block) == 0:
                    break
                if len(file_block) < 8:
                    file_block += b'\x00' * (8 - len(file_block))
                int_file_block = struct.unpack('Q', file_block)[0]
                file_blocks.append(int_file_block)
            f.close()

            # Чтение пароля перевод в 7-ми байтовое число
            password = bytes(password[:7], 'utf-8')
            int_password = int.from_bytes(password, 'big')

            # Применение функции дешифрования DES на каждый блок в отдельности (ECB)
            for block in file_blocks:
                encrypted_block = DES.DES(block, int_password, DES.DECRYPTION)
                output_file_blocks.append(encrypted_block)

            # Вывод в файл
            f = open(values['-decode_into-'], 'wb')
            for block in output_file_blocks:
                packed_data = struct.pack('Q', block)
                f.write(packed_data)
            f.close()
            print(f"saved to: {values['-decode_into-']}")
