from talon import actions, Module, app, scope, noise
from typing import Any
from .state_machine import *
from talon.lib import cubeb

ctx = cubeb.Context()
mod = Module()
mod.mode("warcraft", desc="Mode for controlling world of warcraft")
state_machine = None


@mod.action_class
class Actions:
    def enter_warcraft_mode():
        """Creates or restarts the state machine, intended to be called from command mode"""
        global state_machine

        if not state_machine:
            state_machine = StateMachine()
        else:
            state_machine.restart()

        actions.mode.disable("command")
        actions.mode.enable("user.warcraft")


    def warcraft_mode_pop():
        """Disables mouse movement before triggering pop so it doesn't turn the camera around"""
        if 'user.warcraft' in scope.get("mode"):
            actions.tracking.control_toggle(False)
            actions.sleep('16ms')
            actions.mouse_click()
            actions.sleep('16ms')
            actions.tracking.control_toggle(True)


def discord_callback():
    actions.user.register_enter_exit_callbacks("user.warcraft", lambda: actions.mode.disable("user.warcraft"), lambda: actions.mode.enable("user.warcraft"))


noise.register("pop", lambda _: actions.user.warcraft_mode_pop())
app.register("ready", lambda: discord_callback())