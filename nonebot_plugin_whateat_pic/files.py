from pathlib import Path
from typing import Literal
from nonebot_plugin_alconna.uniseg import Image
from .config import config

def save_pic(img: Image, type: Literal['drink','eat'], name:str) -> None:
    """
    保存图片
    """
    save_path = Path(config.whatpic_res_path) / f"{type}_pic" / name
    if isinstance(img, bytes):
        with open(save_path, "wb") as f:
            f.write(img)
def delete_pic(type: Literal['drink','eat'], name: str) -> None:
    """
    删除图片
    """
    delete_path = Path(config.whatpic_res_path) / f"{type}_pic" / name
    if delete_path.exists():
        delete_path.unlink()
    else:
        raise FileNotFoundError(f"{delete_path} not found")