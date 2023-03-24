

<div align="center">

<a href="https://v2.nonebot.dev/store"><img src="https://i3.meishichina.com/atta/recipe/2023/01/06/20230106167298595549937310737312.JPG?x-oss-process=style/p800" width="180" height="180" alt="NoneBotPluginLogo"></a>

</div>

<div align="center">

# nonebot-plugin-whateat-pic

_⭐基于Nonebot2的一款今天吃什么喝什么的插件⭐_


</div>

<div align="center">
<a href="https://www.python.org/downloads/release/python-390/"><img src="https://img.shields.io/badge/python-3.8+-blue"></a>  <a href=""><img src="https://img.shields.io/badge/QQ-1141538825-yellow"></a> <a href="https://github.com/Cvandia/nonebot-plugin-whateat-pic/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue"></a> <a href="https://v2.nonebot.dev/"><img src="https://img.shields.io/badge/Nonebot2-rc1+-red"></a>
</div>


## ⭐ 介绍

一款离线版决定今天吃喝什么的nb2插件，功能及其简单。
~~抄袭~~改编自hosinoBot的插件[今天吃什么](https://github.com/A-kirami/whattoeat)
有不足的地方还请指出


<div align="center">

### 或者你有啥关于该插件的新想法的，可以提issue或者pr (>A<)

</div>

## 💿 安装

<details>
<summary>安装</summary>

pip 安装

```
pip install nonebot-plugin-whateat-pic
```

nb-cli安装

```
nb plugin install nonebot-plugin-whateat-pic --upgrade
```
 
 </details>
 
 <details>
 <summary>注意</summary>
 
 由于包含有图片，包容量较大，推荐镜像站下载
  
 清华源```https://pypi.tuna.tsinghua.edu.cn/simple```
 
 阿里源```https://mirrors.aliyun.com/pypi/simple/```
 
</details>


## ⚙️ 配置
### 在env.中添加以下配置

|名称|类型|默认值|范围|说明|
|:-----:|:----:|:----:|:------:|:------|
|whateat_cd|int|10|0-9999|内置触发cd|
|whateat_max|int|0|0-9999|每日用户触发的最大次数，默认0时为无上限|


> 机器的名字“脑积水”是默认值，(我不相信有人不会配置nonebot2的nick_name)

## ⭐ 使用

### 指令：
| 指令 | 需要@ | 范围 | 说明 |权限|
|:-----:|:----:|:----:|:----:|:----:|
|今天早上吃什么|否|私聊、群聊|随机发送食物|任何|
|今天早上喝什么|否|私聊、群聊|随机发送饮品|任何|
|查看全部菜单|否|私聊、群聊|查看全部菜单|任何|
|查看菜单|否|私聊、群聊|查看指定菜单|任何|
|添加菜单|否|私聊、群聊|自定义添加菜单|群主，超管，管理员|
|删除菜单|否|私聊、群聊|自定义删除菜单|群主，超管，管理员|

**注意**

默认情况下, 您应该在指令前加上命令前缀, 通常是 /

## 🌙 未来
- [x] 或许添加更多的美食图片吧……
- [x] 添加更多功能
- [x] 自定义添加菜单，饮品(~~我懒，或者帮我写个?~~)QwQ（~~最后还是自己写~~）

--- 喜欢记得点个star⭐---
