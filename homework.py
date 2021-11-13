from typing import Dict, Type


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
        self.message = ('Тип тренировки: {}; '
                        'Длительность: {:.3f} ч.; '
                        'Дистанция: {:.3f} км; '
                        'Ср. скорость: {:.3f} км/ч; '
                        'Потрачено ккал: {:.3f}.'
                        )

    def get_message(self) -> str:
        """Возвращает шаблон для вывода сообщения в терминал."""
        return self.message.format(self.training_type, self.duration,
                                   self.distance, self.speed,
                                   self.calories)


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    minutes_in_hour = 60

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """Получаем величину затраченных калорий (бег)"""
        coeff_1 = 18
        coeff_2 = 20
        return ((coeff_1 * self.get_mean_speed() - coeff_2)
                * self.weight / self.M_IN_KM
                * self.duration * self.minutes_in_hour)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получаем величину затраченных калорий (ходьба)"""
        coeff_1 = 0.035
        coeff_2 = 2
        coeff_3 = 0.029
        return ((coeff_1 * self.weight
                 + (self.get_mean_speed() ** coeff_2
                    // self.height) * coeff_3 * self.weight)
                * self.duration * self.minutes_in_hour)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получаем величину средней скорости для плавания"""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получаем величину затраченных калорий (плавание)"""
        coeff_1 = 1.1   # Коээфицент каллорий 1
        coeff_2 = 2     # Коээфицент каллорий 2
        return ((self.get_mean_speed() + coeff_1) * coeff_2
                * self.weight)

    def get_distance(self) -> float:
        """Получаем дистанцию плавания"""
        return self.action * self.LEN_STEP / self.M_IN_KM


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_workout_type: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                    'RUN': Running,
                                                    'WLK': SportsWalking
                                                    }
    try:
        return dict_workout_type[workout_type](*data)
    except KeyError:
        print(f'{workout_type} - Incorrect type of training. '
              f'Workout types supported - Swimming (SWM), '
              f'Running (RUN), SportsWalking (WLK).')
        exit()
    except TypeError:
        print('Incorrect amount of data from sensors')
        exit()


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
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
