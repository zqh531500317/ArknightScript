import datetime
import time


class JobEntity:
    def __init__(self, id, name, next_run_time, actually_run_time=datetime.datetime.now().replace(microsecond=0)):
        self.id = id
        self.name = name
        self.next_run_time = next_run_time
        self.actually_run_time = actually_run_time
