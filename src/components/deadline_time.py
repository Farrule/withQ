import datetime
import logging
import re

from config.settings import env_c

def deadline_time(deadline_time_str: str, now_datetime: datetime.datetime) -> tuple[float, str, bool]:
    try:
        # 締め切り時間形式の妥当性をチェック
        if not re.match(env_c.DATETIME_TYPE, deadline_time_str):
            return 0.0, deadline_time_str, False

        time_in_datetime = None

        # 一致したフォーマットに基づいて時間要素を抽出
        if re.match(env_c.TIME, deadline_time_str):
            time_parts = deadline_time_str.split(":")
            time_in_datetime = datetime.datetime(
                now_datetime.year, now_datetime.month, now_datetime.day,
                int(time_parts[0]), int(time_parts[1])
            )
        elif re.match(env_c.DATETIME, deadline_time_str):
            time_in_datetime = datetime.datetime.strptime(
                deadline_time_str, "%m/%d/%H:%M")
            # 年がない場合は現在の年を補完
            time_in_datetime = time_in_datetime.replace(year=now_datetime.year)
        elif re.match(env_c.YEARDATETIME, deadline_time_str):
            time_in_datetime = datetime.datetime.strptime(
                deadline_time_str, "%Y/%m/%d/%H:%M")

        if time_in_datetime is None:
            return 0.0, deadline_time_str, False

        # 締め切りステータスと残り秒数を計算
        if time_in_datetime >= now_datetime:
            time_delta = time_in_datetime - now_datetime
            total_seconds = time_delta.total_seconds()
            return total_seconds, deadline_time_str, True

        return 0.0, deadline_time_str, False

    except Exception as e:
        logging.error(f'Error: {e}')
        return 0.0, deadline_time_str, False
