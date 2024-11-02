from nonebot import get_driver
from nonebot.adapters import Event
from nonebot.log import logger

from nonebot_plugin_alconna import on_alconna, Alconna, Args, AlconnaMatch, Match, Query
from nonebot_plugin_alconna.uniseg import UniMessage, Text, Image
from nonebot_plugin_alconna.uniseg.tools import image_fetch

from nonebot_plugin_apscheduler import scheduler

from .random_pic import random_pic
from .check_user_data import check_cd, check_max
from .menu import Menu
from .files import save_pic, delete_pic

import random
import io


NICKNAME = list(get_driver().config.nickname)
BOT_NAME = NICKNAME[0] if NICKNAME else "脑积水"

TIME = 0
USER_DATA = {}
MAX_MSG = [
    "你今天吃的够多了！不许再吃了(´-ωก`)",
    "吃吃吃，就知道吃，你都吃饱了！明天再来(▼皿▼#)",
    "(*｀へ´*)你猜我会不会再给你发好吃的图片",
    f"没得吃的了，{BOT_NAME}的食物都被你这坏蛋吃光了！",
    "你在等我给你发好吃的？做梦哦！你都吃那么多了，不许再吃了！ヽ(≧Д≦)ノ",
]

eat_pic_matcher = on_alconna(
    Alconna("今天吃什么"),
    use_cmd_start=True,
)

drink_pic_matcher = on_alconna(
    Alconna("今天喝什么"),
    use_cmd_start=True,
)

view_menu_matcher = on_alconna(
    Alconna("全部菜单", Args["type?", str]),
    use_cmd_start=True,
    aliases=("查看菜单", "查看菜品"),
)

add_menu_matcher = on_alconna(
    Alconna("添加菜单", Args["name?", str]["type?", str]["img?", Image]),
    use_cmd_start=True,
)

del_menu_matcher = on_alconna(
    Alconna("删除菜单", Args["name?", str]["type?", str]),
    use_cmd_start=True,
)


eat_pic_matcher.shortcut(
    r"^[今|明|后]?[天|日]?(早|中|晚)?(上|午|餐|饭|夜宵|宵夜)吃(什么|啥|点啥)$"
)
drink_pic_matcher.shortcut(
    r"^[今|明|后]?[天|日]?(早|中|晚)?(上|午|餐|饭|夜宵|宵夜)喝(什么|啥|点啥)$"
)


@eat_pic_matcher.handle()
async def handle_eat_pic(event: Event):
    global TIME, USER_DATA
    send_msg = UniMessage()
    send_msg.append(Text(f"{BOT_NAME}建议你吃："))
    send_msg.append(random_pic("eat"))
    await send_msg.finish(event)


@drink_pic_matcher.handle()
async def handle_drink_pic(event: Event):
    global TIME, USER_DATA
    check_result, remain_time, new_last_time = check_cd(TIME)
    check_max_result, USER_DATA = check_max(event, USER_DATA)
    if not check_result or not check_max_result:
        TIME = new_last_time
        await UniMessage.text(f"cd冷却中,还有{remain_time}秒").finish(
            event, at_sender=True
        )
        if not check_max_result:
            send_msg = UniMessage()
            send_msg.append(Text(f"{BOT_NAME}建议你喝："))
            send_msg.append(Image(raw=random_pic("drink")))
            await send_msg.finish(event)
        else:
            await UniMessage.text(random.choice(MAX_MSG)).finish(event, at_sender=True)


@eat_pic_matcher.handle()
async def handle_eat_pic_cd(event: Event):
    global TIME, USER_DATA
    check_result, remain_time, new_last_time = check_cd(TIME)
    check_max_result, USER_DATA = check_max(event, USER_DATA)
    if not check_result or not check_max_result:
        TIME = new_last_time
        await UniMessage.text(f"cd冷却中,还有{remain_time}秒").finish(
            event, at_sender=True
        )
        if not check_max_result:
            send_msg = UniMessage()
            send_msg.append(Text(f"{BOT_NAME}建议你吃："))
            send_msg.append(Image(raw=random_pic("eat")))
            await send_msg.finish(event)
        else:
            await UniMessage.text(random.choice(MAX_MSG)).finish(event, at_sender=True)


@view_menu_matcher.handle()
async def handle_view_menu(event: Event, type: Match[str]):
    if type.available:
        view_menu_matcher.set_path_arg("type", type.result)


@view_menu_matcher.got_path("type", prompt=f"请告诉{BOT_NAME}具体菜单类型吧")
async def _(event: Event, type: str):
    menu_type = type.strip()
    if menu_type in ["菜单", "菜品"]:
        menu_type = "eat"
    elif menu_type in ["饮料", "饮品"]:
        menu_type = "drink"
    else:
        await UniMessage.text("菜单类型错误，请重新输入").finish(event)

    try:
        menu = Menu(menu_type)
        send_msg_list = UniMessage()
        send_msg_list.append(Text("菜单如下："))
        for img in menu.draw_menu():
            img_bytesio = io.BytesIO()
            img.save(img_bytesio, format="JPEG")
            send_msg_list.append(Image(raw=img_bytesio))
    except OSError:
        await UniMessage.text("没有找到菜单，请稍后重试").finish(event)


@add_menu_matcher.handle()
async def _(event: Event, name: Match[str], type: Match[str], img: Match[Image]):
    if name.available:
        add_menu_matcher.set_path_arg("name", name.result)
    if img.available:
        add_menu_matcher.set_path_arg("img", img.result)
    if type.available:
        if type.result in ["菜单", "菜品"]:
            add_menu_matcher.set_path_arg("type", "eat")
        elif type.result in ["饮料", "饮品"]:
            add_menu_matcher.set_path_arg("type", "drink")
        else:
            await UniMessage.text("菜单类型错误，请重新输入").finish(event)


@add_menu_matcher.got_path("name", prompt=f"请告诉{BOT_NAME}具体菜名或者饮品名吧")
async def _(event: Event, name: str):
    if not name:
        await UniMessage.text("菜名不能为空，请重新输入").finish(event)


@add_menu_matcher.got_path("type", prompt=f"请告诉{BOT_NAME}具体菜单类型吧")
async def _(event: Event, type: str):
    if type in ["菜品", "菜单"]:
        add_menu_matcher.set_path_arg("type", "eat")
    elif type in ["饮料", "饮品"]:
        add_menu_matcher.set_path_arg("type", "drink")
    else:
        await UniMessage.text("菜单类型错误，请重新输入").finish(event)

@add_menu_matcher.got_path("img", prompt=f"请告诉{BOT_NAME}图片吧")
async def _(event: Event, img: Image, type: Match[str], name: Match[str]):
    if not img:
        await UniMessage.text("图片不能为空，请重新输入").finish(event)
    try:
        save_pic(img, type.result, name.result) # type: ignore
        await UniMessage.text(f"成功添加{name.result}").finish(event)
    except OSError:
        await UniMessage.text("添加失败，请稍后重试").finish(event)

@del_menu_matcher.handle()
async def _(event: Event, name: Match[str]):
    if name.available:
        del_menu_matcher.set_path_arg("name", name.result)

@del_menu_matcher.got_path("name", prompt=f"请告诉{BOT_NAME}具体菜名或者饮品名吧")
async def _(event: Event, name: str):
    if not name:
        await UniMessage.text("菜名不能为空，请重新输入").finish(event)

@del_menu_matcher.got_path("type", prompt=f"请告诉{BOT_NAME}具体菜单类型吧")
async def _(event: Event, type: str, name: Match[str]):
    if type in ["菜品", "菜单"]:
        del_menu_matcher.set_path_arg("type", "eat")
    elif type in ["饮料", "饮品"]:
        del_menu_matcher.set_path_arg("type", "drink")
    else:
        await UniMessage.text("菜单类型错误，请重新输入").finish(event)
    try:
        delete_pic(type, name.result) # type: ignore
        await UniMessage.text(f"成功删除{name.result}").finish(event)
    except FileNotFoundError:
        await UniMessage.text("删除失败，请稍后重试").finish(event)


# 每日8点清空用户数据
@scheduler.scheduled_job("cron", hour=8)
async def _():
    global USER_DATA
    USER_DATA = {}
    logger.info("已清空用户数据")
    return
