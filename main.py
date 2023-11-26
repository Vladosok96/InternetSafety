import PySimpleGUI as sg
from DES import DES


layout = [[sg.Text('Шифрование DES-EEE3', font=("Helvetica", 14))],
          [sg.Text('Файл:'), sg.FileBrowse(button_text='Выбрать файл', key='-encode_browse-')],
          [sg.Text('Пароль:'), sg.Input(key='-encode_password-')],
          [sg.SaveAs('Зашифровать в', file_types=(("ALL Files", "*.des"),), change_submits=True, key='-encode_into-')],
          [sg.HorizontalSeparator(), sg.Button()],
          [sg.Text('Дешифрование', font=("Helvetica", 14))]]


if __name__ == '__main__':

    window = sg.Window('Шифрование файлов алгоритмом DES', layout)

    while True:
        event, values = window.read()

        print(event, values)

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
            while f.readable():
                file_block = f.read(8)
                if len(file_block) == 0:
                    break
                if len(file_block) < 8:
                    file_block += b'\x00' * (8 - len(file_block))
                int_file_block = int.from_bytes(file_block, 'big')
                file_blocks.append(int_file_block)
            f.close()

            # Чтение пароля перевод в 7-ми байтовое число
            password = bytes(password[:7], 'utf-8')
            int_password = int.from_bytes(password, 'big')
            print(len(bin(int_password)) - 2, bin(int_password))

            # Применение функции шифрования DES на каждый блок в отдельности (ECB)
            for block in file_blocks:
                encrypted_block = DES(block, int_password)
                output_file_blocks.append(encrypted_block)

            # Вывод в файл
            output_array = b''
            for block in output_file_blocks:
                for _ in range(8):
                    output_array += bytes([block & 0xFF])
                    block = block >> 8
            f = open(values['-encode_into-'], 'wb')
            f.write(output_array)
            f.close()


        # Запуск алгоритма дешифрования
        if event == 'Дешифровать':
            filename = values[3]
            password = values[4]
