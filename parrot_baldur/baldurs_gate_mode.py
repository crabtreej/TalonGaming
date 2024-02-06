from talon import actions, Module, app
from typing import Any

mod = Module()
mod.mode("discordbaldur", desc="Mode for speaking and discord without any commands")
mod.mode("baldur", desc="Mode for playing baldur's gate")
in_discord_mode = True
baldur_keyboard_activated = False

@mod.action_class
class Actions:
    def enter_baldur_mode():
        """Presses discord mute hotkey and starts baldur mode"""
        global in_discord_mode
        if in_discord_mode:
            actions.key("f10")
            in_discord_mode = False

        global baldur_keyboard_activated
        if not baldur_keyboard_activated:
            actions.user.hud_set_virtual_keyboard('baldur_keyboard', visible=False)
            baldur_keyboard_activated = True

        actions.mode.enable("command")
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
        actions.mode.enable("command")
        actions.mode.disable("user.discordbaldur")
        actions.mode.disable("user.baldur")
        if in_discord_mode:
            actions.key("f10")
            in_discord_mode = False

        global baldur_keyboard_activated
        if baldur_keyboard_activated:
            actions.user.hud_set_virtual_keyboard('')
            baldur_keyboard_activated = False

def register_virtual_keyboard():
    """Creates a four region virtual keyboard with talon HUD to extend number of keys available and make movement easier"""
    screen_width = 1920
    half_width = screen_width/2
    screen_height = 1080
    half_height = screen_height/2
    center_box_size = 100

    keys =[
        actions.user.hud_create_virtual_key(actions.user.virtual_key_region_activated, x=0, y=0, width=half_width - center_box_size, height=half_height - center_box_size, action_args={"region": 0}),
        actions.user.hud_create_virtual_key(actions.user.virtual_key_region_activated, x=half_width - center_box_size, y=0, width=center_box_size, height=half_height - center_box_size, action_args={"region": 0}),
        actions.user.hud_create_virtual_key(actions.user.virtual_key_region_activated, x=0, y=half_height - center_box_size, width=half_width - center_box_size, height=center_box_size, action_args={"region": 0}),

        actions.user.hud_create_virtual_key(actions.user.virtual_key_region_activated, x=half_width, y=0, width=center_box_size, height=half_height - center_box_size, action_args={"region": 1}),
        actions.user.hud_create_virtual_key(actions.user.virtual_key_region_activated, x=half_width + center_box_size, y=0, width=half_width - center_box_size, height=half_height - center_box_size, action_args={"region": 1}),
        actions.user.hud_create_virtual_key(actions.user.virtual_key_region_activated, x=half_width + center_box_size, y=half_height - center_box_size, width=half_width - center_box_size, height=center_box_size, action_args={"region": 1}),

        actions.user.hud_create_virtual_key(actions.user.virtual_key_region_activated, x=0, y=half_height, width=half_width - center_box_size, height=center_box_size, action_args={"region": 3}),
        actions.user.hud_create_virtual_key(actions.user.virtual_key_region_activated, x=0, y=half_height + center_box_size, width=half_width - center_box_size, height=half_height - center_box_size, action_args={"region": 3}),
        actions.user.hud_create_virtual_key(actions.user.virtual_key_region_activated, x=half_width - center_box_size, y=half_height + center_box_size, width=center_box_size, height=half_height - center_box_size, action_args={"region": 3}),

        actions.user.hud_create_virtual_key(actions.user.virtual_key_region_activated, x=half_width, y=half_height + center_box_size, width=center_box_size, height=half_height - center_box_size, action_args={"region": 4}),
        actions.user.hud_create_virtual_key(actions.user.virtual_key_region_activated, x=half_width + center_box_size, y=half_height + center_box_size, width=half_width - center_box_size, height=half_height - center_box_size, action_args={"region": 4}),
        actions.user.hud_create_virtual_key(actions.user.virtual_key_region_activated, x=half_width + center_box_size, y=half_height, width=half_width - center_box_size, height=center_box_size, action_args={"region": 4}),
    ]
    print("Setting up keys")
    actions.user.hud_register_virtual_keyboard('baldur_keyboard', keys)
    

#app.register('ready', register_virtual_keyboard) 