from talon import actions, Module, app, scope, noise, ctrl
from typing import Any
from .state_machine import *
from talon.lib import cubeb

ctx = cubeb.Context()
mod = Module()
mod.mode("warcraft", desc="Mode for controlling world of warcraft")
mod.mode("discordwow", desc="Mode for speaking and discord without any commands")
state_machine = None

def in_mode(mode):
    active_modes = scope.get("mode")
    return mode in active_modes

@mod.action_class
class Actions:
    def enter_warcraft_mode():
        """Presses discord mute hotkey and starts warcraft mode"""
        global state_machine

        if not state_machine:
            state_machine = StateMachine()
        elif not in_mode('user.discordwow'):
            state_machine.restart()

        if in_mode('user.discordwow'):
            actions.key("f10")
            devices = [
                dev.name for dev in ctx.inputs() if dev.state == cubeb.DeviceState.ENABLED
            ]
            microphone = next((x for x in devices if 'Shure' in x))
            actions.sound.set_microphone(microphone)

        actions.mode.disable("command")
        actions.mode.disable("user.discordwow")
        actions.mode.enable("user.warcraft")
        

    def enter_discord_mode():
        """Toggles discord mute and disables warcraft mode"""
        actions.mode.disable("command")
        actions.mode.disable("user.warcraft")
        actions.mode.enable("user.discordwow")
        actions.key("f10")
        actions.sound.set_microphone("None")


    def return_to_command_mode():
        """Toggles mute off and goes back to normal talon mode"""
        if in_mode('user.discordwow'):
            actions.key("f10")

        actions.user.hud_set_virtual_keyboard(None)
        actions.user.hud_disable_id('Text panel')
        actions.mode.disable("user.discordwow")
        actions.mode.disable("user.warcraft")
        actions.mode.enable("command")


    def warcraft_mode_pop():
        """Disables mouse movement before triggering pop so it doesn't turn the camera around"""
        if in_mode('user.warcraft'):
            actions.tracking.control_toggle(False)
            ctrl.mouse_click(button=0, hold=16000)
            actions.tracking.control_toggle(True)

noise.register("pop", lambda _: actions.user.warcraft_mode_pop())
