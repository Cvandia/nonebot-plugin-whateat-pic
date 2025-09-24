import nonebot_plugin_localstore as store
from nonebot.plugin import get_plugin_config
from pydantic import BaseModel, Field


class Config(BaseModel):
    whateat_cd: int = Field(default=10)
    whateat_max: int = Field(default=0)
    whatpic_res_path: str = Field(default=str(store.get_plugin_cache_dir()))


config = get_plugin_config(Config)
