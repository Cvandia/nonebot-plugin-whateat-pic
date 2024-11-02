from nonebot.log import logger
from pathlib import Path
from rich.progress import Progress
import asyncio
import json
import httpx
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
    global available_urls

    async def _download(client: httpx.AsyncClient, name: str):
        async with semaphore:
            for base_url in available_urls:
                url = base_url + "refs/heads/main/res/" + name
                try:
                    resp = await client.get(url, timeout=20, follow_redirects=True)
                    resp.raise_for_status()
                    return resp.content
                except httpx.HTTPError:
                    pass
            logger.warning(f"{url} download failed!")

    async with httpx.AsyncClient() as client:
        if content := await _download(client, "download_list.json"):
            resource_list = json.loads(content.decode("utf-8"))
        else:
            return

    # 下载资源文件
    download_list: list[tuple[Path, str]] = []

    # 添加下载任务
    for item in resource_list["drink_pic"]:
        path_name = "drink_pic/" + item["name"]
        drink_pic_path = Path(config.whatpic_res_path) / path_name
        download_list.append((drink_pic_path, path_name))
    for item in resource_list["eat_pic"]:
        path_name = "eat_pic/" + item["name"]
        eat_pic_path = Path(config.whatpic_res_path) / path_name
        download_list.append((eat_pic_path, path_name))

    if len(download_list):
        logger.info("Downloading images ...")
    else:
        return

    # 下载资源
    async with httpx.AsyncClient() as client:

        async def download_image(file_path: Path, file_name: str):
            if file_path.exists():
                logger.info(f"{file_path} already exists, skipping download.")
                return
            if content := await _download(client, file_name):
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with file_path.open("wb") as f:
                    f.write(content)

        with Progress(
            *Progress.get_default_columns(), "[yellow]{task.completed}/{task.total}"
        ) as progress:
            progress_task = progress.add_task(
                "[green]Downloading...", total=len(download_list)
            )
            tasks = [
                download_image(file_path, file_name)
                for file_path, file_name in download_list
            ]
            for task in asyncio.as_completed(tasks):
                await task
                progress.update(progress_task, advance=1)

from nonebot import get_driver
import asyncio

driver = get_driver()
@driver.on_startup
async def on_startup():
    logger.info("Checking resources...")
    asyncio.create_task(check_resource())

# 测试代码
# if __name__ == "__main__":
#     asyncio.run(check_resource())


