# Установить бит в 1
def set_bit(number: int, bit_position: int, value: int):
    if value:
        return number | (1 << bit_position)
    else:
        return number & ~(1 << bit_position)


# Прочитать значение бита (0 или 1)
def read_bit(number: int, bit_position: int):
    return (number >> bit_position) & 1
