import os
import json

# 把./drink_pic/下的所有图片和./eat_pic/下的所有图片的文件名写入到./downloaded.json中


def get_file_names(directory):
    """获取给定目录中的文件名列表。"""
    file_names = []
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            file_names.append({"name": file})
    return file_names


def main():
    """主函数，将文件名写入 JSON 文件。"""
    current_directory = os.path.dirname(os.path.abspath(__file__))
    drink_pic_files = get_file_names(os.path.join(current_directory, "drink_pic"))
    eat_pic_files = get_file_names(os.path.join(current_directory, "eat_pic"))

    data = {"drink_pic": drink_pic_files, "eat_pic": eat_pic_files}

    output_file = os.path.join(current_directory, "download_list.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
