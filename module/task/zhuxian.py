import module.step.gamepass_step
import module.step.click_step
import module.step.judge_step
import module.task.fight
from module.utils.core_clickLoader import ci
from module.utils.core_decoratir import timer


# name 主线名称    fight_time最大次数
@timer
def zhuxian(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    # 将主线格式固定到 章节数-X  其中章节=实际章节 如1-X
    series = name[0]
    for i, c in enumerate(name):
        if c.isdigit():
            series = c
            break

    left = str(series) + "-X"
    print(left)
    print(ci)
    v = ci[left]
    module.step.judge_step.ensureGameOpenAndInMain()
    module.step.gamepass_step.exec_by_clickLoader(v)
    # 移动到章节最左边
    module.step.gamepass_step.goto_ahead_for_zhuxian()

    module.step.gamepass_step.find_game_position(name)
    module.task.fight.cycleFight(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
