from datetime import datetime, timedelta
from itertools import chain
import re

class TimeFormatter:
    def __init__(self, timestr):
        self.timestr = timestr
        self.cur_time = datetime.now()
        self.white_list = ['auto', '']

        self.remove_non_digits()
        self.auto_complete()
        self.time_format_checker()

    def format_time(self):
        time = self.timestr
        year = time[0:4]
        month = time[4:6]
        day = time[6:8]
        hour = time[8:10]
        minute = time[10:12]
        return f'{year}-{month}-{day} {hour}:{minute}'

    def parse_time(self):
        if self.timestr and len(self.timestr) == 12:
            return datetime.strptime(self.timestr, "%Y%m%d%H%M")
        else:
            return None

    def auto_complete(self):
        time = self.timestr

        # 如果是auto，直接当前时间往后一小时安排任务
        if time == 'auto' or time == '':
            target_time = self.cur_time + timedelta(hours=1)
            self.timestr = self.convert_datetime_to_timestr(target_time)
            return

        year = str(datetime.now().year)
        month = ('0' + str(datetime.now().month))[-2:]
        day = ('0' + str(datetime.now().day))[-2:]
        minute = '00'

        try:
            if len(time) == 2:
                hour = time
            elif len(time) == 3:
                hour = '0' + time[0]
                minute = time[1:3]
            elif len(time) == 4:
                hour = time[0:2]
                minute = time[2:4]
            elif len(time) == 7:
                month = time[0:2]
                day = time[2:4]
                hour = '0' + time[4]
                minute = time[5:7]
            elif len(time) == 8:
                month = time[0:2]
                day = time[2:4]
                hour = time[4:6]
                minute = time[6:8]
            elif len(time) == 11:
                year = time[0:4]
                month = time[4:6]
                day = time[6:8]
                hour = '0' + time[8]
                minute = time[9:11]
            else:
                year = time[0:4]
                month = time[4:6]
                day = time[6:8]
                hour = time[8:10]
                minute = time[10:12]
        except Exception as e:
            print(e)
            self.timestr = None
            return

        self.timestr = f'{year}{month}{day}{hour}{minute}'

    @staticmethod
    def convert_datetime_to_timestr(datetime_value):
        return datetime_value.strftime('%Y%m%d%H%M')

    def remove_non_digits(self):

        weekdays = {
            "Monday": ["Monday", "Mon"],
            "Tuesday": ["Tuesday", "Tue", "Tues"],
            "Wednesday": ["Wednesday", "Wed"],
            "Thursday": ["Thursday", "Thu", "Thur", "Thurs"],
            "Friday": ["Friday", "Fri"],
            "Saturday": ["Saturday", "Sat"],
            "Sunday": ["Sunday", "Sun"]
        }

        if self.timestr in self.white_list:
            return
        elif 'today' in self.timestr:
            cur_date = self.cur_time.strftime('%Y%m%d')
            self.timestr = self.timestr.replace('today', cur_date)
        elif 'tomorrow' in self.timestr:
            tomorrow_date = (self.cur_time + timedelta(days=1)).strftime('%Y%m%d')
            self.timestr = self.timestr.replace('tomorrow', tomorrow_date)
        elif any(word.lower() in self.timestr.lower() for word in chain.from_iterable(weekdays.values())):
            found_weekday = None
            for weekday, aliases in weekdays.items():
                for alias in aliases:
                    if alias.lower() in self.timestr.lower():
                        found_weekday = weekday
                        matched_alis = alias
                        break

                if found_weekday:
                    break

            if found_weekday:
                target_weekday = list(weekdays.keys()).index(found_weekday)

                days_ahead = (target_weekday - self.cur_time.weekday()) % 7
                if days_ahead == 0:
                    days_ahead = 7

                next_date = (datetime.today() + timedelta(days=days_ahead)).strftime('%Y%m%d')
                self.timestr = self.timestr.replace(matched_alis, next_date)
        elif match := re.search(r'in \d+ day(s?)', self.timestr):
            days = int(match.group(0).split()[1])
            next_date = (datetime.today() + timedelta(days=days)).strftime('%Y%m%d')
            self.timestr = self.timestr.replace(match.group(0), next_date)


        self.timestr = ''.join(i for i in self.timestr if i.isdigit())

    def time_format_checker(self):
        try:
            datetime.strptime(self.timestr, '%Y%m%d%H%M')
        except Exception as e:
            print(e)
            self.timestr = None


if __name__ == '__main__':
    time_formatter = TimeFormatter('202201300000')
    print(time_formatter.format_time())
    print(time_formatter.parse_time())
    print(time_formatter.auto_complete())
    print(time_formatter.convert_datetime_to_timestr(datetime.now()))
