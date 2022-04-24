import datetime

from apscheduler.triggers.date import DateTrigger

import module.task.fight
import module.task.zhuxian
import module.task.ziyuanshouji
import module.task.jiaomie
import module.task.huodong
from module.schedule.baseScheduler import base_scheduler


def once_zhuxian(name, times, use_medicine, medicine_num, use_stone, stone_num):
   base_scheduler.add_job(module.task.zhuxian.zhuxian,
                                          args=(name, times, use_medicine, medicine_num, use_stone, stone_num),
                                          trigger=DateTrigger(), id="zhuxian_once")


def once_ziyuanshouji(name, times, use_medicine, medicine_num, use_stone, stone_num):
   base_scheduler.add_job(module.task.ziyuanshouji.ziyuanshouji,
                                          args=(times, name, use_medicine, medicine_num, use_stone, stone_num),
                                          trigger=DateTrigger(), id="ziyuanshouji_once")


def once_jiaomie(times, use_medicine, medicine_num, use_stone, stone_num):
   base_scheduler.add_job(module.task.jiaomie.jiaomie,
                                          args=("", times, use_medicine, medicine_num, use_stone, stone_num),
                                          trigger=DateTrigger(), id="jiaomie_once")


def once_unknown(times, use_medicine, medicine_num, use_stone, stone_num):
   base_scheduler.add_job(module.task.fight.cycleFight,
                                          args=(times, "unknown", use_medicine, medicine_num, use_stone, stone_num),
                                          trigger=DateTrigger(), id="unknown_once")


def once_huodong(name, times, use_medicine, medicine_num, use_stone, stone_num):
   base_scheduler.add_job(module.task.huodong.huodong,
                                          args=(name, times, use_medicine, medicine_num, use_stone, stone_num),
                                          trigger=DateTrigger(), id="huodong_once")


def once_recently(name, times, use_medicine, medicine_num, use_stone, stone_num):
   base_scheduler.add_job(module.task.fight.recently,
                                          args=(name, times, use_medicine, medicine_num, use_stone, stone_num),
                                          trigger=DateTrigger(), id="recently_once")


def zhuxian(id, trigger, map_name, times):
   base_scheduler.add_job(module.task.zhuxian.zhuxian,
                                          args=(map_name, times, False, 0, False, 0),
                                          trigger=trigger, id=id)


def ziyuanshouji(id, trigger, map_name, times):
   base_scheduler.add_job(module.task.ziyuanshouji.ziyuanshouji,
                                          args=(times, map_name, False, 0, False, 0),
                                          trigger=trigger, id=id)


def jiaomie(id, trigger, map_name, times):
   base_scheduler.add_job(module.task.jiaomie.jiaomie,
                                          args=(map_name, times, False, 0, False, 0),
                                          trigger=trigger, id=id)


def huodong(id, trigger, map_name, times):
   base_scheduler.add_job(module.task.huodong.huodong,
                                          args=(map_name, times, False, 0, False, 0),
                                          trigger=trigger, id=id)


def recently(id, trigger, times):
   base_scheduler.add_job(module.task.fight.recently,
                                          args=("recently", times, False, 0, False, 0),
                                          trigger=trigger, id=id)
