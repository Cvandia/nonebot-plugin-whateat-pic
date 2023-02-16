from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.plugin import on_regex
from pathlib import Path
import os
import nonebot
import random, base64

what_eat=on_regex(r"^(/)?[今|明|后]?[天|日]?(早|中|晚)?(上|午|餐|饭|夜宵|宵夜)吃(什么|啥|点啥)$",priority=5)
what_drink=on_regex(r"^(/)?[今|明|后]?[天|日]?(早|中|晚)?(上|午|餐|饭|夜宵|宵夜)喝(什么|啥|点啥)$",priority=5)

#今天吃什么路径
img_eat_path = Path(os.path.join(os.path.dirname(__file__), "eat_pic"))
all_file_eat_name = os.listdir(str(img_eat_path))

#今天喝什么路径
img_drink_path = Path(os.path.join(os.path.dirname(__file__), "drink_pic"))
all_file_drink_name= os.listdir(str(img_drink_path))

#载入bot名字
Bot_NICKNAME = list(nonebot.get_driver().config.nickname)
Bot_NICKNAME = Bot_NICKNAME[0] if Bot_NICKNAME else "脑积水"

@what_drink.handle()
async def wtd():
    img_name = random.choice(all_file_drink_name)
    img = img_eat_path / img_name
    with open(img, 'rb') as im:
        img_bytes = im.read()
    base64_str = "base64://" + base64.b64encode(img_bytes).decode()
    msg=(
        f"{Bot_NICKNAME}建议你吃: \n⭐{img.stem}⭐\n"
        + MessageSegment.image(base64_str)
    )
    try:
        await what_drink.send("正在为你找好喝的……")
        await what_drink.send(msg, at_sender=True)
    except:
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
    except:
        await what_eat.finish("出错啦！没有找到好吃的~")
