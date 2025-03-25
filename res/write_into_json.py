import json
from pathlib import Path

# 把./drink_pic/下的所有图片和./eat_pic/下的所有图片的文件名写入到./downloaded.json中


def get_file_names(directory: Path):
    """获取给定目录中的文件名列表。"""
    return [
        {"name": entry.name}
        for entry in directory.iterdir()
        if entry.is_file()
    ]


def main():
    """主函数，将文件名写入 JSON 文件。"""
    current_directory = Path(__file__).resolve().parent
    drink_pic_files = get_file_names(current_directory / "drink_pic")
    eat_pic_files = get_file_names(current_directory / "eat_pic")

    data = {"drink_pic": drink_pic_files, "eat_pic": eat_pic_files}

    output_file = current_directory / "download_list.json"
    with Path.open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
