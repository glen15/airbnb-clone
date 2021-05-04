# calendar.py  로 이름만들지 말것

import calendar


class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.day_names = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
        self.months = (
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        days = []
        for week in weeks:
            for (
                day,
                _,
            ) in week:  # for 다음 변수 두개넣어서 튜플로 된 애를 앞 뒤 하나 씩 따로 변수받아냄( _ 는 무시하라는 뜻)
                days.append(day)

        return days

    def get_month(self):
        return self.months[self.month - 1]
