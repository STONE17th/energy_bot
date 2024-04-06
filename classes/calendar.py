from datetime import date


def _is_leap_year(year: int) -> bool:
    return not year % 4 and year % 100 or not year % 400


class TrainingMonth:
    def __init__(self, month_year: str, trainings_days: list[int]):
        year, month = list(map(int, month_year.split('-')))
        self.month = month
        self.year = year
        self.first_day = date(year, month, 1).weekday()
        self.trainings_days = self._fill_days(trainings_days)

    def _fill_days(self, trainings_days: list[int]):
        month = []
        days = [0] * self.first_day
        i = 1
        while i <= self.last_day:
            while len(days) < 7 and i <= self.last_day:
                mark = f'{i}_✅' if i in trainings_days else i
                days.append(mark)
                i += 1
            month.append(days)
            days = []
        while len(month[-1]) < 7:
            month[-1].append(0)
        return month

    @property
    def last_day(self):
        max_days = {1: 31, 2: 29 if _is_leap_year(self.year) else 28, 3: 31, 4: 30,
                    5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
        return max_days[self.month]
