import rumps
from datetime import datetime, timedelta
from enum import Enum
from configparser import ConfigParser
import global_memory
from system_wakes_daemon import SystemWakesDaemon

# Consts
APP_NAME = 'Take a break'
CONFIG_FILE = 'config.INI'
BREAK_NOTIFICATION_MESSAGE = 'It\'s time for a little break!'
CMD_TIME_FORMAT = '%Y-%m-%d'


# Application states
class State(Enum):
    WORK = 0
    BREAK = 1


class Application(rumps.App):
    def __init__(self, config):
        super().__init__(APP_NAME)
        self.state_seconds_counter = 0
        self.state = State.WORK
        self.start_datetime = datetime.now()
        self.config = config

    def calculate_current_state_seconds_left(self):
        if self.state == State.WORK:
            return float(self.config['DEFAULT']['WORK_TIME']) * 60 - self.state_seconds_counter + 1
        elif self.state == State.BREAK:
            return float(self.config['DEFAULT']['BREAK_TIME']) * 60 - self.state_seconds_counter + 1

    def restart_to_state(self, state):
        self.state_seconds_counter = 0
        self.state = state

    def tick(self):
        self.state_seconds_counter += 1

        seconds_left = self.calculate_current_state_seconds_left()
        if self.state == State.WORK:
            self.title = f"🧑🏻‍💻 [W] {format_seconds(seconds_left)}"

            if not seconds_left:
                self.restart_to_state(State.BREAK)
                print('asd')
                rumps.notification('', BREAK_NOTIFICATION_MESSAGE, '')
        else:
            self.title = f"💤 [B] {format_seconds(seconds_left)}"

            if not seconds_left:
                self.restart_to_state(State.WORK)

        local_last_system_wake = global_memory.last_system_wake  # thread safe

        if local_last_system_wake and local_last_system_wake > self.start_datetime:
            self.restart_to_state(State.WORK)
            self.start_datetime = local_last_system_wake

    @rumps.timer(1)
    def update(self, _):
        self.tick()

    @rumps.clicked('Restart work timer')
    def restart(self, _):
        self.restart_to_state(State.WORK)


def format_seconds(s):
    return ":".join(str(timedelta(seconds=s)).split(':')[1:])


def read_config():
    config = ConfigParser()
    config.read(CONFIG_FILE)
    return config


def run():
    config = read_config()
    SystemWakesDaemon(config).start()
    Application(config).run()


if __name__ == "__main__":
    run()
