import datetime
import re

import libs.constants.const as c
import libs.constants.regex as regex


def deadline_time(deadline_time: str, setting_param: str, now_datetime: datetime, is_deadline: bool):
    if deadline_time == "":
        if re.match(regex.TIME, str(setting_param)) != None:
            time_in_seconds = datetime.datetime.strptime(
                str(now_datetime.year) + str(now_datetime.month) + str(now_datetime.day) + setting_param.replace(':', ''), "%Y%m%d%H%M")
            if time_in_seconds >= now_datetime:
                deadline_time = c.DEADLINE_TEXT + ': ' + setting_param
                time_delta = time_in_seconds - now_datetime
                total_seconds = time_delta.total_seconds()
                is_deadline = True
                return total_seconds, deadline_time, is_deadline

        if re.match(regex.DATETIME, str(setting_param)) != None:
            time_in_datetime = datetime.datetime.strptime(
                str(now_datetime.year) + setting_param.replace('/', '').replace(':', ''), "%Y%m%d%H%M")
            if time_in_datetime >= now_datetime:
                deadline_time = c.DEADLINE_TEXT + ': ' + setting_param
                time_delta = time_in_datetime - now_datetime
                total_seconds = time_delta.total_seconds()
                is_deadline = True
                return total_seconds, deadline_time, is_deadline

        if re.match(regex.YEARDATETIME, str(setting_param)) != None:
            time_in_datetime = datetime.datetime.strptime(
                setting_param.replace('/', '').replace(':', ''), "%Y%m%d%H%M")
            if time_in_datetime >= now_datetime:
                deadline_time = c.DEADLINE_TEXT + ': ' + setting_param
                time_delta = time_in_datetime - now_datetime
                total_seconds = time_delta.total_seconds()
                is_deadline = True
                return total_seconds, deadline_time, is_deadline
