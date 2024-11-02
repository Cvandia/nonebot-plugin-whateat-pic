from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import Literal, Iterator
from .config import config


class Menu:
    """
    生成菜单的类
    """

    dish_path: Path  # 菜品图片的路径
    menu_background: Image.Image  # 菜单背景图
    menu_font: ImageFont.FreeTypeFont  # 菜单字体

    def __init__(self, menu_type: Literal["drink", "eat"]) -> None:
        # 菜单图片的路径
        self.dish_path = Path(config.whatpic_res_path) / f"{menu_type}_pic"
        # 获取所有菜品的名字
        self.all_dish_name = [i.stem for i in self.dish_path.iterdir()]
        # 菜单背景图
        self.menu_background = Image.open(
            Path(__file__).parent / "menu_res" / "menu_bg.jpg"
        )
        # 字体大小
        self.font_size = 30
        # 加载字体
        self.menu_font = ImageFont.truetype(
            str(Path(__file__).parent / "menu_res" / "msyh.ttc"), self.font_size
        )

    @property
    def menu_bg_size(self) -> tuple:
        """
        获取菜单背景图的大小
        """
        return self.menu_background.size

    # 生成迭代器用于for循环遍历所有的生成的菜单
    def draw_menu(self) -> Iterator[Image.Image]:
        # 每个菜单的行数: 背景图高度 - 200(上下边距) // （字体大小+10(行间距)） = 菜单行数
        line_num = (self.menu_bg_size[1] - 150) // (self.font_size + 10)
        # 总共需要合成的图片数量
        img_num = len(self.all_dish_name) // line_num + 1
        # 生成所有菜单的图片
        for i in range(img_num):
            # 生成一张背景图的副本
            menu_img = self.menu_background.copy()
            # 生成draw对象
            draw = ImageDraw.Draw(menu_img)
            # 生成菜单的名字
            for j in range(line_num):
                # 如果菜单名字已经全部生成完毕
                if i * line_num + j >= len(self.all_dish_name):
                    break
                # 生成菜单序号+名字，（居中显示）
                draw.text(
                    ((self.menu_bg_size[0] - 300) // 2, 75 + j * (self.font_size + 10)),
                    f"{i * line_num + j + 1}.{self.all_dish_name[i * line_num + j]}",
                    font=self.menu_font,
                    fill="black",
                )
            yield menu_img


# 测试程序
# mn = Menu("eat")
# for i in mn.draw_menu():
#     i.show()
#     if input("是否继续") == "n":
#         break
