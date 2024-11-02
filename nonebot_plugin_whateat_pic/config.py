from nonebot import get_driver
from nonebot import logger
# from .check_on_statup import check_resource
import asyncio

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
        try:
            self.whatpic_res_path = get_driver().config.whatpic_res_path
        except:
            self.whatpic_res_path = "./data/whateat_pic"

config = Config()

# driver = get_driver()
# @driver.on_startup
# async def _():
#     logger.info("正在检查资源文件……")
#     asyncio.create_task(check_resource())
    