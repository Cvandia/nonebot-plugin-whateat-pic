import secrets

import aiofiles
from nonebot import get_driver
from nonebot.adapters import Event
from nonebot.log import logger
from nonebot.permission import SUPERUSER
from nonebot_plugin_alconna import Alconna, Args, Match, on_alconna
from nonebot_plugin_alconna.uniseg import Image, Text, UniMessage
from nonebot_plugin_alconna.uniseg.tools import image_fetch
from nonebot_plugin_apscheduler import scheduler

from .check_user_data import check_iscd, check_ismax
from .files import delete_pic, save_pic
from .menu import Menu
from .random_pic import random_pic

NICKNAME = list(get_driver().config.nickname)
BOT_NAME = NICKNAME[0] if NICKNAME else "脑积水"

TIME = 0.0
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
    Alconna("全部菜单", Args["img_type?", str]),
    use_cmd_start=True,
    aliases=("查看菜单", "查看菜品"),
)

add_menu_matcher = on_alconna(
    Alconna(
        "添加菜单", Args["name?", str], Args["img_type?", str], Args["img?", Image]
    ),
    use_cmd_start=True,
    permission=SUPERUSER,
)

del_menu_matcher = on_alconna(
    Alconna("删除菜单", Args["name?", str], Args["img_type?", str]),
    use_cmd_start=True,
    permission=SUPERUSER,
)


eat_pic_matcher.shortcut(
    r"^[今|明|后]?[天|日]?(早|中|晚)?(上|午|餐|饭|夜宵|宵夜|早|晚)吃(什么|啥|点啥)$",
    fuzzy=False,
    prefix=True,
)
drink_pic_matcher.shortcut(
    r"^[今|明|后]?[天|日]?(早|中|晚)?(上|午|餐|饭|夜宵|宵夜|早|晚)喝(什么|啥|点啥)$",
    fuzzy=False,
    prefix=True,
)


@eat_pic_matcher.handle()
async def handle_eat_pic(event: Event):
    global TIME
    global USER_DATA
    check_max_result, USER_DATA = check_ismax(event, USER_DATA)
    check_result, remain_time, TIME = check_iscd(TIME)
    if check_max_result:
        await UniMessage.text(secrets.choice(MAX_MSG)).finish()
    elif check_result:
        await UniMessage.text(f"cd冷却中,还有{remain_time:.2f}秒").finish()
    else:
        pic_path, pic_name = random_pic("eat")
        send_msg: UniMessage = UniMessage(Text(f"🎉{BOT_NAME}建议你吃🎉\n{pic_name}"))
        async with aiofiles.open(pic_path, "rb") as f:
            send_msg.append(Image(raw=await f.read()))
        await send_msg.finish()


@drink_pic_matcher.handle()
async def handle_drink_pic(event: Event):
    global TIME
    global USER_DATA
    check_max_result, USER_DATA = check_ismax(event, USER_DATA)
    check_result, remain_time, TIME = check_iscd(TIME)
    if check_max_result:
        await UniMessage.text(secrets.choice(MAX_MSG)).finish()
    elif check_result:
        await UniMessage.text(f"cd冷却中,还有{remain_time:.2f}秒").finish()
    else:
        pic_path, pic_name = random_pic("drink")
        send_msg: UniMessage = UniMessage(Text(f"🎉{BOT_NAME}建议你喝🎉\n{pic_name}"))
        async with aiofiles.open(pic_path, "rb") as f:
            send_msg.append(Image(raw=await f.read()))
        await send_msg.finish()


@view_menu_matcher.handle()
async def handle_view_menu(img_type: Match[str]):
    if img_type.available:
        view_menu_matcher.set_path_arg("img_type", img_type.result)


@view_menu_matcher.got_path("img_type", prompt=f"请告诉{BOT_NAME}具体菜单类型吧")
async def _(img_type: str):
    menu_type = img_type.strip()
    if menu_type in ["菜单", "菜品"]:
        menu_type = "eat"
    elif menu_type in ["饮料", "饮品"]:
        menu_type = "drink"
    else:
        await UniMessage.text("菜单类型错误，请重新输入").finish()

    try:
        menu = Menu(menu_type)
        send_msg_list = UniMessage(Text("菜单如下："))
        for img in menu.draw_menu():
            img_bytesio = io.BytesIO()
            img.save(img_bytesio, format="JPEG")
            send_msg_list.append(Image(raw=img_bytesio))  # type: ignore
        await send_msg_list.finish()
    except OSError as e:
        await UniMessage.text(f"没有找到菜单，请稍后重试\n{e}").finish()


@add_menu_matcher.handle()
async def _(name: Match[str], img_type: Match[str]):
    if name.available:
        add_menu_matcher.set_path_arg("name", name.result)
    if img_type.available:
        add_menu_matcher.set_path_arg("img_type", img_type.result)


@add_menu_matcher.got_path("name", prompt=f"请告诉{BOT_NAME}具体菜名或者饮品名吧")
async def _(name: str):
    if not name:
        await UniMessage.text("菜名不能为空，请重新输入").finish()


@add_menu_matcher.got_path("img_type", prompt=f"请告诉{BOT_NAME}具体菜单类型吧")
async def _(img_type: str):
    if img_type in ["菜品", "菜单"]:
        add_menu_matcher.set_path_arg("img_type", "eat")
    elif img_type in ["饮料", "饮品"]:
        add_menu_matcher.set_path_arg("img_type", "drink")
    else:
        await UniMessage.text("菜单类型错误，请重新输入").finish()


@add_menu_matcher.got_path(
    "img", prompt=f"请告诉{BOT_NAME}图片吧", middleware=image_fetch
)
async def _(
    name: str,
    img_type: str,
    img: bytes,
):
    if not img:
        await UniMessage.text("图片不能为空，请重新输入").finish()
    try:
        save_pic(img, img_type=img_type, name=name)
        await UniMessage.text(f"成功添加{name}").finish()
    except OSError as e:
        await UniMessage.text(f"添加失败，请稍后重试\n{e}").finish()


@del_menu_matcher.handle()
async def _(name: Match[str], img_type: Match[str]):
    if name.available:
        del_menu_matcher.set_path_arg("name", name.result)
    if img_type.available:
        del_menu_matcher.set_path_arg("img_type", img_type.result)


@del_menu_matcher.got_path("name", prompt=f"请告诉{BOT_NAME}具体菜名或者饮品名吧")
async def _(name: str):
    if not name:
        await UniMessage.text("菜名不能为空，请重新输入").finish()


@del_menu_matcher.got_path("img_type", prompt=f"请告诉{BOT_NAME}具体菜单类型吧")
async def _(img_type: str, name: str):
    if img_type in ["菜品", "菜单"]:
        img_type = "eat"
    elif img_type in ["饮料", "饮品"]:
        img_type = "drink"
    else:
        await UniMessage.text("菜单类型错误，请重新输入").finish()
    try:
        delete_pic(img_type, name)  # type: ignore
        await UniMessage.text(f"成功删除{name}").finish()
    except FileNotFoundError as e:
        await UniMessage.text(f"删除失败, {e}").finish()


# 每日8点清空用户数据
@scheduler.scheduled_job("cron", hour=8)
async def _():
    USER_DATA.clear()
    logger.info("已清空用户数据")
