from talon import actions, Module
from typing import Any

mod = Module()


class Handler:
    def make_command_filter(filter_str: str):
        """Convenience method for making a filter"""
        return lambda a: a == filter_str


    ordered_action_list = [
        [
            (lambda: actions.key("shift-2"), make_command_filter("two")),
            (lambda: actions.key("shift-4"), make_command_filter("four")),
            (lambda: actions.key("shift-8"), make_command_filter("eight")),
            (lambda: actions.key("shift-9"), make_command_filter("nine")),
        ],
        [
            (lambda: actions.key("2"), make_command_filter("two")),
            (lambda: actions.key("4"), make_command_filter("four")),
            (lambda: actions.key("8"), make_command_filter("eight")),
            (lambda: actions.key("9"), make_command_filter("nine")),
        ],
        [],
        [],
    ]

    def action_called_for_region(self: Any, region: int, command: Any):
        """Calls Action Corresponding to Region but only allows one continuously held action"""
        # allows for different sounds to not trigger each other despite going to the same handler method
        for (action, command_filter) in self.ordered_action_list[region]:
            if command_filter(command):
                action()
                print(f"{command} in region {region} matches filter")
                break


handler_instance = Handler()

@mod.action_class
class Actions:
    def cast(key: str):
        """Presses mapped hotkey"""
        print(f"{key} called for casting")
        actions.user.hud_activate_virtual_key(callback_args={"target": handler_instance, "command": key})
