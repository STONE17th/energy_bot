from datetime import date


class Day:
    def __init__(self, number: int | None = None, training: bool = False, payment: int | None = None):
        self.number = number
        self.training = training
        self.payment = payment


class Month:
    month_name = {
        1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь',
        7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
    }

    def __init__(self, str_date: str, training_days: list[int], payment_days: list[tuple[int, int]]):
        self.year, self.month = list(map(int, str_date.split('-')))
        self.name = Month.month_name[self.month]
        self._first_day = date(self.year, self.month, 1).weekday()
        self._training_days = training_days
        self._payment_days = {day[0]: day[1] for day in payment_days}

    @property
    def days(self):
        list_days = []
        total_days = self._max_days + self._first_day
        for i in range(total_days + (7 - total_days % 7) * bool(total_days % 7)):
            number = i - self._first_day + 1
            if 0 <= number - 1 < self._max_days:
                list_days.append(Day(number, number in self._training_days, self._payment_days.get(number, None)))
            else:
                list_days.append(Day())
        return list_days

    @property
    def _max_days(self) -> int:
        month_day = {
            1: 31, 2: 29 if self._is_leap() else 28, 3: 31, 4: 30, 5: 31, 6: 30,
            7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }
        return month_day[self.month]

    def _is_leap(self) -> bool:
        return not self.year % 4 and self.year % 100 or not self.year % 400

    def __repr__(self):
        return ' -> '.join(
            [f'{day.number} {"T" if day.training else ""} {day.payment if day.payment else ""}' for day in self.days])
