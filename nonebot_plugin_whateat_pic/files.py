from pathlib import Path

from nonebot.log import logger

from .config import config


def resolve_pic_path(img_type: str, name: str) -> Path:
    """
    解析菜品图片的绝对路径，并确保结果始终位于资源目录内。

    Args:
        img_type(str): 图片类型, 只能是 eat 或 drink
        name(str): 菜品或饮品的名字

    Returns:
        - Path: 图片的绝对路径

    Raises:
        ValueError: img_type 或 name 非法, 或者解析后的路径逃逸出资源目录
    """
    if img_type not in ["eat", "drink"]:
        raise ValueError("img_type must be 'eat' or 'drink'")

    # 拒绝路径分隔符、上级目录、Windows 驱动器/流分隔符和空字节
    if not name or name in [".", ".."]:
        raise ValueError("name must not be empty or a relative path segment")
    if any(sep in name for sep in ["/", "\\", ":", "\0"]):
        raise ValueError("name must not contain path separators")

    pic_dir = (Path(config.whatpic_res_path) / f"{img_type}_pic").resolve()

    # 校验链接目标，但保留原始文件目录项，避免删除别名时误删原图
    pic_path = pic_dir / (name + ".jpg")
    if not pic_path.resolve().is_relative_to(pic_dir):
        raise ValueError("name must not escape the resource directory")
    return pic_path


def save_pic(img: bytes, img_type: str, name: str) -> None:
    """
    保存图片
    """
    if not isinstance(img, bytes):
        logger.error(f"img must be bytes, but got {type(img)}")
        raise TypeError("img must be bytes")
    save_path = resolve_pic_path(img_type, name)
    with Path.open(save_path, "wb") as f:
        f.write(img)


def delete_pic(img_type: str, name: str) -> None:
    """
    删除图片
    """
    delete_path = resolve_pic_path(img_type, name)
    if delete_path.exists():
        try:
            delete_path.unlink()
        except OSError as e:
            logger.error(f"Error: {e}")
            raise
    else:
        raise FileNotFoundError(f"{delete_path} not found")
