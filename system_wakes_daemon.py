from subprocess import run
from datetime import datetime
from threading import Thread
from time import sleep
import global_memory

# Consts
SYSTEM_WAKES_CMD = 'pmset -g log|grep " Wake  "'
WAKES_DT_FORMAT = '%Y-%m-%d %H:%M:%S'


def _find_latest_system_wake():
    # Last element is blank line, take penultimate.
    result = run(SYSTEM_WAKES_CMD, capture_output=True, shell=True).stdout.decode().split('\n')[-2]
    tmp = result.split(' ')

    global_memory.last_system_wake = datetime.strptime(f'{tmp[0]} {tmp[1]}', WAKES_DT_FORMAT)


class SystemWakesDaemon(Thread):
    def __init__(self, config):
        super().__init__(daemon=True)
        self.config = config

    def _get_system_wakes_check_interval(self):
        return float(self.config['DEFAULT']['SYSTEM_WAKES_CHECK_INTERVAL']) * 60

    def run(self):
        while True:
            _find_latest_system_wake()
            sleep(self._get_system_wakes_check_interval())
