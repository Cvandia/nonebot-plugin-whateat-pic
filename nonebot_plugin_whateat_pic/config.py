from nonebot.plugin import get_plugin_config
from pydantic import BaseModel

"""
解决pydantic v2 无法获取配置的问题
"""


class Config(BaseModel):
    whateat_cd: int = 10
    whateat_max: int = 0
    whatpic_res_path: str = "./data/whateat_pic"


config = get_plugin_config(Config)
