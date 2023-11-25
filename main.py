import PySimpleGUI as sg
from DES import DES


layout = [[sg.Text('Шифрование DES-EEE3', font=("Helvetica", 14))],
          [sg.Text('Файл:'), sg.FileBrowse(button_text='Выбрать файл', key='-encode_browse-')],
          [sg.Text('Пароль:'), sg.Input(key='-encode_password-')],
          [sg.Button('Зашифровать')],
          [sg.HorizontalSeparator()],
          [sg.Text('Дешифрование', font=("Helvetica", 14))]]


if __name__ == '__main__':

    window = sg.Window('Шифрование файлов алгоритмом DES', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            runGame = False
            break

        # Запуск алгоритма шифрования
        if event == 'Зашифровать':
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

            # Применение функции шифрования DES на каждый блок в отдельности (ECB)
            for block in file_blocks:
                encrypted_block = DES(block, password)
                output_file_blocks.append(encrypted_block)

        # Запуск алгоритма дешифрования
        if event == 'Дешифровать':
            filename = values[3]
            password = values[4]
