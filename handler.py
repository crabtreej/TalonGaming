from talon import actions
from typing import Callable
from .state import *


class Handler:
    def __init__(self):
        self.actions = []
        self.regions = {}
        self.screen_width = 1920
        self.screen_height = 1080
        
        # some convenience definitions and functions
        self.button = lambda key: lambda: actions.key(key)
        self.half_height = self.screen_height / 2 
        self.third_width = self.screen_width / 3 
        self.quarter_height = self.screen_height / 4
    
    
    def handle_action(self, command: str, region: int):
        """for each region and command pair there should be a unique action, returns a new state type if the action causes a transition"""
        for action in self.actions:
            if action.region == region and action.command == command:
                return action.handle_action()

    def cleanup(self):
        raise NotImplementedError(f"Handler {type(self)} didn't implement a cleanup explicitly!")


class Bounds:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Action:
    def __init__(self, command: str, region: int, action: Callable, bounds: Bounds):
        self.command = command
        self.region = region
        self.handle_action = action
        self.bounds = bounds
        

class MovementHandler(Handler):
    forward_held = False
    backward_held = False
    safe_walk = False
    held_keys = []
    held_command_and_region = None
    suspended_keys = []


    def __init__(self):
        super().__init__()
        self.regions = {
            0: Bounds(x=0, y=0, width=self.third_width, height=self.screen_height),
            1: Bounds(x=self.third_width, y=0, width=self.third_width, height=(self.quarter_height) * 3),
            2: Bounds(x=self.third_width, y=(self.quarter_height) * 3, width=self.third_width, height=self.quarter_height),
            3: Bounds(x=(self.third_width) * 2, y=0, width=self.third_width, height=self.screen_height)
        }
        self.actions = [
            Action('Hiss', 0, lambda: self.stationary_left_turn(), self.regions[0]),
            Action('Hiss', 1, lambda: self.safe_move_forward(), self.regions[1]),
            Action('Hiss', 2, lambda: self.safe_move_backward(), self.regions[2]),
            Action('Hiss', 3, lambda: self.stationary_right_turn(), self.regions[3]),
            Action('Sh', 0, lambda: self.toggle_move_left(), self.regions[0]),
            Action('Sh', 3, lambda: self.toggle_move_right(), self.regions[3]),
            Action('Cluck', 1, lambda: self.toggle_move_forward(), self.regions[1]),
            Action('Cluck', 2, lambda: self.toggle_move_backward(), self.regions[2]),
        ]
        self.actions.extend([Action('Suck', x, lambda: self.jump(), self.regions[x]) for x in range(4)])


    def toggle_move_forward(self):
        """Holds forward movement key"""
        print("Walking forward")
        actions.key(f"w:{'up' if self.forward_held else 'down'}")
        self.forward_held = not self.forward_held

    
    def toggle_move_backward(self):
        """Holds backward movement key"""
        actions.key(f"s:{'up' if self.backward_held else 'down'}")
        self.backward_held = not self.backward_held


    def toggle_move_left(self):
        """Holds left movement key"""
        if "a" not in self.held_keys:
            actions.key("a:down")
            self.held_keys.append("a")
            return True


    def toggle_move_right(self):
        """Holds right movement key"""
        if "d" not in self.held_keys:
            actions.key("d:down")
            self.held_keys.append("d")
            return True


    def stationary_left_turn(self):
        """Turns left while suspending forward and backward movement"""
        if "a" not in self.held_keys:
            if self.forward_held:
                actions.key("w:up")
                self.suspended_keys.append("w")
            
            if self.backward_held:
                actions.key("s:up")
                self.suspended_keys.append("s")
            return self.toggle_move_left()


    def stationary_right_turn(self):
        """Turns right while suspending forward and backward movement"""
        if "d" not in self.held_keys:
            if self.forward_held:
                actions.key("w:up")
                self.suspended_keys.append("w")
            
            if self.backward_held:
                actions.key("s:up")
                self.suspended_keys.append("s")
            return self.toggle_move_right()


    def safe_move_forward(self):
        """Turns moving into a continuous command"""
        if self.safe_walk:
            actions.key("w:down")
            self.held_keys.append("w")
            return True


    def safe_move_backward(self):
        """Turns moving into a continuous command"""
        if self.safe_walk:
            actions.key("s:down")
            self.held_keys.append("s")
            return True

    
    def set_safe_walk(self, value: bool):
        """set safe walk"""
        self.safe_walk = value


    def jump(self):
        actions.key("space")
        

    def restore_keys(self):
        """Releases held keys and re-presses suspended keys"""
        [actions.key(f"{key}:up") for key in self.held_keys]
        self.held_keys = []

        [actions.key(f"{key}:down") for key in self.suspended_keys]
        self.suspended_keys = []

        self.held_command_and_region = None

        
    def cleanup(self):
        [actions.key(f"{key}:up") for key in self.held_keys]
        self.held_keys = []
        self.suspended_keys = []
        self.held_command_and_region = None

        
    def handle_action(self, command: str, region: int):
        """Calls Action Corresponding to Region but only allows one continuously held action"""
        # a held action (e.g. hissing continuously) has to end before another one can begin, so we can be sure it's always undoing  last one
        print("movement handler called")
        if not(len(self.held_keys) == 0 and len(self.suspended_keys) == 0):
            if not (command == self.held_command_and_region[0] and region == self.held_command_and_region[1]):
                self.restore_keys()
        else:
            # allows for different sounds to not trigger each other despite going to the same handler method
            print(command)
            print(region)
            for action in self.actions:
                if action.command == command and action.region == region:
                    if action.handle_action():
                        self.held_command_and_region = (command, region)
                    print(f"{command} in region {region} matches filter")
                    break


class CastingHandler(Handler):
    def __init__(self):
        super().__init__()
        self.regions = {
            0: Bounds(x=0, y=0, width=self.third_width, height=self.half_height),
            1: Bounds(x=self.third_width, y=0, width=self.third_width, height=self.half_height),
            2: Bounds(x=self.third_width*2, y=0, width=self.third_width, height=self.half_height),
            3: Bounds(x=0, y=self.half_height, width=self.third_width, height=self.half_height),
            4: Bounds(x=self.third_width, y=self.half_height, width=self.third_width, height=self.half_height),
            5: Bounds(x=self.third_width*2, y=self.half_height, width=self.third_width, height=self.half_height)
        }

        self.actions = [
            # player buffs
            Action('Ae', 0, self.button('ctrl-shift-1'), self.regions[0]),
            Action('Ah', 0, self.button('ctrl-shift-2'), self.regions[0]),
            Action('Iy', 0, self.button('ctrl-shift-3'), self.regions[0]),
            Action('Oh', 0, self.button('ctrl-shift-4'), self.regions[0]),
            Action('U', 0, self.button('ctrl-shift-5'), self.regions[0]),
            # most common rotation
            Action('Ae', 1, self.button('1'), self.regions[1]),
            Action('Ah', 1, self.button('2'), self.regions[1]),
            Action('Iy', 1, self.button('3'), self.regions[1]),
            Action('Oh', 1, self.button('4'), self.regions[1]),
            Action('U', 1, self.button('5'), self.regions[1]),
            # random garbage
            Action('Ae', 2, self.button('q'), self.regions[2]),
            Action('Ah', 2, self.button('e'), self.regions[2]),
            Action('Iy', 2, self.button('r'), self.regions[2]),
            Action('Oh', 2, self.button('t'), self.regions[2]),
            Action('U', 2, self.button('f'), self.regions[2]),
            # heals and defensives
            Action('Ae', 3, self.button('ctrl-1'), self.regions[3]),
            Action('Ah', 3, self.button('ctrl-2'), self.regions[3]),
            Action('Iy', 3, self.button('ctrl-3'), self.regions[3]),
            Action('Oh', 3, self.button('ctrl-4'), self.regions[3]),
            Action('U', 3, self.button('ctrl-5'), self.regions[3]),
            # second most common
            Action('Ae', 4, self.button('shift-1'), self.regions[4]),
            Action('Ah', 4, self.button('shift-2'), self.regions[4]),
            Action('Iy', 4, self.button('shift-3'), self.regions[4]),
            Action('Oh', 4, self.button('shift-4'), self.regions[4]),
            Action('U', 4, self.button('shift-5'), self.regions[4]),
            # big cooldowns
            Action('Ae', 5, self.button('shift-q'), self.regions[5]),
            Action('Ah', 5, self.button('shift-e'), self.regions[5]),
            Action('Iy', 5, self.button('shift-r'), self.regions[5]),
            Action('Oh', 5, self.button('shift-t'), self.regions[5]),
            Action('U', 5, self.button('shift-f'), self.regions[5]),
        ]
    

    def cleanup(self):
        """Providing default implementation for cleanup"""
        pass
        

class MiscellaneousHandler(Handler):
    def __init__(self):
        super().__init__()
        self.regions = {
            0: Bounds(x=0, y=0, width=self.third_width, height=self.screen_height)
        }
        self.actions = [
            Action('Cluck', 0, lambda: actions.key('tab'), self.regions[0])
        ]

    
    def cleanup(self):
        """Providing default implementation for cleanup"""
        pass
        

class MoveCastMiscTransitionHandler(Handler):
    def __init__(self):
        super().__init__()
        self.regions = {
            0: Bounds(x=0, y=0, width=self.third_width, height=self.screen_height),
            1: Bounds(x=self.third_width, y=0, width=self.third_width, height=(self.quarter_height) * 3),
            2: Bounds(x=self.third_width, y=(self.quarter_height) * 3, width=self.third_width, height=self.quarter_height),
            3: Bounds(x=(self.third_width) * 2, y=0, width=self.third_width, height=self.screen_height)
        }
        self.actions = [
            Action('Cluck', 0, lambda: ChatState, self.regions[0]),
            Action('Whistle', 1, lambda: MenusState, self.regions[1]),
            Action('Whistle', 2, lambda: actions.user.return_to_command_mode(), self.regions[2]),
        ]

    
    def cleanup(self):
        """Providing default implementation for cleanup"""
        pass
        

class MenusHandler(Handler):
    def __init__(self):
        super().__init__()
        self.regions = {
            0: Bounds(x=0, y=0, width=self.screen_width, height=self.screen_height / 2),
            1: Bounds(x=0, y=self.screen_height / 2, width=self.screen_width, height=self.screen_height / 2)
        }
        self.pressed = {}
        def action(b):
            self.pressed[b] = (not self.pressed[b]) if b in self.pressed else True
            actions.key(b)


        self.actions = [
            Action('Ae', 0, action('b'), self.regions[0]),
            Action('Ah', 0, action('c'), self.regions[0]),
            Action('Iy', 0, action('p'), self.regions[0]),
            Action('Oh', 0, action('n'), self.regions[0]),
            Action('U', 0, action('l'), self.regions[0]),
            Action('Ae', 1, action('o'), self.regions[1]),
            Action('Ah', 1, action('i'), self.regions[1]),
            Action('Iy', 1, action('escape'), self.regions[1]),
            Action('Oh', 1, action('m'), self.regions[1]),
            Action('U', 1, action('shift-p'), self.regions[1]),
        ]

    
    def cleanup(self):
        """Providing default implementation for cleanup"""
        # may want to make this conditional on whether or not any menus were opened
        if True in self.pressed.values():
            actions.key('escape')
        

class MenusTransitionHandler(Handler):
    def __init__(self):
        super().__init__()
        self.regions = {
            0: Bounds(x=0, y=0, width=self.screen_width, height=self.screen_height)
        }
        self.actions = [Action('Whistle', 0, lambda: MoveCastMiscState, self.regions[0])]

    
    def cleanup(self):
        """Providing default implementation for cleanup"""
        pass
        

class SubmenusHandler(Handler):
    def __init__(self):
        super().__init__()
        self.actions = []
        self.regions = {}

    
    def cleanup(self):
        """Providing default implementation for cleanup"""
        pass
        

class SubmenusTransitionHandler(Handler):
    def __init__(self):
        super().__init__()
        self.actions = []
        self.regions = {}

    
    def cleanup(self):
        """Providing default implementation for cleanup"""
        pass
        

class ChatHandler(Handler):
    def __init__(self):
        super().__init__()
        self.regions = {
            0: Bounds(x=0, y=0, width=self.screen_width / 2, height=self.screen_height),
            1: Bounds(x=self.screen_width / 2, y=0, width=self.screen_width / 2, height=self.screen_height),
        }

        self.dictating = False

        def open_chat(channel):
            if not self.dictating:
                actions.key('enter')
                actions.insert(f"/{channel} ")
                self.dictating = True
                actions.mode.enable("command")
        

        def send():
            if self.dictating:
                actions.key('enter')
                self.dictating = False
                actions.mode.disable("command")


        self.actions = [
            Action('Ae', 0, open_chat('p'), self.regions[0]),
            Action('Ah', 0, open_chat('s'), self.regions[0]),
            Action('Iy', 0, open_chat('g'), self.regions[0]),
            Action('Oh', 0, open_chat('2'), self.regions[0]),
            Action('U', 0, open_chat('r'), self.regions[0]),
            Action('Ae', 1, open_chat('1'), self.regions[1]),
            Action('Ah', 1, open_chat('w'), self.regions[1]),
            Action('Iy', 1, open_chat('e'), self.regions[1]),
            Action('Oh', 1, open_chat('y'), self.regions[1]),
            Action('U', 1, open_chat('raid'), self.regions[1]),
            Action('Cluck', 0, send, self.regions[0]),
            Action('Cluck', 1, send, self.regions[1]),
            Action('Suck', 0, self.back_out, self.regions[0]),
            Action('Suck', 1, self.back_out, self.regions[1]),
        ]


    def back_out():
        if self.dictating:
            actions.edit.delete_line()
            actions.key('enter')
            actions.mode.disable("command")
            self.dictating = False

    
    def cleanup(self):
        """Providing default implementation for cleanup"""
        self.back_out()

        
class ChatTransitionHandler(Handler):
    def __init__(self):
        super().__init__()
        self.regions = {
            Bounds(x=0, y=0, width=self.screen_width, height=self.screen_height)
        }
        self.actions = [
            Action('Whistle', 0, lambda: MoveCastMiscState, self.regions[0])
        ]

    
    def cleanup(self):
        """Providing default implementation for cleanup"""
        pass
        
