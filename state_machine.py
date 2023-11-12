from talon import actions, Module, app
from .common import intersects
from .state import *


global run_sanity_check
run_sanity_check = False
mod = Module()


class StateMachine:
    should_handle = True
    states = [MoveCastMiscState, MenusState, SubmenusState, ChatState]
    
    def __init__(self):
        """Initialize an instance of our base state and run the sanity check if desired"""
        if run_sanity_check:
            self.sanity_check()
        print("Setting up state machine")
        self.active_state = MoveCastMiscState(self)
        print("State machine configured")

    
    def sanity_check(self):
        """Checks up for all handlers that can be active at the same time that none of their commands and regions simultaneously overlap"""
        global run_sanity_check
        run_sanity_check = False
        for state in self.states:
            s = state(self)
            for i in range(len(s.handlers)):
                handler1 = s.handlers[i]
                for j in range(i + 1, len(s.handlers)):
                    handler2 = s.handlers[j]
                    for action_pair in [(action1, action2) for action1 in handler1.actions for action2 in handler2.actions]:
                        if action_pair[0].command == action_pair[1].command:
                            if intersects(action_pair[0].bounds, action_pair[1].bounds):
                                raise Exception(f"{action_pair[0].command} and {action_pair[1].command} intersect in both region and command in handlers {type(handler_pair[0])}, {type(handler_pair[1])}!")


    def transition(self, next_state: State):
        self.active_state.cleanup(future_state)
        self.active_state = future_state

    
    def handle_action(self, command: str, region: int):
        print("State machine received action")
        future_state = self.active_state.handle_action(command, region)
        if future_state: 
            self.transition(future_state)

    
    def deactivate(self):
        self.active_state.cleanup(None)
        actions.user.hud_set_virtual_keyboard(None)


@mod.action_class
class ParrotAction:
    def handle_parrot_action(command: str):
        """ handles any parrot action by pushing it to the state machine """
        actions.user.hud_activate_virtual_key(callback_args={"command": command})
