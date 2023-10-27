import random
from abc import ABC

"""Я оставил некоторые "тестовые" функции, чтобы в случае необходимости можно было не сложно проверить
поведение программы в том или ином сценарии. Данные функции не требуются в ходе выполнения программы, они
использовались лишь для ее отладки. По-хорошему можно было бы сделать отдельный класс Shoot, но как же мне 
не хочется переделывать половину программы..."""


class PlayerBase(ABC):
    def __init__(self, nickname='', is_human=True):
        self._nickname = nickname
        self._is_human = is_human
        self._ships = []
        self._one_deck_ship_count = 4
        self._two_deck_ship_count = 2
        self._three_deck_ship_count = 1
        self._max_score = self.calculate_max_score()
        self._ships_to_place = [
            ("Крейсер", 3, self._three_deck_ship_count),  # Тип, размер, максимальное количество
            ("Эсминец", 2, self._two_deck_ship_count),
            ("Катер", 1, self._one_deck_ship_count)
        ]
        self._ship_type_counters = {ship_type: 0 for ship_type, _, _ in self._ships_to_place}
        self._ships_field = ShipsField(self._ships, self._nickname)
        self._shoots_field = ShootsField(self._ships, self._nickname)
        self._score = 0
        self._is_ready = False

    def calculate_max_score(self):
        """Вычисляет максимальное количество очков для игрока в зависимости от типов кораблей"""
        one_deck_score = self._one_deck_ship_count
        two_deck_score = self._two_deck_ship_count * 2
        three_deck_score = self._three_deck_ship_count * 3
        return one_deck_score + two_deck_score + three_deck_score

    def setup_ships(self):
        """Размещает корабли выборочным способом на игровом поле."""
        while not self._is_ready:

            way = self.input_menu_choice(["Автоматическая случайная расстановка", "Ручная расстановка"],
                                         "Каким способом хотите расставить корабли?")
            if way == 1:
                self.setup_ships_automatically()

            elif way == 2:
                self.setup_ships_manually()

            else:
                print("Ошибка в выборе меню")

    def setup_ships_manually(self):
        """Ручная расстановка кораблей"""
        while not self._is_ready:
            choice = self.input_menu_choice(
                ["Катер (4 шт)", "Эсминец (2 шт)", "Крейсер (1 шт)", "Назад (к выбору способа расстановки)",
                 "Готово", "Сбросить", "Текущее положение кораблей"], "Какой тип корабля хотите расположить?")

            # Катера
            if choice == 1:
                if self._one_deck_ship_count > 0:
                    ship_name = input("Введите название корабля: ")
                    ship = Ship(self._ships_field, ship_name, 1)
                    ship.place_ship()
                    self.add_ship(ship)
                    self._one_deck_ship_count -= 1
                else:
                    print("Вы уже разместили все катера. Попробуйте другой тип корабля.")

            # Эсминцы
            elif choice == 2:
                if self._two_deck_ship_count > 0:
                    ship_name = input("Введите название корабля: ")
                    ship = Ship(self._ships_field, ship_name, 2)
                    ship.place_ship()
                    self.add_ship(ship)
                    self._two_deck_ship_count -= 1
                else:
                    print("Вы уже разместили все эсминцы. Попробуйте другой тип корабля.")

            # Крейсеры
            elif choice == 3:
                if self._three_deck_ship_count > 0:
                    ship_name = input("Введите название корабля: ")
                    ship = Ship(self._ships_field, ship_name, 3)
                    ship.place_ship()
                    self.add_ship(ship)
                    self._three_deck_ship_count -= 1
                else:
                    print("Вы уже разместили все крейсеры. Попробуйте другой тип корабля.")

            elif choice == 4:
                self.reset_ships_placement()  # Сбросить корабли
                break

            elif choice == 5:
                if self.check_all_ships_are_placed():
                    print("Вы успешно разместили все корабли!")
                    self._is_ready = True
                else:
                    print("Не все корабли были размещены. Размещайте и приходите снова!")

            elif choice == 6:
                self.reset_ships_placement()  # Сбросить корабли

            elif choice == 7:
                self.show_both_fields()

            else:
                print("Некорректный выбор, попробуйте ещё раз.")

    def check_all_ships_are_placed(self):
        return self._one_deck_ship_count == 0 and self._two_deck_ship_count == 0 and self._three_deck_ship_count == 0

    def reset_ships_placement(self):
        self._one_deck_ship_count = 4
        self._two_deck_ship_count = 2
        self._three_deck_ship_count = 1
        self._ships_to_place = [
            ("Крейсер", 3, self._three_deck_ship_count),
            ("Эсминец", 2, self._two_deck_ship_count),
            ("Катер", 1, self._one_deck_ship_count)
        ]
        self._ship_type_counters = {ship_type: 0 for ship_type, _, _ in self._ships_to_place}
        self._ships_field.reset_field()
        self._ships.clear()
        self._is_ready = False

    def setup_ships_automatically(self):
        """Размещает корабли автоматическим способом на игровом поле."""
        while not self._is_ready:
            self.reset_ships_placement()
            for ship_type, ship_size, max_count in self._ships_to_place:

                # Разместить корабли данного типа
                for i in range(max_count):
                    ship_name = f"{ship_type} {self._nickname} №{i + 1}"
                    ship = Ship(self._ships_field, ship_name, ship_size)
                    if not ship.place_ship_randomly():
                        break
                    self.add_ship(ship)

                    # Увеличиваем счетчик для данного типа кораблей
                    self._ship_type_counters[ship_type] += 1

            # Если все корабли успешно размещены
            if all(self._ship_type_counters[ship_type] == max_count for ship_type, _, max_count in self._ships_to_place):
                print(f"\x1B[3m{self._nickname}\x1B[0m. Корабли успешно размещены!")
                if self._is_human:
                    choice = self.input_menu_choice(["Да", "Нет"], "Желаете отобразить ваше игровое поле?")
                    if choice == 1:
                        print("Текущее расположение кораблей:")
                        self._ships_field.show_field()

                    self._is_ready = True
                else:
                    self._is_ready = True
                    # self.show_both_fields()
            else:
                print("Невозможно расставить все корабли. Перегенерация...")
                continue

    @staticmethod
    def input_menu_choice(menu_items: list, prompt: str):
        """Отображение пунктов меню с возвратом выбранного пункта.

        :param menu_items: Список из пунктов меню
        :param prompt: Заголовок меню
        :return: Выбранный пункт меню
        """
        while True:
            try:
                print(prompt)
                for index, item in enumerate(menu_items, 1):
                    print(f"{index} - {item}")
                choice = int(input())

                if 1 <= choice <= len(menu_items):
                    return choice
                else:
                    print("Некорректный выбор. Попробуйте ещё раз.")
            except ValueError:
                print("Ошибка. Введите число.")

    def check_all_ships_are_sunk(self):
        if all(ship.get_is_sunk() for ship in self._ships):
            return True
        return False

    def shoot(self, target_player):
        """Производит выстрел по другому игроку и обновляет игровые поля.

        :param target_player: Поле соперника
        """
        pass

    def show_both_fields(self):
        """Показывает поле кораблей и поле выстрелов игрока."""
        ships_field_data = self._ships_field.get_field()
        shoots_field_data = self._shoots_field.get_field()

        _field_size = self._ships_field.get_field_size()

        print(f"Поле игрока \x1B[3m{self.get_nickname(): <14}\x1B[0m|", end='  ')
        print(f"  Поле выстрелов игрока \x1B[3m{self.get_nickname()}\x1B[0m:")
        print('  |', *[f'{i} |' for i in range(1, _field_size + 1)], end='')
        print('       ', *[f'{i} |' for i in range(1, _field_size + 1)])

        for x in range(1, _field_size + 1):
            print(x, end=' | ')
            for y in range(_field_size):
                ship_cell_status = ships_field_data[x - 1][y]
                if ship_cell_status == 0:
                    print("O |", end=' ')  # Корабля нет
                elif ship_cell_status == 1:
                    print("■ |", end=' ')  # Корабль цел
                elif ship_cell_status == 2:
                    print("X |", end=' ')  # Корабль подбит
                elif ship_cell_status == 3:
                    print("T |", end=' ')  # Промах
                else:
                    print("E |", end=' ')  # Error

            # print(" ", end=' ')

            print('  ', x, end=' | ')

            for y in range(_field_size):
                shoot_cell_status = shoots_field_data[x - 1][y]
                if shoot_cell_status == 0:
                    print("O |", end=' ')  # Корабля нет
                elif shoot_cell_status == 1:
                    print("■ |", end=' ')  # Корабль цел
                elif shoot_cell_status == 2:
                    print("X |", end=' ')  # Корабль подбит
                elif shoot_cell_status == 3:
                    print("T |", end=' ')  # Промах
                else:
                    print("E |", end=' ')  # Error

            print()

    def get_nickname(self):
        return self._nickname

    def add_ship(self, ship):
        self._ships.append(ship)

    def get_is_human(self):
        return self._is_human

    def get_ships(self):
        return self._ships

    def get_max_score(self):
        return self._max_score

    def get_score(self):
        return self._score

    def get_ships_field(self):
        return self._ships_field

    def get_shoots_field(self):
        return self._shoots_field

    def __str__(self):
        return f"{self._nickname}. Очки: {self._score}/{self._max_score}"


class Player(PlayerBase):
    def shoot(self, target_player):
        print(f"Выстрел игрока '{self._nickname}'. ")
        while True:
            self.show_both_fields()
            try:
                x = int(input("Введите № строки: ")) - 1
                y = int(input("Введите № столбцы: ")) - 1
                if not self._is_ready:
                    print("Вы не готовы к стрельбе, так как не разместили корабли.")
                    return

                # Проверяем, может ли игрок стрелять в данные координаты
                if not self._ships_field.is_valid_coordinate(x, y):
                    print("Некорректные координаты для стрельбы. Попробуйте снова.")
                    continue

                # Проверяем, не стреляли ли уже в эти координаты
                if self._shoots_field.get_field()[x][y] in [2, 3]:
                    print("Вы уже стреляли в эти координаты. Попробуйте снова.")
                    continue

                # Получаем поле цели (target_player._ships_field) и проверяем, было ли попадание
                if target_player.get_ships_field().is_overlap(x, y):
                    print(f"Попадание! {self._nickname} ходит снова!")
                    target_player.get_ships_field().update_field(x, y, 2)  # Помечаем на поле цели, что попали
                    self._shoots_field.update_field(x, y, 2)  # Помечаем на своем поле, что попали
                    self._score += target_player.get_ships_field().check_sinking_score()
                    # target_player._ships_field.show_ships()
                    if target_player.check_all_ships_are_sunk():
                        return
                    continue

                else:
                    print(f"{self._nickname}. Мимо!")
                    target_player.get_ships_field().update_field(x, y, 3)  # Помечаем на поле цели, что мимо
                    self._shoots_field.update_field(x, y, 3)  # Помечаем на своем поле, что мимо
                    # target_player._ships_field.show_ships()

                    return

            except ValueError:
                print("Неверный выбор. Введите цифру.")

            except Exception as e:
                print(f"Произошла ошибка в shoot: {e}")


class Computer(PlayerBase):
    def __init__(self, nickname):
        super().__init__(nickname, is_human=False)
        self.last_hit_coordinates = None
        self.hit_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.shoot_directions_available = self.hit_directions.copy()
        self.saved_direction = None
        self.shoot_direction = ()
        self.coordinates_available = []
        for row in range(self._ships_field.get_field_size()):
            for col in range(self._ships_field.get_field_size()):
                self.coordinates_available.append((row, col))

    def shoot(self, target_player):
        """Выстрелы на рандом."""
        while True:
            try:
                x, y = self.get_random_coordinates()

                if not self._is_ready:
                    print(f"{self._nickname}, вы не готовы к стрельбе, так как не разместили корабли.")
                    return

                # Проверяем, может ли игрок стрелять в данные координаты
                if not self._ships_field.is_valid_coordinate(x, y):
                    continue

                # Проверяем, не стреляли ли уже в эти координаты
                if self._ships_field.get_field()[x][y] in [2, 3]:
                    continue

                # Получаем поле цели (target_player._ships_field) и проверяем, было ли попадание
                if target_player.get_ships_field().is_overlap(x, y):
                    print(f"Попадание! {self._nickname} ходит снова!")
                    target_player.get_ships_field().update_field(x, y, 2)  # Помечаем на поле цели, что попали
                    self._shoots_field.update_field(x, y, 2)  # Помечаем на своем поле, что попали
                    self._score += target_player.get_ships_field().check_sinking_score()
                    target_player.get_ships_field().show_field()
                    if target_player.check_all_ships_are_sunk():
                        return
                    continue

                else:
                    print(f"{self._nickname}. Мимо!")
                    target_player.get_ships_field().update_field(x, y, 3)  # Помечаем на поле цели, что мимо
                    self._shoots_field.update_field(x, y, 3)  # Помечаем на своем поле, что мимо
                    return

            except Exception as e:
                print(f"Произошла ошибка в shoot_automatically: {e}")

    def shoot_smart(self, target_player):
        while True:
            try:
                if not self._is_ready:
                    print(f"{self._nickname}, вы не готовы к стрельбе, так как не разместили корабли.")
                    return

                # Если было попадание по кораблю предыдущим выстрелом
                if self.last_hit_coordinates:
                    # print(f'Функция попадания для {self._nickname}')
                    if not self.shoot_directions_available:
                        self.last_hit_coordinates = None
                        self.saved_direction = None
                        self.shoot_directions_available = self.hit_directions.copy()
                        continue

                    if not self.saved_direction:
                        self.shoot_direction = random.choice(self.shoot_directions_available)
                        self.shoot_directions_available.remove(self.shoot_direction)
                    else:
                        self.shoot_direction = self.saved_direction

                    dx, dy = self.shoot_direction
                    # print(f"Выбранное направление: {dx, dy}")
                    x, y = self.last_hit_coordinates
                    # print(f"Координаты последнего попадания: {x, y}")
                    x, y = x + dx, y + dy
                    if (x, y) not in self.coordinates_available:
                        # print(f'{self.coordinates_available}')
                        # print(f"Координаты недоступны, перерасчет...")
                        self.saved_direction = None
                        # self.show_both_fields()
                        continue

                    # Если можно выстрелить
                    if (self._ships_field.is_valid_coordinate(x, y)
                            and self._shoots_field.get_field()[x][y] not in [2, 3]):

                        # Если попали
                        if target_player.get_ships_field().is_overlap(x, y):
                            print(f"Попадание! {self._nickname} ходит снова!")
                            self.remove_coordinates(x, y)
                            self.saved_direction = self.shoot_direction
                            target_player.get_ships_field().update_field(x, y, 2)
                            self._shoots_field.update_field(x, y, 2)
                            self._score += target_player.get_ships_field().check_sinking_score()
                            target_player.get_ships_field().show_field()

                            # Проверка затонул ли в этих координатах корабль
                            if any(ship.check_is_sunk_ship_coordinates(x, y) for ship in
                                   target_player.get_ships_field().get_ship_list()):
                                self.reset_shoot()
                                continue

                            if target_player.check_all_ships_are_sunk():
                                return
                            self.last_hit_coordinates = x, y
                            continue

                        # Если промахнулись
                        else:
                            print(f"{self._nickname}. Мимо!")
                            target_player.get_ships_field().update_field(x, y, 3)
                            self._shoots_field.update_field(x, y, 3)
                            self.saved_direction = None
                            if (x, y) in self.coordinates_available:
                                self.remove_coordinates(x, y)
                            self.last_hit_coordinates = None
                            return

                    # Если что-то пошло не так - сброс текущего выстрела
                    else:
                        self.reset_shoot()
                        continue

                # Если последнего попадания не было
                else:
                    # print(f'Функция когда нет попадания для {self._nickname}')

                    x, y = random.choice(self.coordinates_available)
                    # print(f"Текущие координаты: {x, y}")

                    # Если попали
                    if target_player.get_ships_field().is_overlap(x, y):
                        print(f"Попадание! {self._nickname} ходит снова!")
                        target_player.get_ships_field().update_field(x, y, 2)
                        self._shoots_field.update_field(x, y, 2)
                        self._score += target_player.get_ships_field().check_sinking_score()
                        # self.show_both_fields()
                        self.remove_coordinates(x, y)
                        # print(self.coordinates_available)
                        if target_player.check_all_ships_are_sunk():
                            return

                        # Если после попадания корабль затонул
                        if any(ship.check_is_sunk_ship_coordinates(x, y) for ship in
                               target_player.get_ships_field().get_ship_list()):

                            # Удаляем из списка доступных координат координаты близ "потопившего" выстрела,
                            # если координаты валидны
                            if ((self._ships_field.is_valid_coordinate(x, y + 1)
                                 and self._ships_field.get_field()[x][y + 1] not in [2, 3])
                                    and (x, y) in self.coordinates_available):
                                self.remove_coordinates(x, y + 1)
                            if (self._ships_field.is_valid_coordinate(x, y - 1)
                                    and self._ships_field.get_field()[x][y - 1] not in [2, 3]
                                    and (x, y) in self.coordinates_available):
                                self.remove_coordinates(x, y - 1)
                            if (self._ships_field.is_valid_coordinate(x - 1, y)
                                    and self._ships_field.get_field()[x - 1][y] not in [2, 3]
                                    and (x, y) in self.coordinates_available):
                                self.remove_coordinates(x - 1, y)
                            if (self._ships_field.is_valid_coordinate(x + 1, y)
                                    and self._ships_field.get_field()[x + 1][y] not in [2, 3]
                                    and (x, y) in self.coordinates_available):
                                self.remove_coordinates(x + 1, y)
                            continue

                        self.last_hit_coordinates = x, y
                        continue

                    else:
                        print(f"{self._nickname}. Мимо!")
                        target_player.get_ships_field().update_field(x, y, 3)
                        self._shoots_field.update_field(x, y, 3)
                        self.remove_coordinates(x, y)
                        return
            except Exception as e:
                print(f'Произошла ошибка в shoot_smart: {e}')

    def get_random_coordinates(self):
        return (random.randint(0, self._ships_field.get_field_size() - 1),
                random.randint(0, self._ships_field.get_field_size() - 1))

    def remove_coordinates(self, x, y):
        self.coordinates_available.remove((x, y))

    def reset_shoot(self):
        """Сброс координаты последнего попадания, сохраненного направления и списка доступных направлений"""
        self.last_hit_coordinates = None
        self.saved_direction = None
        self.shoot_directions_available = self.hit_directions.copy()


class Ship:
    def __init__(self, ships_field, name, length: int):
        self._ships_field = ships_field
        self._name = name
        self._length = length
        self._coordinates = []
        self._is_sunk = False

    def place_ship(self):
        coordinates_to_add = []
        while True:
            try:
                x = int(input(f"Введите № строки для корабля {self._name}: ")) - 1
                y = int(input(f"Введите № столбца для корабля {self._name}: ")) - 1

                if (not self._ships_field.is_valid_coordinate(x, y) or self._ships_field.is_overlap(x, y)
                        or not self._ships_field.is_nearby_ships(x, y)):
                    print("Ошибка. Возможно, координата уже занята, выходит за границу или рядом есть корабль.")
                    continue  # Перезапустить цикл, чтобы пользователь ввел координаты заново

                direction = self.choose_direction()
                temp_coordinates_to_add = []

                # Постепенно добавляем координаты корабля в зависимости от выбранного направления
                for i in range(self._length):
                    current_x, current_y = x, y
                    if direction == 1:  # Вверх
                        current_x = x - i
                    elif direction == 2:  # Вправо
                        current_y = y + i
                    elif direction == 3:  # Вниз
                        current_x = x + i
                    elif direction == 4:  # Влево
                        current_y = y - i

                    if (not self._ships_field.is_valid_coordinate(current_x, current_y)
                            or self._ships_field.is_overlap(current_x, current_y)
                            or not self._ships_field.is_nearby_ships(current_x, current_y)):
                        print(
                            "Ошибка при добавлении координат. Возможно, координата уже занята или выходит за границу.")
                        break

                    temp_coordinates_to_add.append(Coordinate(current_x, current_y))

                # Итоговая проверка
                else:
                    if len(temp_coordinates_to_add) != self._length:
                        self.rollback_coordinates(temp_coordinates_to_add)  # Откатываем некорректные координаты

                        # Можно было бы перезапустить расстановку, но по ТЗ нужно использовать raise
                        raise ValueError("Количество координат не соответствует длине корабля")

                    self._coordinates.extend(temp_coordinates_to_add)  # Добавляем координаты к кораблю

                    for coordinate in temp_coordinates_to_add:
                        self._ships_field.update_field(coordinate.get_coordinate_x(), coordinate.get_coordinate_y(), 1)

                    coordinates_to_add.extend(temp_coordinates_to_add)
                    self._ships_field.add_ship(self)  # Добавляем корабль в список кораблей поля
                    break

            except ValueError:
                print("Некорректный ввод. Введите целое число.")

        print(f"Корабль '{self._name}' успешно размещен! Текущее расположение кораблей: ")
        self._ships_field.show_field()

    def place_ship_randomly(self):
        max_attempts = 50  # Ограничение на количество попыток
        try:
            for _ in range(max_attempts):
                x = random.randint(0, self._ships_field.get_field_size() - 1)
                y = random.randint(0, self._ships_field.get_field_size() - 1)
                direction = random.randint(1, 4)  # Случайное направление

                # Проверяем, что корабль может быть размещен в заданных координатах
                if self.can_place_ship(x, y, direction):
                    self._coordinates = []  # Сбрасываем текущие координаты корабля

                    for i in range(self._length):
                        current_x, current_y = x, y
                        if direction == 1:  # Вверх
                            current_x = x - i
                        elif direction == 2:  # Вправо
                            current_y = y + i
                        elif direction == 3:  # Вниз
                            current_x = x + i
                        elif direction == 4:  # Влево
                            current_y = y - i

                        self._coordinates.append(Coordinate(current_x, current_y))
                        self._ships_field.update_field(current_x, current_y, 1)

                    self._ships_field.add_ship(self)  # Добавляем корабль в список кораблей поля
                    return True

                # Если нельзя разместить, то повторяем попытку
                else:
                    continue

            return False

        except Exception as e:
            print(f'Произошла ошибка в place_ship_randomly: {e}')

    def can_place_ship(self, x, y, direction):
        """Проверка на возможность разместить корабль в заданном направлении"""
        for i in range(self._length):
            current_x, current_y = x, y
            if direction == 1:  # Вверх
                current_x = x - i
            elif direction == 2:  # Вправо
                current_y = y + i
            elif direction == 3:  # Вниз
                current_x = x + i
            elif direction == 4:  # Влево
                current_y = y - i

            if (not self._ships_field.is_valid_coordinate(current_x, current_y)
                    or self._ships_field.is_overlap(current_x, current_y)
                    or not self._ships_field.is_nearby_ships(current_x, current_y)):
                return False

        return True

    @staticmethod
    def choose_direction():
        while True:
            print("Выберите направление для корабля:")
            print("1 - Вверх")
            print("2 - Вправо")
            print("3 - Вниз")
            print("4 - Влево")
            choice = input("Введите номер направления: ")
            if choice in ("1", "2", "3", "4"):
                return int(choice)
            else:
                print("Некорректный выбор. Попробуйте ещё раз.")

    def rollback_coordinates(self, coordinates_to_remove):
        for coordinate in coordinates_to_remove:
            self._coordinates.remove(coordinate)
            # Обнуляем координату, так как корабль не был размещен
            self._ships_field.update_field(coordinate.get_coordinate_x(), coordinate.get_coordinate_y(), 0)

    def get_ship_coordinates(self):
        return [[coordinate.get_coordinate_x(), coordinate.get_coordinate_y()] for coordinate in self._coordinates]

    def check_is_sunk_ship_coordinates(self, x, y):
        """Проверяет потоплен ли корабль в данных координатах"""
        return any([coord.get_coordinate_x() == x and coord.get_coordinate_y() == y for coord in
                    self._coordinates]) if self._is_sunk else False

    def get_name(self):
        return self._name

    def get_length(self):
        return self._length

    def get_coordinates(self):
        return self._coordinates

    def get_is_sunk(self):
        return self._is_sunk

    def __str__(self):
        coordinates_str = ', '.join(
            [f'({coord.get_coordinate_x()} {coord.get_coordinate_y()})' for coord in self._coordinates])
        return (
            f"Корабль: {self._name}. Длина: {self._length}, координаты: {coordinates_str}, "
            f"потоплен: {self._is_sunk}")


class Field(ABC):
    def __init__(self, ship_list, nickname):
        self._ship_list = ship_list
        self._nickname = nickname
        self._field_size = 6
        self._field = [[0 for _ in range(self._field_size)] for _ in range(self._field_size)]

    def show_field(self):
        print(f"Поле игрока \x1B[3m{self._nickname}\x1B[0m:")  # Курсивное имя игрока
        print('  |', *[f'{i} |' for i in range(1, self._field_size + 1)])
        for x in range(1, self._field_size + 1):
            print(x, end=' | ')
            for y in range(self._field_size):
                cell_status = self._field[x - 1][y]
                if cell_status == 0:
                    print("O |", end=' ')  # Корабля нет
                elif cell_status == 1:
                    print("■ |", end=' ')  # Корабль цел
                elif cell_status == 2:
                    print("X |", end=' ')  # Корабль подбит
                elif cell_status == 3:
                    print("T |", end=' ')  # Промах
                else:
                    print("E |", end=' ')  # Error
            print()

    def update_field(self, x, y, value):
        self._field[x][y] = value

    def add_ship(self, ship):
        self._ship_list.append(ship)

    def get_field(self):
        """Значения клеток:
        0: Корабля нет
        1: Корабль цел
        2: Корабль подбит
        3: Промах
        """
        return self._field

    def get_ship_list(self):
        return self._ship_list

    def get_field_size(self):
        return self._field_size


class ShipsField(Field):
    def __init__(self, ship_list, nickname):
        super().__init__(ship_list, nickname)
        self._ship_list = ship_list

    def check_sinking_score(self) -> int:
        earned_score = 0

        for ship in self._ship_list:
            if all(self._field[coord.get_coordinate_x()][coord.get_coordinate_y()] == 2 for coord in
                   ship.get_coordinates()) and not ship._is_sunk:
                print(f"Корабль '{ship.get_name()}' потоплен!")
                ship._is_sunk = True
                earned_score += ship.get_length()
                print(f"Получено {earned_score} очков")

        return earned_score

    def update_field(self, x, y, value):
        self._field[x][y] = value

    def show_ships(self):
        print(*[ship for ship in self._ship_list])

    def is_valid_coordinate(self, x, y):
        """Проверка нв выход за границы поля"""
        return 0 <= x < self._field_size and 0 <= y < self._field_size

    def is_overlap(self, x, y):
        """Проверка на наличие корабля в данных координатах"""
        return self._field[x][y] == 1  # Если 1, значит, уже есть корабль

    def is_nearby_ships(self, x, y):
        """"Проверяет, чтобы корабли были расположены на расстоянии друг от друга"""
        for ship in self._ship_list:
            for coordinate in ship.get_coordinates():
                if abs(coordinate.get_coordinate_x() - x) <= 1 and abs(coordinate.get_coordinate_y() - y) <= 1:
                    return False
        return True

    def reset_field(self):
        """Сбрасываем поле до начального состояния"""
        self._field = [[0 for _ in range(self._field_size + 1)] for _ in range(self._field_size + 1)]
        self._ship_list = []


class ShootsField(Field):
    def __init__(self, ship_list, nickname):
        super().__init__(ship_list, nickname)


class Coordinate:
    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y

    def get_coordinate(self):
        return self.__x, self.__y

    def get_coordinate_x(self):
        """Возвращает x."""
        return self.__x

    def get_coordinate_y(self):
        """Возвращает y."""
        return self.__y

    def __str__(self):
        return f'({self.__x} {self.__y})'


class Game:
    def __init__(self):
        self.__player = Player('Игрок')
        self.__computer = Computer('Компьютер')
        self.__player_list = [self.__player, self.__computer]
        self.__current_player = self.__player_list[0]

    def start(self):
        """Запуск игры."""
        # Разместить корабли на игровых полях
        self.__player.setup_ships()
        self.__computer.setup_ships_automatically()

        while not self.is_game_over():
            if self.__current_player.get_is_human():
                self.__current_player.shoot(self.__player_list[self.__player_list.index(self.__current_player) - 1])
            else:
                self.__current_player.shoot_smart(
                    self.__player_list[self.__player_list.index(self.__current_player) - 1])

            if self.is_game_over():
                break
            self.__current_player = self.__player_list[self.__player_list.index(self.__current_player) - 1]

    def is_game_over(self):
        for player in self.__player_list:
            if player.get_score() == player.get_max_score():
                print(f"Победил {player.get_nickname()}! Заработано {player.get_score()} очков!")
                print("Ваше итоговое поле:")
                player.show_both_fields()
                return True
            else:
                continue


if __name__ == '__main__':
    while True:
        game = Game()
        game.start()

        # После завершения игры спрашиваем пользователя о повторной игре
        play_again = input("Хотите сыграть ещё раз? (y/n): ")
        if play_again.lower() not in ['да', 'y', 'у']:
            break
