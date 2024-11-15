import time
from .config import config
from typing import Tuple
from nonebot.adapters import Event

cd = config.whateat_cd
max_count = config.whateat_max


def check_iscd(last_time: int) -> Tuple[bool, int, int]:
    """
    判断是否在冷却时间内

    Args:
        last_time(int): 上次使用时间

    Returns:
        - tuple[bool, int, int]: 是否在冷却时间内, 剩余时间, 当前时间
    """
    now_time = int(time.time())
    delta_time = now_time - last_time
    if delta_time < cd:
        return True, cd - delta_time, now_time
    else:
        return False, 0, now_time


def check_ismax(message: Event, user_count: dict) -> Tuple[bool, dict]:
    """
    判断是否达到最大次数

    Args:
        message(Event): 消息事件
        user_count(dict): 用户使用次数记录

    Returns:
        - tuple[bool, dict]: 是否达到最大次数, 用户使用次数记录
    """
    user_id = message.get_user_id()
    if max_count == 0:
        return False, {}
    if user_id not in user_count:
        user_count[f"{user_id}"] = 0
    if user_count[f"{user_id}"] < max_count:
        user_count[f"{user_id}"] += 1
        return False, user_count
    else:
        return True, user_count
