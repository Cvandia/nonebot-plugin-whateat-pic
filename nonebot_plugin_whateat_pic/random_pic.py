import secrets
from pathlib import Path
from typing import Literal

from .config import config


def random_pic(menu_type: Literal["drink", "eat"]) -> tuple[Path, str]:
    """
    随机获取一张图片
    """
    if menu_type not in ["drink", "eat"]:
        raise ValueError("menu_type must be 'drink' or 'eat'")

    menu_dir = Path(config.whatpic_res_path) / f"{menu_type}_pic"
    pic_list = [entry.name for entry in menu_dir.iterdir() if entry.is_file()]

    pic_name = secrets.choice(pic_list)
    pic_path = Path(config.whatpic_res_path) / f"{menu_type}_pic" / pic_name
    return pic_path, pic_name.split(".")[0]
