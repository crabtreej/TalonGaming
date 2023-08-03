from talon import actions, Module, app
from typing import Any

mod = Module()
mod.mode("discordbaldur", desc="Mode for speaking and discord without any commands")
mod.mode("baldur", desc="Mode for playing baldur's gate")
in_discord_mode = True

@mod.action_class
class Actions:
    def enter_baldur_mode():
        """Presses discord mute hotkey and starts baldur mode"""
        global in_discord_mode
        if in_discord_mode:
            actions.key("f10")
            in_discord_mode = False
        actions.mode.disable("command")
        actions.mode.disable("user.discordbaldur")
        actions.mode.enable("user.baldur")

    def enter_discord_mode_baldur():
        """Toggles discord mute and disables baldur mode"""
        global in_discord_mode
        actions.mode.disable("command")
        actions.mode.disable("user.baldur")
        actions.mode.enable("user.discordbaldur")
        actions.key("f10")
        in_discord_mode = True

    def return_to_command_mode_baldur():
        """Toggles mute off and goes back to normal talon mode"""
        global in_discord_mode
        actions.mode.disable("user.discordbaldur")
        actions.mode.disable("user.baldur")
        actions.mode.enable("command")
        if in_discord_mode:
            actions.key("f10")
            in_discord_mode = False