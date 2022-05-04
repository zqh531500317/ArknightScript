from module.entity.ocr_entity import OcrEntity
from module.step.gamepass_step import GamePassStep
from module.step.common_step import CommonStep
from module.step.fight_step import FightStep
from module.base import *
from module.utils.core_clickLoader import *


@timer
def huodong(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    now = "yurenhao"
    eval(now)(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num)


def yurenhao(name: str, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    func_name = "yurenhao"
    CommonStep.ensureGameOpenAndInMain()
    CommonStep.dowait(a_zhongduan[1], "/ui/a_zhongduan.png", description="进入终端")
    CommonStep.dowait(b_huodong[1], OcrEntity(except_result="作战", x1=913, y1=19, x2=952, y2=38), description="进入活动")
    huodong_click = (336, 563, 369, 570)
    CommonStep.dowait(huodong_click, "/huodong/main_{}.png".format(func_name), description="进入活动界面")
    GamePassStep.goto_ahead_for_huodong()
    SN_9 = (687, 404, 712, 428)
    SN_10 = (750, 297, 779, 322)

    if name.upper() == "SN-9":
        ck = SN_9
    elif name.upper() == "SN-10":
        ck = SN_10
    else:
        return
    CommonStep.dowait(ck, "/huodong/map_choosed_{}.png".format(func_name), description="选中关卡")

    def prefunc(*parem):
        func_name_ = parem[0]
        ck1 = parem[1]
        # 选择代理
        if not base.is_template_match("/huodong/map_daili_{}.png".format(func_name_)):
            CommonStep.dowait((1085, 582, 1086, 583),
                              "/huodong/map_daili_{}.png".format(func_name_),
                              description="选中代理")

    FightStep.cycleFight(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num,
                         True, True, prefunc, func_name, ck)
    #
# # name 名称    fight_time最大次数
# def yichenmanbu(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
#     CommonStep.ensureGameOpenAndInMain()
#     v = ci["huodong"]
#     GamePassStep.exec_by_clickLoader(v)
#     base.randomClick((1049, 540, 1111, 555))
#     time.sleep(base.get("sleep_time"))
#     # 移动到章节最右边
#     GamePassStep.goto_behind_for_huodong()
#     if name == "WD-6":
#         base.randomClick((13, 338, 73, 361))
#     elif name == "WD-7":
#         randomClick((139, 458, 216, 481))
#     elif name == "WD-8":
#         randomClick((455, 461, 527, 481))
#     else:
#         return
#     time.sleep(cf.get("sleep_time"))
#     module.task.fight.cycleFight(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
#
#
# # name 名称    fight_time最大次数
# def wudaoxianlu(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
#     CommonStep.ensureGameOpenAndInMain()
#     v = ci["huodong"]
#     module.step.gamepass_step.exec_by_clickLoader(v)
#     randomClick((1114, 465, 1130, 482))
#     time.sleep(cf.get("sleep_time"))
#     # 移动到章节最右边
#     module.step.gamepass_step.goto_behind_for_huodong()
#     if name == "GA-6":
#         randomClick((34, 332, 95, 350))
#     elif name == "GA-7":
#         randomClick((317, 332, 382, 350))
#     elif name == "GA-8":
#         randomClick((612, 332, 678, 350))
#     else:
#         return
#     time.sleep(cf.get("sleep_time"))
#     module.task.fight.cycleFight(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
#
#
# # name 名称    fight_time最大次数
# def changyelinguang(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
#     CommonStep.ensureGameOpenAndInMain()
#     v = ci["changyelinguang"]
#     module.step.gamepass_step.exec_by_clickLoader(v)
#     # 移动到章节最左边
#     module.step.gamepass_step.goto_ahead_for_huodong()
#
#     module.step.gamepass_step.find_game_position(name)
#     module.task.fight.cycleFight(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
#
#
# # name 名称    fight_time最大次数
# def gudaofengyun(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
#     CommonStep.ensureGameOpenAndInMain()
#     v = ci["gudaofengyun"]
#     module.step.gamepass_step.exec_by_clickLoader(v)
#     time.sleep(3)
#     if name == "MB-6":
#         randomClick((804, 386, 873, 409))
#     elif name == "MB-7":
#         randomClick((802, 512, 876, 534))
#     elif name == "MB-8":
#         randomClick((1102, 513, 1170, 536))
#     else:
#         return
#     time.sleep(3)
#     module.task.fight.cycleFight(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
#
#
# # name 名称    fight_time最大次数
# def fengxueguojing(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
#     CommonStep.ensureGameOpenAndInMain()
#     v = ci["fengxueguojing"]
#     module.step.gamepass_step.exec_by_clickLoader(v)
#     time.sleep(3)
#     module.step.gamepass_step.goto_behind_for_ziyuanshouji()
#     time.sleep(3)
#     if name == "BI-6":
#         randomClick((228, 194, 295, 213))
#     elif name == "BI-7":
#         randomClick((447, 280, 506, 300))
#     elif name == "BI-8":
#         randomClick((000, 384, 670, 402))
#     else:
#         return
#     time.sleep(3)
#     module.task.fight.cycleFight(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
#
#
# # name 名称    fight_time最大次数
# def huazhongren(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
#     CommonStep.ensureGameOpenAndInMain()
#     v = ci["huazhongren"]
#     module.step.gamepass_step.exec_by_clickLoader(v)
#     # 移动到章节最左边
#     module.step.gamepass_step.goto_ahead_for_huodong()
#
#     module.step.gamepass_step.find_game_position(name)
#     module.task.fight.cycleFight(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
#
#
# # name 名称    fight_time最大次数
# def jiangjinjiu(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
#     CommonStep.ensureGameOpenAndInMain()
#     v = ci["jiangjinjiu"]
#     module.step.gamepass_step.exec_by_clickLoader(v)
#
#     if name != "IW-6" and name != "IW-7" and name != "IW-8":
#         return
#         # 移动到章节最左边
#     module.step.gamepass_step.goto_ahead_for_huodong()
#
#     module.step.gamepass_step.find_game_position_with_template(name)
#     module.task.fight.cycleFight(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
