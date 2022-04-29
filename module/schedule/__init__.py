import module.schedule.fightScheduler
import module.schedule.dailyScheduler
import module.schedule.jijianScheduler


def config_scheduler():
    module.schedule.dailyScheduler.add_all()
    module.schedule.jijianScheduler.add_all()
