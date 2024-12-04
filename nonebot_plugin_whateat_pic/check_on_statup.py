import asyncio
import json
from pathlib import Path

import httpx
from nonebot import get_driver
from nonebot.log import logger
from rich.progress import Progress

from .config import config

available_urls = [
    "https://raw.githubusercontent.com/Cvandia/nonebot-plugin-whateat-pic/",
    "https://mirror.ghproxy.com/https://raw.githubusercontent.com/Cvandia/nonebot-plugin-whateat-pic/",
    "https://cdn.jsdelivr.net/gh/Cvandia/nonebot-plugin-whateat-pic@",
    "https://fastly.jsdelivr.net/gh/Cvandia/nonebot-plugin-whateat-pic@",
    "https://raw.gitmirror.com/Cvandia/nonebot-plugin-whateat-pic/",
]


async def check_resource():
    semaphore = asyncio.Semaphore(10)

    async def _download(client: httpx.AsyncClient, name: str):
        async with semaphore:
            for base_url in available_urls:
                url = base_url + "refs/heads/main/res/" + name
                try:
                    resp = await client.get(url, timeout=20, follow_redirects=True)
                    if resp.raise_for_status():
                        logger.debug(f"{url} download success!")
                        return resp.content
                except httpx.HTTPError:
                    pass
            logger.warning(f"{url} download failed!")
            return None

    # 下载资源列表
    async with httpx.AsyncClient() as client:
        if content := await _download(client, "download_list.json"):
            resource_list = json.loads(content.decode("utf-8"))
        else:
            return

    # 检查资源目录下文件是否完整
    drink_pic_path = Path(config.whatpic_res_path) / "drink_pic"  # 本地资源目录
    eat_pic_path = Path(config.whatpic_res_path) / "eat_pic"  # 本地资源目录
    # TODO: 检查文件是否完整

    # 创建下载任务列表
    download_list: list[tuple[Path, str]] = []

    # 添加下载任务
    for item in resource_list["drink_pic"]:
        path_name = (
            "drink_pic/" + item["name"]
        )  # 在线资源路径: github.com/Cvandia/nonebot-plugin-whateat-pic/main/res/+ path_name
        download_list.append((drink_pic_path / item["name"], path_name))
    for item in resource_list["eat_pic"]:
        path_name = "eat_pic/" + item["name"]  # 在线资源路径
        download_list.append((eat_pic_path / item["name"], path_name))

    if download_list:
        logger.info("Downloading images ...")
    else:
        return

    # 下载资源
    async with httpx.AsyncClient() as client:
        exist_count = 0

        async def download_image(file_path: Path, file_name: str):
            if file_path.exists():
                logger.debug(f"{file_path} already exists, skipping download.")
                nonlocal exist_count
                exist_count += 1
                return
            if content := await _download(client, file_name):
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with file_path.open("wb") as f:
                    f.write(content)

        with Progress(
            *Progress.get_default_columns(), "[yellow]{task.completed}/{task.total}"
        ) as progress:
            progress_task = progress.add_task(
                "[green]Downloading pic...", total=len(download_list)
            )
            tasks = [
                download_image(file_path, file_name)
                for file_path, file_name in download_list
            ]
            for task in asyncio.as_completed(tasks):
                await task
                progress.update(progress_task, advance=1)

        logger.info(f"Downloaded {len(download_list) - exist_count} images.")


driver = get_driver()


@driver.on_startup
async def on_startup():
    logger.info("Checking resources...")
    task = asyncio.create_task(check_resource())
    await task


# 测试代码
