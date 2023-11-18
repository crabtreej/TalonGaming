from talon import actions
from .handler import *


class State:
    def __init__(self, machine):
        self.machine = machine
        self.handlers = []
        from .handler import Handler
    

    def handle_action(self, command: str, region: int, intended_handler: Handler):
        """Asks each handler to handle the action. This is safe because the sanity check will confirm that multiple won't handle the same action"""
        for handler in self.handlers:
            if intended_handler is handler:
                return handler.handle_action(command, region)


    def cleanup(self, next_state):
        """Calls cleanup on the handlers to reset any held keys, etc."""
        for handler in self.handlers:
            handler.cleanup()

    
    def register_keyboard(self, keyboard_name):
        keys = []
        for handler in self.handlers:
            for region, bounds in handler.regions.items():
                keys.append(actions.user.hud_create_virtual_key(self.machine.handle_action, x=bounds.x, y=bounds.y, width=bounds.width, height=bounds.height, action_args={"region": region, "handler": handler}))
        actions.user.hud_register_virtual_keyboard(keyboard_name, keys)


class MoveCastMiscState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.handlers = [MovementHandler(), CastingHandler(), MiscellaneousHandler(), MoveCastMiscTransitionHandler()]
        self.keyboard_name = 'MoveCastMiscStateKeyboard'
        self.state_title = 'Movement State'
        self.register_keyboard(self.keyboard_name)


    def handle_action(self, command: str, region: int, handler: Handler):
        """Each state should have a special escape action to move back to a 'higher' state"""
        return super().handle_action(command, region, handler)
        

class MenusState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.handlers = [MenusHandler(), MovementHandler(), MenusTransitionHandler()]
        self.keyboard_name = 'MenusStappteKeyboard'
        self.state_title = 'Menus State'
        self.register_keyboard(self.keyboard_name)


    def handle_action(self, command: str, region: int, handler: Handler):
        """Each state should have a special escape action to move back to a 'higher' state"""
        return super().handle_action(command, region, handler)


class SubmenusState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.handlers = [SubmenusHandler(), MovementHandler(), SubmenusTransitionHandler()]
        self.keyboard_name = 'SubmenusStateKeyboard'
        self.state_title = 'Submenus State'
        self.register_keyboard(self.keyboard_name)


    def handle_action(self, command: str, region: int, handler: Handler):
        """Each state should have a special escape action to move back to a 'higher' state"""
        return super().handle_action(command, region, handler)


class ChatState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.handlers = [ChatHandler(), ChatTransitionHandler()]
        self.keyboard_name = 'ChatStateKeyboard'
        self.state_title = 'Chat State'
        self.register_keyboard(self.keyboard_name)


    def handle_action(self, command: str, region: int, handler: Handler):
        """Each state should have a special escape action to move back to a 'higher' state"""
        return super().handle_action(command, region, handler)
