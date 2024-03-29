from typing import Union


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: Union[int, float],
                 distance: Union[int, float],
                 speed: Union[int, float],
                 calories: Union[int, float],
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Получить данные о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000.
    LEN_STEP: float = 0.65
    MIN_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: Union[int, float],
                 weight: Union[int, float],
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> Union[int, float]:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> Union[int, float]:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> Union[int, float]:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1 = 18.
    COEFF_CALORIE_2 = 20.

    def get_spent_calories(self) -> Union[int, float]:
        """Получить количество затраченных калорий при беге."""
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                 - self.COEFF_CALORIE_2)
                * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_3: float = 0.035
    COEFF_CALORIE_4 = 2.
    COEFF_CALORIE_5: float = 0.029

    def __init__(self,
                 action: int,
                 duration: Union[int, float],
                 weight: Union[int, float],
                 height: Union[int, float],
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight
                         )
        self.height = height

    def get_spent_calories(self) -> Union[int, float]:
        """Получить количество затраченных калорий при спортивной ходьбе."""
        return ((self.COEFF_CALORIE_3 * self.weight
                + ((self.get_mean_speed() ** self.COEFF_CALORIE_4)
                 // self.height)
                * self.COEFF_CALORIE_5 * self.weight)
                * self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_CALORIE_4 = 2.
    COEFF_CALORIE_6: float = 1.1

    def __init__(self,
                 action: int,
                 duration: Union[int, float],
                 weight: Union[int, float],
                 length_pool: Union[int, float],
                 count_pool: float,
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight
                         )
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> Union[int, float]:
        """Получить среднюю скорость движения при плвании."""
        return (self.length_pool
                * self.count_pool / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> Union[int, float]:
        """Получить количество затраченных калорий при плавании."""
        return ((self.get_mean_speed() + self.COEFF_CALORIE_6)
                * self.COEFF_CALORIE_4
                * self.weight
                )


SPORT = {'SWM': Swimming,
         'RUN': Running,
         'WLK': SportsWalking
         }


def read_package(workout_type: str, data: list) -> Union[Training, None]:
    """Прочитать данные полученные от датчиков."""
    if workout_type in SPORT:
        return SPORT[workout_type](*data)
    return None


def main(training: Union[Training, None]) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
