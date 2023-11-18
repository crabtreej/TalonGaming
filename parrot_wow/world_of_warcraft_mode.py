from talon import actions, Module, app
from typing import Any
from .state_machine import *
from talon.lib import cubeb

ctx = cubeb.Context()
mod = Module()
mod.mode("warcraft", desc="Mode for controlling world of warcraft")
mod.mode("discordwow", desc="Mode for speaking and discord without any commands")
in_discord_mode = True
state_machine = None


@mod.action_class
class Actions:
    def enter_warcraft_mode():
        """Presses discord mute hotkey and starts warcraft mode"""
        global state_machine
        global in_discord_mode

        if not state_machine:
            state_machine = StateMachine()
        elif not in_discord_mode:
            state_machine.restart()

        if in_discord_mode:
            actions.key("f10")
            in_discord_mode = False
            devices = [
                dev.name for dev in ctx.inputs() if dev.state == cubeb.DeviceState.ENABLED
            ]
            microphone = next((x for x in devices if 'Shure' in x), "System Default")
            actions.sound.set_microphone(microphone)

        actions.mode.disable("command")
        actions.mode.disable("user.discordwow")
        actions.mode.enable("user.warcraft")
        

    def enter_discord_mode():
        """Toggles discord mute and disables warcraft mode"""
        global in_discord_mode
        actions.mode.disable("command")
        actions.mode.disable("user.warcraft")
        actions.mode.enable("user.discordwow")
        actions.key("f10")
        in_discord_mode = True
        actions.sound.set_microphone("None")


    def return_to_command_mode():
        """Toggles mute off and goes back to normal talon mode"""
        global in_discord_mode
        
        if in_discord_mode:
            actions.key("f10")
            in_discord_mode = False

        actions.user.hud_set_virtual_keyboard(None)
        print("this is running")
        actions.user.hud_publish_content(None, "Current state", None, show=False)
        actions.mode.disable("user.discordwow")
        actions.mode.disable("user.warcraft")
        actions.mode.enable("command")
