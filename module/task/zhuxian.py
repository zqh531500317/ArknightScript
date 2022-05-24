from module.fight.zhuxian import ZhuXian


# name 主线名称    fight_time最大次数
def zhuxian(name, max_fight_time, use_medicine=False, medicine_num=0, use_stone=False, stone_num=0):
    task = ZhuXian(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
    task.cycleFight()
