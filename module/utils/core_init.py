from module.utils.core_log import init_log
import module.schedule.dailyScheduler
import module.schedule.jijianScheduler


def init():
    init_log()
    module.schedule.dailyScheduler.add_all()
    module.schedule.jijianScheduler.add_all()
