from nonebot.log import logger
from pathlib import Path
from rich.progress import Progress
from config import config

import asyncio
import json
import httpx


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
                url = base_url+name
                try:
                    resp = await client.get(url, timeout=20, follow_redirects=True)
                    resp.raise_for_status()
                    return resp.content
                except httpx.HTTPError:
                    pass
            logger.warning(f"{name} download failed!")

    async with httpx.AsyncClient() as client:
        if content := await _download(client, "res/download_list.json"):
            resource_list = json.loads(content.decode("utf-8"))
        else:
            return

    # 下载资源文件
    download_list: list[tuple[Path, str]] = [] 
    drink_pic_path = Path(config.whatpic_res_path) / "drink_pic"
    eat_pic_path = Path(config.whatpic_res_path) / "eat_pic"

    # 检查文件夹是否存在
    if not drink_pic_path.exists():
        drink_pic_path.mkdir(parents=True)
    if not eat_pic_path.exists():
        eat_pic_path.mkdir(parents=True)

    # 添加下载任务
    for item in resource_list["drink_pic"]:
        download_list.append((drink_pic_path, item["name"]))
    for item in resource_list["eat_pic"]:
        download_list.append((eat_pic_path, item["name"]))

    if len(download_list):
        logger.info("Downloading images ...")
    else:
        return

    # 下载资源
    async with httpx.AsyncClient() as client:
        async def download_image(file_path: Path, file_name: str):
            if content := await _download(client, file_name):
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


if __name__ == "__main__":
    asyncio.run(check_resource())