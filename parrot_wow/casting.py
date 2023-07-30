from talon import actions, Module
from typing import Any

mod = Module()


class Handler:
    def make_command_filter(filter_str: str):
        """Convenience method for making a filter"""
        return lambda a: a == filter_str


    action_map = [
        [
            (lambda: actions.key("shift-1"), make_command_filter("one")),
            (lambda: actions.key("shift-2"), make_command_filter("two")),
            (lambda: actions.key("shift-3"), make_command_filter("three")),
            (lambda: actions.key("shift-4"), make_command_filter("four")),
            (lambda: actions.key("shift-5"), make_command_filter("eight")),
            (lambda: actions.key("shift-6"), make_command_filter("nine")),
        ],
        [
            (lambda: actions.key(1), make_command_filter("one")),
            (lambda: actions.key(2), make_command_filter("two")),
            (lambda: actions.key(3), make_command_filter("three")),
            (lambda: actions.key(4), make_command_filter("four")),
            (lambda: actions.key(5), make_command_filter("eight")),
            (lambda: actions.key(6), make_command_filter("nine")),
        ],
        [],
        [],
    ]


handler_instance = Handler()

@mod.action_class
class Actions:
    def cast(key: int):
        """Presses mapped hotkey"""
        actions.user.hud_to_activate_virtual_key(callback_args={"target": handler_instance, "command": key})
