import datetime
import re

import components.constants.regex as regex
import components.constants.const as c

# import constants.regex as regex


def deadline_time(deadline_time: str, setting_param: str, now_datetime: datetime, is_deadline: bool):
    print("aa")
    if deadline_time == "":
        if re.match(regex.TIME, str(setting_param)) != None:
            time_in_seconds = datetime.datetime.strptime(
                str(now_datetime.year) + str(now_datetime.month) + str(now_datetime.day) + setting_param.replace(':', ''), "%Y%m%d%H%M")
            print(time_in_seconds)
            if time_in_seconds >= now_datetime:
                deadline_time = c.DEADLINE + ': ' + setting_param
                time_delta = time_in_seconds - now_datetime
                total_seconds = time_delta.total_seconds()
                print(total_seconds)
                is_deadline = True
                return total_seconds, deadline_time, is_deadline
        if re.match(regex.DATETIME, str(setting_param)) != None:
            print(setting_param.replace('/', '').replace(':', ''))
            time_in_datetime = datetime.datetime.strptime(
                str(now_datetime.year) + setting_param.replace('/', '').replace(':', ''), "%Y%m%d%H%M")
            print(time_in_datetime)
            if time_in_datetime >= now_datetime:
                deadline_time = c.DEADLINE + ': ' + setting_param
                time_delta = time_in_datetime - now_datetime
                total_seconds = time_delta.total_seconds()
                print(total_seconds)
                is_deadline = True
                return total_seconds, deadline_time, is_deadline
        if re.match(regex.YEARDATETIME, str(setting_param)) != None:
            time_in_datetime = datetime.datetime.strptime(
                setting_param.replace('/', '').replace(':', ''), "%Y%m%d%H%M")
            print(time_in_datetime)
            if time_in_datetime >= now_datetime:
                deadline_time = c.DEADLINE + ': ' + setting_param
                time_delta = time_in_datetime - now_datetime
                total_seconds = time_delta.total_seconds()
                print(total_seconds)
                is_deadline = True
                return total_seconds, deadline_time, is_deadline
