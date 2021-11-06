class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
        self.massage = (f'Тип тренировки: {training_type}; '   # Шаблон для вывода сообщения в терминал
                        f'Длительность: {duration:.3f} ч.; '
                        f'Дистанция: {distance:.3f} км; '
                        f'Ср. скорость: {speed:.3f} км/ч; '
                        f'Потрачено ккал: {calories:.3f}.'
                        )

    def get_message(self) -> str:
        """Возвращает шаблон для вывода сообщения в терминал."""
        return self.massage


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65   # Расстояние за один шаг
    M_IN_KM = 1000    # Константа для перевода значений из метров в километры

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        massage = InfoMessage(
            self.__class__.__name__,    # Получение имени класса
            self.duration,              # Получение расстояния из класса
            self.get_distance(),        # Полечение дистанции из класса
            self.get_mean_speed(),      # Получение средней скорости из класса
            self.get_spent_calories()   # Получение затраченных каллорий из класса
        )
        return massage


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """Получаем величину затраченных калорий (бег)"""
        coeff_1 = 18   # Коээфицент каллорий 1
        coeff_2 = 20   # Коээфицент каллорий 2
        calories: float = (coeff_1 * self.get_mean_speed() - coeff_2) * self.weight / self.M_IN_KM * self.duration * 60
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)   # Наследование функциональности конструктора класса-родителя
        self.height = height   # Добавление новой функции

    def get_spent_calories(self) -> float:
        """Получаем величину затраченных калорий (ходьба)"""
        coeff_1 = 0.035   # Коээфицент каллорий 1
        coeff_2 = 2       # Коээфицент каллорий 2
        coeff_3 = 0.029   # Коээфицент каллорий 3
        calories: float = (coeff_1 * self.weight + (self.get_mean_speed()**coeff_2 // self.height) *
                           coeff_3 * self.weight) * self.duration * 60
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38   # # Расстояние за один гребок

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)   # Наследование функциональности конструктора класса-родителя
        self.length_pool = length_pool   # Добавление новой функции
        self.count_pool = count_pool     # Добавление новой функции

    def get_mean_speed(self) -> float:
        """Получаем величину средней скорости для плавания"""
        speed = self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получаем величину затраченных калорий (плавание)"""
        coeff_1 = 1.1   # Коээфицент каллорий 1
        coeff_2 = 2     # Коээфицент каллорий 2
        calories: float = (self.get_mean_speed() + coeff_1) * coeff_2 * self.weight
        return calories

    def get_distance(self) -> float:
        """Получаем дистанцию плавания"""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_workout_type = {'SWM': Swimming,       # Словарь, где в значении указан класс тренировки
                         'RUN': Running,
                         'WLK': SportsWalking
                         }
    training_class = dict_workout_type[workout_type]
    return training_class(*data)
    # Возвращает обьект соответствующего класса со значениями, указанными в списке data


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = Training.show_training_info(training)
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)