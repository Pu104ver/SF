def show_field(field):
    for row in field:
        print(*row, sep=' | ', end=' |\n')


def check_win(field, player_symbol):
    for row in field:
        if all(value == player_symbol for value in row[1:]):
            print(f'Победа {player_symbol}-ов!')
            return True

    for col in range(1, 4):
        if all(row[col] == player_symbol for row in field[1:]):
            print(f'Победа {player_symbol}-ов!')
            return True

    if all(field[i][i] == player_symbol for i in range(1, 4)) or \
            all(field[i][4 - i] == player_symbol for i in range(1, 4)):
        print(f'Победа {player_symbol}-ов!')
        return True

    if all(value != '-' for row in field for value in row):
        print('Ничья! Игра окончена.')
        return True

    return False


def update_field(field, moves_hash, turn_to_go):
    while True:
        try:
            x, y = map(int, input(f'''Куды ходим, {turn_to_go[0]}? Напиши в формате "строка столбец": ''').split())
            if 1 <= x <= 3 and 1 <= y <= 3:
                if (x, y) not in moves_hash:
                    if turn_to_go[0] == 'Крестики':
                        field[x][y] = 'X'
                    else:
                        field[x][y] = 'O'

                    moves_hash[(x, y)] = True
                    if check_win(field, field[x][y]):
                        return False
                else:
                    print("Эта позиция уже занята. Выбери другую позицию.")
                    continue
            else:
                print("Координаты выходят за границы допустимого диапазона (1-3). Попробуйте снова.")
                continue

            turn_to_go = turn_to_go[::-1]
            show_field(field)
        except ValueError:
            print("Введи два целых числа через пробел.")
            continue


def play_game():
    field = [
        [' ', 1, 2, 3],
        [1, '-', '-', '-'],
        [2, '-', '-', '-'],
        [3, '-', '-', '-'],
    ]
    turn_to_go = ['Крестики', 'Нолики']
    show_field(field)
    moves_hash = {}
    while True:
        if not update_field(field, moves_hash, turn_to_go):
            break

    print('Конечное поле:')
    show_field(field)
    print()
    play_again = input("Хотите сыграть ещё раз? (Y/N): ")
    if play_again.lower() != 'y':
        return False
    return True


if __name__ == '__main__':
    while True:
        if not play_game():
            break
