import _thread

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from module.base.config import CoreConfig
from logzero import logger
from module.utils.core_utils import project_root_path
from module.base.state import State


class ConfigHandler(FileSystemEventHandler):
    def __init__(self):
        self.state = State()

    def on_modified(self, event):
        logger.debug("modify file:  %s", event.src_path)
        if 'config.yaml' in event.src_path:
            self.state.is_config_edit = True

    def on_created(self, event):
        logger.debug("creat file: %s", event.src_path)


def watch():
    logger.info("init_watchdog")
    watch_path = project_root_path() + "/config"
    config_handler = ConfigHandler()
    observer = Observer()
    observer.schedule(config_handler, watch_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(5)

    except KeyboardInterrupt:
        observer.stop()
    observer.join()


class Watcher(CoreConfig):

    def __init__(self):
        super().__init__()
        _thread.start_new_thread(watch, ())
