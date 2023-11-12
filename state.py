from talon import actions
from .handler import *

class State:
    def __init__(self, machine):
        self.machine = machine
        self.handlers = []
    

    def handle_action(self, command: str, region: int):
        """Asks each handler to handle the action. This is safe because the sanity check will confirm that multiple won't handle the same action"""
        for handler in self.handlers:
            next_state = handler.handle_action(command, region)
            if next_state:
                return next_state


    def cleanup(self, next_state):
        """Calls cleanup on the handlers to reset any held keys, etc."""
        for handler in self.handlers:
            handler.cleanup()

    
    def register_keyboard(self, keyboard_name):
        keys = []
        for handler in self.handlers:
            for region, bounds in handler.regions.items():
                keys.append(actions.user.hud_create_virtual_key(self.machine.handle_action, x=bounds.x, y=bounds.y, width=bounds.width, height=bounds.height, action_args={"region": region}))
        actions.user.hud_register_virtual_keyboard(keyboard_name, keys)
        actions.user.hud_set_virtual_keyboard(keyboard_name)


class MoveCastMiscState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.handlers = [MovementHandler(), CastingHandler(), MiscellaneousHandler(), MoveCastMiscTransitionHandler()]
        self.register_keyboard('MoveCastMiscStateKeyboard')


    def handle_action(self, command: str, region: int):
        """Each state should have a special escape action to move back to a 'higher' state"""
        return super().handle_action(command, region)
        

class MenusState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.handlers = [MenusHandler(), MovementHandler(), MenusTransitionHandler()]
        self.register_keyboard('MenusStateKeyboard')


    def handle_action(self, command: str, region: int):
        """Each state should have a special escape action to move back to a 'higher' state"""
        return super().handle_action(command, region)


class SubmenusState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.handlers = [SubmenusHandler(), MovementHandler(), SubmenusTransitionHandler()]
        self.register_keyboard('SubmenusStateKeyboard')


    def handle_action(self, command: str, region: int):
        """Each state should have a special escape action to move back to a 'higher' state"""
        return super().handle_action(command, region)


class ChatState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.handlers = [ChatHandler(), ChatTransitionHandler()]
        self.register_keyboard('ChatStateKeyboard')



    def handle_action(self, command: str, region: int):
        """Each state should have a special escape action to move back to a 'higher' state"""
        return super().handle_action(command, region)
