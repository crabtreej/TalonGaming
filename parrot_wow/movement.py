from talon import actions, Module
from typing import Any


mod = Module()

class Handler:
    forward_held = False
    backward_held = False
    held_keys = []

    def toggle_move_forward(self: Any):
        """Holds forward movement key"""
        actions.key(f"w:{'up' if self.forward_held else 'down'}")
        self.forward_held = not self.forward_held
    
    def toggle_move_backward(self: Any):
        """Holds backward movement key"""
        actions.key(f"s:{'up' if self.backward_held else 'down'}")
        self.backward_held = not self.backward_held

    def toggle_move_left(self: Any):
        """Holds left movement key"""
        actions.key("a:down")
        actions.key("\\")
        self.held_keys.append("a")
        self.held_keys.append("\\")

    def toggle_move_right(self: Any):
        """Holds right movement key"""
        actions.key("d:down")
        actions.key("\\")
        self.held_keys.append("d")
        self.held_keys.append("\\")

    def stop_movement(self: Any):
        """Releases all movement keys"""
        actions.key("w:up")
        actions.key("s:up")
        actions.key("a:up")
        actions.key("d:up")
        self.forward_held = False
        self.backward_held = False
        self.drop_held_keys()

    def drop_held_keys(self: Any):
        [actions.key(f"{key}:up") for key in self.held_keys]
        self.held_keys = []

    ordered_action_list = [
        (toggle_move_left, lambda a: a == "hiss"),
        (toggle_move_forward, lambda a: a == "pop"),
        (toggle_move_backward, lambda a: a == "pop"),
        (toggle_move_right, lambda a: a == "hiss"),
    ]

    def action_called_for_region(self: Any, region: int, command: Any):
        """Calls Action Corresponding to Region but only allows one continuously held action"""
        # a held action (e.g. hissing continuously) has to end before another one can begin, so we can be sure it's always undoing the last one
        if not(len(self.held_keys) == 0):
            self.drop_held_keys()
        else:
            # allows for different sounds to not trigger each other despite going to the same handler method
            action, command_filter = self.ordered_action_list[region]
            if command_filter(command):
                action(self) 
            else: 
                print(f"{command} in region {region} doesn't match filter")



handler_instance = Handler()


@mod.action_class
class Actions:
    def move_in_direction(command: str):
        """Sends event to activate virtual key"""
        print("got command to move")
        actions.user.hud_activate_virtual_key(callback_args={"target": handler_instance, "command": command})

    def stop_movement():
        """Releases all movement keys"""
        handler_instance.stop_movement()

        