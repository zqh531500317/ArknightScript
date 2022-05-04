from module.inventory.demo import get_all_item_img_in_screen, get_quantity_ppocr, get_item_info
from module.base import base, logger


def show_bag(with_quantity=True):
    items = {}
    img = base.screen(memery=True)
    item_images = get_all_item_img_in_screen(img)
    for item_img in item_images:
        # prob 识别结果置信度
        # item_id, item_name, item_type 见 Kengxxiao/ArknightsGameData 的解包数据
        # https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/item_table.json
        prob, item_id, item_name, item_type = get_item_info(item_img['item_img'])
        quantity = None
        if with_quantity:
            quantity = get_quantity_ppocr(item_img['item_img'])
        items[item_name] = {"num": quantity, "prob": prob}
        # name: 中级作战记录, quantity: 8416, pos: (235, 190), prob: 0.9656420946121216
        logger.info(f"name: {item_name}, quantity: {quantity}, pos: {item_img['item_pos']}, prob: {prob}")
        # show_img(item_img['item_img'])
    return items


__all__ = ["show_bag"]
