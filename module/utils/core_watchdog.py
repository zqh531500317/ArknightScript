import _thread

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from module.utils.core_utils import project_root_path
import module.utils.core_config
from logzero import logger


class ConfigHandler(FileSystemEventHandler):
    def on_modified(self, event):
        logger.info("modify file:  %s", event.src_path)
        if 'config.yaml' in event.src_path:
            module.utils.core_config.cf.read()

    def on_created(self, event):
        logger.info("creat file: %s", event.src_path)


def watch():
    logger.info("init_watchdog")
    root = project_root_path()
    watch_path = root + "/config"
    config_handler = ConfigHandler()
    observer = Observer()
    observer.schedule(config_handler, watch_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(5)
            # print(module.utils.core_config.cf.get("efficient"))
            # print(module.utils.core_config.cf.get("enable_mail"))

    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def init():
    _thread.start_new_thread(watch, ())


if __name__ == "__main__":
    init()
