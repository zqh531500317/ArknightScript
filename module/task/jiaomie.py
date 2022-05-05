from module.fight.jiaomie import Jiaomie
from module.base import *


@timer
def jiaomie(map_name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    task = Jiaomie(max_fight_time, use_medicine=use_medicine, medicine_num=medicine_num,
                   use_stone=use_stone, stone_num=stone_num)
    task.cycleFight()
