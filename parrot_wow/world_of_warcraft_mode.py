from talon import actions, Module, app
from typing import Any

mod = Module()
mod.mode("warcraft", desc="Mode for controlling world of warcraft")
mod.mode("discordwow", desc="Mode for speaking and discord without any commands")
mod.mode("warcraftmenus", desc="Mode for accessing menus in wow")
in_discord_mode = True

@mod.action_class
class Actions:
    def enter_warcraft_mode():
        """Presses discord mute hotkey and starts warcraft mode"""
        global in_discord_mode
        if in_discord_mode:
            actions.key("f10")
            in_discord_mode = False
        actions.mode.disable("command")
        actions.mode.disable("user.discordwow")
        actions.mode.disable("user.warcraftmenus")
        actions.mode.enable("user.warcraft")
        
    def enter_menus_mode():
        """Goes to menu milmode"""
        global in_discord_mode
        if in_discord_mode:
            actions.key("f10")
            is_discord_mode = False
        actions.mode.disable("command")
        actions.mode.disable("user.discordwow")
        actions.mode.disable("user.warcraft")
        actions.mode.enable("user.warcraftmenus")

    def enter_discord_mode():
        """Toggles discord mute and disables warcraft mode"""
        global in_discord_mode
        actions.mode.disable("command")
        actions.mode.disable("user.warcraft")
        actions.mode.disable("user.warcraftmenus")
        actions.mode.enable("user.discordwow")
        actions.key("f10")
        in_discord_mode = True

    def return_to_command_mode():
        """Toggles mute off and goes back to normal talon mode"""
        global in_discord_mode
        actions.mode.disable("user.discordwow")
        actions.mode.disable("user.warcraft")
        actions.mode.disable("user.warcraftmenus")
        actions.mode.enable("command")
        if in_discord_mode:
            actions.key("f10")
            in_discord_mode = False

    # action_args (from call to hud_create_virtual_key) and callback_args get joined together and passed into this method
    def virtual_key_region_activated(target: Any, region: int, command: Any):
        """Activates action for region on target"""
        print(f"keyboard action for region {region} called by command {command}")
        target.action_called_for_region(region, command)


def register_virtual_keyboard():
    """Creates a four region virtual keyboard with talon HUD to extend number of keys available and make movement easier"""
    keys =[
        actions.user.hud_create_virtual_key(actions.user.virtual_key_region_activated, x=0, y=0, width=640, height=1080, action_args={"region": 0}),
        actions.user.hud_create_virtual_key(actions.user.virtual_key_region_activated, x=640, y=0, width=640, height=810, action_args={"region": 1}),
        actions.user.hud_create_virtual_key(actions.user.virtual_key_region_activated, x=640, y=810, width=640, height=270, action_args={"region": 2}),
        actions.user.hud_create_virtual_key(actions.user.virtual_key_region_activated, x=1280, y=0, width=640, height=1080, action_args={"region": 3}),
    ]
    print("Setting up keys")
    actions.user.hud_register_virtual_keyboard('warcraft_keyboard', keys)
    actions.user.hud_set_virtual_keyboard('warcraft_keyboard')

app.register('ready', register_virtual_keyboard)