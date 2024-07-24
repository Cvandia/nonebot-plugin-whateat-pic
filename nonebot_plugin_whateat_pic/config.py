from typing import Optional
from nonebot import get_driver

'''
解决pydantic v2 无法获取配置的问题
'''
class Config():
    def __init__(self):
        try:
            self.whateat_cd = get_driver().config.whateat_cd
        except:
            self.whateat_cd = 10
        try:
            self.whateat_max  = get_driver().config.whateat_max
        except:
            self.whateat_max = 0

config = Config()