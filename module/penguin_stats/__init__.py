import asyncio
from module.base import base
from module.penguin_stats.core import Img, Result
from module.penguin_stats.gui_preload import item_index


def analyse() -> (dict, str):
    async def test():
        img = Img.read(base.endFight_path)
        if result := await Result.analyse(img):
            data, display = result
            return data, display

    data, display = asyncio.run(test())
    return data, display


def get_name_by_id(id):
    return item_index[id]['name_i18n']['zh']


__all__ = ["analyse", "get_name_by_id"]
