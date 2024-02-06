from talon import actions, Module, app, scope, noise, ctrl
from talon.lib import cubeb

ctx = cubeb.Context()
mod = Module()


@mod.action_class
class Actions:
    def return_to_command_mode():
        """Disables any warcraft mode configurations and returns to command mode"""
        actions.user.hud_set_virtual_keyboard(None)
        actions.user.hud_disable_id('Text panel')
        actions.mode.disable("user.warcraft")
        actions.mode.enable("command")


def discord_callback():
    actions.user.register_enter_exit_callbacks("command", lambda: actions.mode.disable("command"), lambda: actions.mode.enable("command"))


app.register("ready", lambda: discord_callback())