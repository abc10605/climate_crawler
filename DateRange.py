import datetime
from dateutil.relativedelta import relativedelta


class DayRange(object):
    def __init__(self, first, last):
        self.__oneDay = datetime.timedelta(days=1)
        self.__curr = first.toPyDate()
        self.__term = last.toPyDate()
        self.__term += self.__oneDay

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.__curr >= self.__term:
            raise StopIteration()
        (cur, self.__curr) = (self.__curr, self.__curr + self.__oneDay)
        return str(cur)


class MonthRange(object):
    def __init__(self, first, last):
        self.__oneMonth = relativedelta(months=1)
        self.__curr = first.toPyDate()
        self.__term = last.toPyDate()
        self.__term += self.__oneMonth

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.__curr >= self.__term - self.__oneMonth:
            raise StopIteration()
        (cur, self.__curr) = (self.__curr, self.__curr + self.__oneMonth)
        return str(cur)[:7]
