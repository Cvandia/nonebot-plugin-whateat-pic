from nonebot import require
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require("nonebot_plugin_alconna")
require("nonebot_plugin_apscheduler")

from . import check_on_statup as _
from . import matcher as _  # noqa

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
    type="application",
    homepage="https://github.com/Cvandia/nonebot-plugin-whateat-pic",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
)
