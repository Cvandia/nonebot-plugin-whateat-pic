from typing import Literal
from pathlib import Path
from .config import config

import random
import os


def random_pic(menu_type: Literal["drink", "eat"]) -> tuple[Path, str]:
    """
    随机获取一张图片
    """
    if menu_type == "drink":
        pic_list = os.listdir(config.whatpic_res_path + "/drink_pic")
    elif menu_type == "eat":
        pic_list = os.listdir(config.whatpic_res_path + "/eat_pic")
    else:
        raise ValueError("menu_type must be 'drink' or 'eat'")

    pic_name = random.choice(pic_list)
    pic_path = Path(config.whatpic_res_path) / f"{menu_type}_pic" / pic_name
    return pic_path, pic_name.split(".")[0]
