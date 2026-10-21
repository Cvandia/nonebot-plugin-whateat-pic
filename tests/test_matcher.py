"""Exercise the real command parser and user-facing error handlers."""

import asyncio
import importlib
import warnings
from types import SimpleNamespace

import nonebot
import pytest
from nonebot.exception import FinishedException


@pytest.fixture(scope="module")
def matcher_module(tmp_path_factory):
    root = tmp_path_factory.mktemp("runtime")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        nonebot.init(
            driver="~none",
            command_start={"/", "!"},
            whatpic_res_path=str(root),
            localstore_cache_dir=str(root / "cache"),
            localstore_data_dir=str(root / "data"),
            localstore_config_dir=str(root / "config"),
        )
        plugin = nonebot.load_plugin("nonebot_plugin_whateat_pic")
    assert plugin is not None  # noqa: S101
    assert not any("Shortcut Key" in str(w.message) for w in caught)  # noqa: S101
    return importlib.import_module("nonebot_plugin_whateat_pic.matcher")


@pytest.mark.parametrize("kind", ["eat", "drink"])
@pytest.mark.parametrize(
    ("template", "matched"),
    [
        ("/今天早上{}什么", True),
        ("!明天中午{}啥", True),
        ("/今晚{}点啥", True),
        ("今天早上{}什么", False),
        ("/今天早上{}什么abc", False),
        ("/今天早上{}什么 abc", False),
        ("/|天早上{}什么", False),
    ],
)
def test_shortcuts_respect_prefix_and_full_match(
    matcher_module, kind, template, matched
):
    matcher = getattr(matcher_module, f"{kind}_pic_matcher")
    verb = "吃" if kind == "eat" else "喝"
    result = matcher.command().parse(template.format(verb))
    assert result.matched is matched  # noqa: S101


@pytest.mark.parametrize(
    ("operation", "error", "expected"),
    [
        ("add", OSError("/private/bot/cache/secret.jpg"), "添加失败，请稍后重试"),
        ("add", ValueError("/private/bot/cache"), "菜名不合法，请重新输入"),
        (
            "delete",
            FileNotFoundError("/private/bot/cache/secret.jpg"),
            "删除失败，未找到该菜品或饮品",
        ),
        (
            "delete",
            PermissionError("/private/bot/cache/secret.jpg"),
            "删除失败，请稍后重试",
        ),
        ("delete", ValueError("/private/bot/cache"), "菜名不合法，请重新输入"),
        (
            "view",
            FileNotFoundError("/private/bot/cache/secret.jpg"),
            "没有找到菜单，请稍后重试",
        ),
    ],
)
def test_file_errors_do_not_expose_paths(
    matcher_module, monkeypatch, operation, error, expected
):
    replies = []

    class Reply:
        async def finish(self):
            raise FinishedException

    def text(message):
        replies.append(message)
        return Reply()

    def fail(*_args, **_kwargs):
        raise error

    monkeypatch.setattr(matcher_module, "UniMessage", SimpleNamespace(text=text))
    if operation == "add":
        monkeypatch.setattr(matcher_module, "save_pic", fail)
        handler = matcher_module.add_menu_matcher.handlers[-1].call
        kwargs = {"name": "测试", "img_type": "eat", "img": b"image"}
    elif operation == "delete":
        monkeypatch.setattr(matcher_module, "delete_pic", fail)
        handler = matcher_module.del_menu_matcher.handlers[-1].call
        kwargs = {"name": "测试", "img_type": "菜品"}
    else:
        monkeypatch.setattr(matcher_module, "Menu", fail)
        handler = matcher_module.view_menu_matcher.handlers[-1].call
        kwargs = {"img_type": "菜品"}

    with pytest.raises(FinishedException):
        asyncio.run(handler(**kwargs))
    assert replies == [expected]  # noqa: S101
