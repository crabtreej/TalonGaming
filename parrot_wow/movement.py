from talon import actions, Module
from typing import Any


mod = Module()

class Handler:
    forward_held = False
    backward_held = False
    safe_walk = False
    held_keys = []
    suspended_keys = []

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
        self.held_keys.append("a")

    def toggle_move_right(self: Any):
        """Holds right movement key"""
        actions.key("d:down")
        self.held_keys.append("d")

    def stationary_left_turn(self: Any):
        """Turns left while suspending forward and backward movement"""
        if self.forward_held:
            actions.key("w:up")
            self.suspended_keys.append("w")
        
        if self.backward_held:
            actions.key("s:up")
            self.suspended_keys.append("s")
        self.toggle_move_left()

    def stationary_right_turn(self: Any):
        """Turns right while suspending forward and backward movement"""
        if self.forward_held:
            actions.key("w:up")
            self.suspended_keys.append("w")
        
        if self.backward_held:
            actions.key("s:up")
            self.suspended_keys.append("s")
        self.toggle_move_right()

    def safe_move_forward(self: Any):
        """Turns moving into a continuous command"""
        if self.safe_walk:
            actions.key("w:down")
            self.held_keys.append("w")

    def safe_move_backward(self: Any):
        """Turns moving into a continuous command"""
        if self.safe_walk:
            actions.key("s:down")
            self.held_keys.append("s")
    
    def stop_movement(self: Any):
        """Releases all movement keys"""
        actions.key("w:up")
        actions.key("s:up")
        actions.key("a:up")
        actions.key("d:up")
        self.forward_held = False
        self.backward_held = False
        set_safe_walk(False)
        self.drop_held_keys()

    def set_safe_walk(self: Any, value: bool):
        """set safe walk"""
        self.safe_walk = value

    def restore_keys(self: Any):
        """Releases held keys and re-presses suspended keys"""
        [actions.key(f"{key}:up") for key in self.held_keys]
        self.held_keys = []
        
        [actions.key(f"{key}:down") for key in self.suspended_keys]
        self.suspended_keys = []

    def make_command_filter(filter_str: str):
        """Convenience method for making a filter"""
        return lambda a: a == filter_str


    ordered_action_list = [
        [(toggle_move_left, make_command_filter("hiss")), (stationary_left_turn, make_command_filter("long_e"))],
        [(toggle_move_forward, make_command_filter("clack")), (safe_move_forward, make_command_filter("hiss"))],
        [(toggle_move_backward, make_command_filter("clack")), (safe_move_backward, make_command_filter("hiss")), (() => actions.key("space"), make_command_filter("space"))],
        [(toggle_move_right, make_command_filter("hiss")), (stationary_right_turn, make_command_filter("long_e"))],
    ]

    def action_called_for_region(self: Any, region: int, command: Any):
        """Calls Action Corresponding to Region but only allows one continuously held action"""
        # a held action (e.g. hissing continuously) has to end before another one can begin, so we can be sure it's always undoing  last one
        if not(len(self.held_keys) == 0 and len(self.suspended_keys) == 0):
            self.restore_keys()
        else:
            # allows for different sounds to not trigger each other despite going to the same handler method
            for (action, command_filter) in self.ordered_action_list[region]:
                if command_filter(command):
                    action(self)
                    print(f"{command} in region {region} matches filter")
                    break


handler_instance = Handler()


@mod.action_class
class Actions:
    def movement_command(command: str):
        """Sends event to activate virtual key"""
        print("got command to move")
        actions.user.hud_activate_virtual_key(callback_args={"target": handler_instance, "command": command})

    def stop_movement():
        """Releases all movement keys"""
        handler_instance.stop_movement()
 
    def set_safe_walk(value: bool):
        """set Safe Walking Mode"""
        handler_instance.set_safe_walk(value)