import datetime
import logging
import re

import withQ.libs.constants.const as c
import withQ.libs.constants.regex as regex


def deadline_time(deadline_time: str, now_datetime: datetime.datetime) -> tuple[float, str, bool]:
    """
    締め切りまでの残り時間を秒単位で計算し、締め切り文字列をフォーマットします。

    Args:
        deadline_time: 締め切り時間文字列 (例: "HH:MM", "YYYY-MM-DD HH:MM", "YYYY/MM/DD HH:MM")
        now_datetime: 現在の日時オブジェクト

    Returns:
        以下のタプルを返す:
            - total_seconds: 締め切りまでの残り秒数
            - deadline_time: "締め切り:" プレフィックス付きのフォーマット済み締め切り文字列
            - is_deadline: 締め切りが過ぎている場合は True、それ以外の場合は False
    """

    try:
        # 締め切り時間形式の妥当性をチェック
        if not re.match(regex.DATETIME_TYPE, deadline_time):
            return 0.0, deadline_time, False

        # 一致したフォーマットに基づいて時間要素を抽出
        if re.match(regex.TIME, deadline_time):
            time_in_seconds = datetime.datetime(
                now_datetime.year, now_datetime.month, now_datetime.day,
                int(deadline_time.split(":")[0]), int(
                    deadline_time.split(":")[1])
            )
        elif re.match(regex.DATETIME, deadline_time):
            time_in_datetime = datetime.datetime.strptime(
                deadline_time, "%Y-%m-%d %H:%M")
        else:  # regex.YEARDATETIME
            time_in_datetime = datetime.datetime.strptime(
                deadline_time, "%Y/%m/%d %H:%M")

        # 締め切りステータスと残り秒数を計算
        if time_in_seconds >= now_datetime or time_in_datetime >= now_datetime:
            deadline_time = f"{c.DEADLINE_TEXT}: {deadline_time}"
            time_delta = (time_in_seconds if re.match(
                regex.TIME, deadline_time) else time_in_datetime) - now_datetime
            total_seconds = time_delta.total_seconds()
            is_deadline = True
            return total_seconds, deadline_time, is_deadline

        return 0.0, deadline_time, False

    except Exception as e:
        logging.error(f'Error: {e}')
        return 0.0, deadline_time, False
