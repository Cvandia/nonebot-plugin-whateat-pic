from nonebot import require

require("nonebot_plugin_alconna")
require("nonebot_plugin_apscheduler")

from nonebot.plugin import PluginMetadata, inherit_supported_adapters
from . import matcher, config, check_on_statup


__plugin_meta__ = PluginMetadata(
    name="今天吃什么（图片版）",
    description="随机发送吃的或者喝的图片",
    usage="""
    今天吃什么
    今天喝什么
    添加菜单
    删除菜单
    查看菜单
    """,
    homepage = "https://github.com/Cvandia/nonebot-plugin-whateat-pic",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna")
)