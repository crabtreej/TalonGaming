from talon import actions, Module, cron
from typing import Any


mod = Module()

class Handler:
    held_keys = []
    held_region = None

    def press_keys(self: Any, keys: str):
        """whatever"""
        for key in keys:
            if key not in self.held_keys:
                actions.key(f"{key}:down")
                self.held_keys.append(key)

    def restore_keys(self: Any):
        """Releases held keys and re-presses suspended keys"""
        [actions.key(f"{key}:up") for key in self.held_keys]
        self.held_keys = []
        self.held_region = None

    keys_for_region = [
        "wa", "wd", "", "as", "ds"
    ]

    def action_called_for_region(self: Any, region: int, command: Any):
        """Calls Action Corresponding to Region but only allows one continuously held action"""
        # a held action (e.g. hissing continuously) has to end before another one can begin, so we can be sure it's always undoing  last one
        if ":repeat" in command and self.held_region is not None:
            if not (region == self.held_region):
                print("region changed, dropping command and starting new one")
                self.restore_keys()
                self.press_keys(self.keys_for_region[region])
                self.held_region = region
        else:
            self.press_keys(self.keys_for_region[region])
            self.held_region = region

handler_instance = Handler()

@mod.action_class
class Actions:
    def move_camera_command(command: str):
        """Sends event to activate virtual key"""
        #print("got command to move")
        actions.user.hud_activate_virtual_key(callback_args={"target": handler_instance, "command": command})

    def stop_camera():
        """Stops camera panning"""
        handler_instance.restore_keys()
