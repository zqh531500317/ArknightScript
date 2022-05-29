import module.schedule.fightScheduler
import module.schedule.dailyScheduler
import module.schedule.jijianScheduler
import module.schedule.otherScheduler


def config_scheduler():
    module.schedule.dailyScheduler.add_all()
    module.schedule.jijianScheduler.add_all()
    module.schedule.otherScheduler.add_all()
