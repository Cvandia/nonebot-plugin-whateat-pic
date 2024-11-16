from pathlib import Path
from nonebot.log import logger
from .config import config


def save_pic(img: bytes, img_type: str, name: str) -> None:
    """
    保存图片
    """
    save_path = Path(config.whatpic_res_path) / f"{img_type}_pic" / (name + ".jpg")
    if isinstance(img, bytes):
        with open(save_path, "wb") as f:
            f.write(img)
    else:
        logger.error(f"img must be bytes, but got {type(img)}")
        raise TypeError("img must be bytes")


def delete_pic(img_type: str, name: str) -> None:
    """
    删除图片
    """
    delete_path = Path(config.whatpic_res_path) / f"{img_type}_pic" / (name + ".jpg")
    if delete_path.exists():
        try:
            delete_path.unlink()
        except OSError:
            logger.error(f"delete {delete_path} failed")
            raise Exception(f"delete {delete_path} failed")
