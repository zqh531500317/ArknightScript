from module.base import before
from module.fight.ziyuanshouji import Ziyuanshouji


# name 资源本名称   fight_time最大次数
@before
def ziyuanshouji(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num):
    task = Ziyuanshouji(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num)
    task.cycleFight()
