import sys
import time
from talon import actions, cron
from telemetrix import telemetrix

# Callback data indices
CB_PIN_MODE = 0
CB_PIN = 1
CB_VALUE = 2
CB_TIME = 3

forward, backward, left, right = 5, 6, 4, 3
grace_time_milliseconds = 60


class PinInformation:
    def __init__(self, key, pin):
        self.key = key
        self.pin = pin
        self.callback = lambda data: the_callback(data, self)
        self.last_ignored_value_cron = None
        self.last_change_time = time.time() * 1000
        self.last_set_value = 0

def update_key(data, pin_info):
    current_time = time.time() * 1000
    if pin_info.last_ignored_value_cron:
        cron.cancel(pin_info.last_ignored_value_cron)
        pin_info.last_ignored_value_cron = None

    if data[CB_VALUE] != pin_info.last_set_value:
        actions.key(f'{pin_info.key}:{"down" if data[CB_VALUE] == 1 else "up"}')
        pin_info.last_change_time = current_time
        pin_info.last_set_value = data[CB_VALUE]


def the_callback(data, pin_info: PinInformation):
    """
    :param data: [pin, current reported value, pin_mode, timestamp]
    """
    current_time = time.time() * 1000
    if current_time - pin_info.last_change_time > grace_time_milliseconds:
        update_key(data, pin_info)
    else:
        if pin_info.last_ignored_value_cron:
            cron.cancel(pin_info.last_ignored_value_cron)
            pin_info.last_ignored_value_cron = None

        pin_info.last_ignored_value_cron = cron.after("60ms", lambda: update_key(data, pin_info))


def digital_in(my_board, pin_info):
    my_board.set_pin_mode_digital_input(pin_info.pin, callback=pin_info.callback)


board = telemetrix.Telemetrix()
digital_in(board, PinInformation("w", forward))
digital_in(board, PinInformation("s", backward))
digital_in(board, PinInformation("a", left))
digital_in(board, PinInformation("d", right))
