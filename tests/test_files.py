"""resolve_pic_path 的路径穿透防护测试。

不依赖 nonebot 运行时, 通过注入假的 config 模块来单独测试 files.py 的路径解析。
"""

import importlib.util
import sys
import types
from pathlib import Path

import pytest

PLUGIN_DIR = Path(__file__).parent.parent / "nonebot_plugin_whateat_pic"


def _noop(*_args, **_kwargs):
    """占位 logger.error, 吞掉被测代码的日志调用。"""


@pytest.fixture
def files_module(tmp_path, monkeypatch):
    """构造一个最小可用的 files.py 运行环境, 资源目录指向 tmp_path。"""
    plugin_pkg = types.ModuleType("nonebot_plugin_whateat_pic")
    plugin_pkg.__path__ = [str(PLUGIN_DIR)]
    monkeypatch.setitem(sys.modules, "nonebot_plugin_whateat_pic", plugin_pkg)

    config_mod = types.ModuleType("nonebot_plugin_whateat_pic.config")
    config_mod.config = types.SimpleNamespace(whatpic_res_path=str(tmp_path))
    monkeypatch.setitem(sys.modules, "nonebot_plugin_whateat_pic.config", config_mod)

    log_mod = types.ModuleType("nonebot.log")
    log_mod.logger = types.SimpleNamespace(error=_noop)
    monkeypatch.setitem(sys.modules, "nonebot.log", log_mod)

    spec = importlib.util.spec_from_file_location(
        "nonebot_plugin_whateat_pic.files", PLUGIN_DIR / "files.py"
    )
    mod = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, "nonebot_plugin_whateat_pic.files", mod)
    spec.loader.exec_module(mod)

    (tmp_path / "eat_pic").mkdir()
    (tmp_path / "drink_pic").mkdir()
    return mod


def test_normal_name_resolves_inside_dir(files_module, tmp_path):
    path = files_module.resolve_pic_path("eat", "红烧肉")
    expected = (tmp_path / "eat_pic" / "红烧肉.jpg").resolve()
    assert path == expected  # noqa: S101


@pytest.mark.parametrize(
    "name",
    [
        "../../evil",
        "..\\..\\evil",
        "../evil",
        "..",
        ".",
        "",
        "a/b",
        "a\\b",
        "/abs/path",
        "evil\0name",
    ],
)
def test_malicious_names_are_rejected(files_module, name):
    with pytest.raises(ValueError, match="name must not"):
        files_module.resolve_pic_path("eat", name)


@pytest.mark.parametrize("img_type", ["", "eat_pic", "../eat", "other"])
def test_invalid_img_type_is_rejected(files_module, img_type):
    with pytest.raises(ValueError, match="img_type must be"):
        files_module.resolve_pic_path(img_type, "红烧肉")


def test_save_pic_does_not_write_outside_dir(files_module, tmp_path):
    with pytest.raises(ValueError, match="name must not"):
        files_module.save_pic(b"data", "eat", "../../escaped")
    # 确认没有在资源目录外留下文件
    assert not (tmp_path.parent / "escaped.jpg").exists()  # noqa: S101
