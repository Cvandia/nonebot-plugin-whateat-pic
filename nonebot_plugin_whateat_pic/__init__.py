from nonebot.adapters.onebot.v11 import MessageSegment,MessageEvent,Bot,Message,GroupMessageEvent
from nonebot.exception import ActionFailed
from nonebot.plugin import on_regex
from nonebot.matcher import Matcher
from nonebot.params import Arg
from nonebot.log import logger
from nonebot.typing import T_State
from pathlib import Path
import os
import re
import nonebot
import random, base64

what_eat = on_regex(r"^(/)?[今|明|后]?[天|日]?(早|中|晚)?(上|午|餐|饭|夜宵|宵夜)吃(什么|啥|点啥)$",priority=5)
what_drink = on_regex(r"^(/)?[今|明|后]?[天|日]?(早|中|晚)?(上|午|餐|饭|夜宵|宵夜)喝(什么|啥|点啥)$",priority=5)
view_all_dishes = on_regex(r"^(/)?查[看|寻]?全部(菜[单|品]|饮[料|品])$",priority=5)
view_dish = on_regex(r"^(/)?查[看|寻]?(菜[单|品]|饮[料|品])[\s]?(.*)?")

#今天吃什么路径
img_eat_path = Path(os.path.join(os.path.dirname(__file__), "eat_pic"))
all_file_eat_name = os.listdir(str(img_eat_path))

#今天喝什么路径
img_drink_path = Path(os.path.join(os.path.dirname(__file__), "drink_pic"))
all_file_drink_name= os.listdir(str(img_drink_path))

#载入bot名字
Bot_NICKNAME = list(nonebot.get_driver().config.nickname)
Bot_NICKNAME = Bot_NICKNAME[0] if Bot_NICKNAME else "脑积水"


@view_dish.handle()
async def got_name(matcher:Matcher,state:T_State,event:MessageEvent):
    
    #正则匹配组
    args = list(state['_matched_groups'])
    
    if args[1] in ["菜单","菜品"]:
        state['type'] = "吃的"
    elif args[1] in ["饮料","饮品"]:
        state['type'] = "喝的"
        
    #设置下一步got的arg    
    if args[2]:
        matcher.set_arg("name",args[2])


        
@view_dish.got("name",prompt=f"请告诉{Bot_NICKNAME}具体菜名或者饮品名吧")
async def handle(state:T_State,name:Message = Arg()):
    
    if state['type'] == "吃的":
        img = img_eat_path / (str(name)+".jpg")
    elif state['type'] == "喝的":
        img = img_drink_path / (str(name)+".jpg")
          
    try:
        await view_dish.send(MessageSegment.image(img))
    except ActionFailed:
        await view_dish.finish("没有找到你所说的，请检查一下菜单吧",at_sender = True)


@view_all_dishes.handle()
async def handle(bot:Bot,event:MessageEvent,state:T_State):
    #正则匹配组
    args = list(state['_matched_groups'])
    
    if args[1] in ["菜单","菜品"]:
        path = img_eat_path
        all_name = all_file_eat_name
    elif args[1] in ["饮料","饮品"]:
        path = img_drink_path
        all_name = all_file_drink_name
        
        
    msg_list = [f"{Bot_NICKNAME}查询到的{args[1]}如下"]
    N = 0
    for name in all_name:
        N += 1
        img = path / name
        with open(img, 'rb') as im:
            img_bytes = im.read()
        base64_str = "base64://" + base64.b64encode(img_bytes).decode()
        name = re.sub(".jpg",'',name)
        msg_list.append(f"{N}.{name}\n{MessageSegment.image(base64_str)}")
    await send_forward_msg(bot,event,Bot_NICKNAME,bot.self_id,msg_list)
    
    
@what_drink.handle()
async def wtd():
    img_name = random.choice(all_file_drink_name)
    img = img_drink_path / img_name
    with open(img, 'rb') as im:
        img_bytes = im.read()
    base64_str = "base64://" + base64.b64encode(img_bytes).decode()
    msg=(
        f"{Bot_NICKNAME}建议你喝: \n⭐{img.stem}⭐\n"
        + MessageSegment.image(base64_str)
    )
    try:
        await what_drink.send("正在为你找好喝的……")
        await what_drink.send(msg, at_sender=True)
    except ActionFailed:
        await what_drink.finish("出错啦！没有找到好喝的~")



@what_eat.handle()
async def wte():
    img_name = random.choice(all_file_eat_name)
    img = img_eat_path / img_name
    with open(img, 'rb') as im:
        img_bytes = im.read()
    base64_str = "base64://" + base64.b64encode(img_bytes).decode()
    msg=(
        f"{Bot_NICKNAME}建议你吃: \n⭐{img.stem}⭐\n"
        + MessageSegment.image(base64_str)
    )
    try:
        await what_eat.send("正在为你找好吃的……")
        await what_eat.send(msg, at_sender=True)
    except ActionFailed:
        await what_eat.finish("出错啦！没有找到好吃的~")
        
#调用合并转发api        
async def send_forward_msg(
        bot: Bot,
        event: MessageEvent,
        name: str,
        uin: str,
        msgs: list,
) -> dict:
    def to_json(msg: Message):
        return {"type": "node", "data": {"name": name, "uin": uin, "content": msg}}

    messages = [to_json(msg) for msg in msgs]
    if isinstance(event, GroupMessageEvent):
        return await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
    else:
        return await bot.call_api(
            "send_private_forward_msg", user_id=event.user_id, messages=messages
        )