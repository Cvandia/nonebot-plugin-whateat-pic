import time

from nonebot.adapters import Event

from .config import config

cd = config.whateat_cd
max_count = config.whateat_max


def check_iscd(last_time: float) -> tuple[bool, float, float]:
    """
    判断是否在冷却时间内

    Args:
        last_time(float): 上次使用时间

    Returns:
        - tuple[bool, float, float]: 是否在冷却时间内, 剩余冷却时间, 当前时间
    """
    now_time = time.time()
    if now_time - last_time < cd:
        return True, cd - (now_time - last_time), last_time
    return False, 0, now_time


def check_ismax(message: Event, user_count: dict) -> tuple[bool, dict]:
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
    return True, user_count
