from talon import actions, Module, app
from typing import Any
from ..state_machine import *

mod = Module()
mod.mode("warcraftnew", desc="Mode for controlling world of warcraft")
mod.mode("discordwow", desc="Mode for speaking and discord without any commands")
#mod.mode("warcraftmenus", desc="Mode for accessing menus in wow")
in_discord_mode = True

@mod.action_class
class Actions:
    def enter_warcraft_mode():
        """Presses discord mute hotkey and starts warcraft mode"""
        if not self.state_machine:
            self.state_machine = StateMachine()

        global in_discord_mode
        if in_discord_mode:
            actions.key("f10")
            in_discord_mode = False

        actions.mode.disable("command")
        actions.mode.disable("user.discordwow")
        #actions.mode.disable("user.warcraftmenus")
        print("entered warcraft mode")
        actions.mode.enable("user.warcraftnew")
        
    def enter_menus_mode():
        """Goes to menu mode"""
        global in_discord_mode
        if in_discord_mode:
            actions.key("f10")
            is_discord_mode = False

        actions.mode.disable("command")
        actions.mode.disable("user.discordwow")
        actions.mode.disable("user.warcraftnew")
        #actions.mode.enable("user.warcraftmenus")

    def enter_discord_mode():
        """Toggles discord mute and disables warcraft mode"""
        global in_discord_mode
        actions.mode.disable("command")
        actions.mode.disable("user.warcraftnew")
        #actions.mode.disable("user.warcraftmenus")
        actions.mode.enable("user.discordwow")
        actions.key("f10")
        in_discord_mode = True

    def return_to_command_mode():
        """Toggles mute off and goes back to normal talon mode"""
        global in_discord_mode
        if self.state_machine:
            self.state_machine.deactivate()
            self.state_machine = None

        if in_discord_mode:
            actions.key("f10")
            in_discord_mode = False

        actions.mode.disable("user.discordwow")
        actions.mode.disable("user.warcraftnew")
        #actions.mode.disable("user.warcraftmenus")
        actions.mode.enable("command")
