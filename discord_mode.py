from typing import Callable
from talon import actions, Module, app, scope
from talon.lib import cubeb

ctx = cubeb.Context()
mod = Module()
mod.mode("discord", desc="Mode for speaking in discord without any commands")


def restore_microphone(name):
    devices = [
        dev.name for dev in ctx.inputs() if dev.state == cubeb.DeviceState.ENABLED
    ]
    microphone = next((x for x in devices if name in x))
    actions.sound.set_microphone(microphone)


global callbacks
callbacks = {}


@mod.action_class
class Actions:
    def enter_discord_mode():
        """Toggles discord mute calls any registered enter callbacks"""
        active_modes = scope.get("mode")
        if "sleep" in active_modes or "user.discord" in active_modes:
            print("already in discord or sleep mode, not entering again")
            return

        global callbacks
        for mode in active_modes:
            if mode in callbacks:
                callbacks[mode]["enter"]()
                callbacks[mode]["exited"] = True

        actions.mode.enable("user.discord")
        actions.key("f10")
        actions.sound.set_microphone("None")
    

    def exit_discord_mode():
        """Leaves discord mode and calls any registered exit callbacks"""
        active_modes = scope.get("mode")

        global callbacks
        for mode in callbacks:
            if callbacks[mode]["exited"]:
                callbacks[mode]["exit"]()
                callbacks[mode]["exited"] = False

        actions.key("f10")
        try:
            restore_microphone('Shure')
        except:
            restore_microphone('Hyper')
        actions.mode.disable("user.discord")


    def register_enter_exit_callbacks(mode: str, enter_cb: Callable, exit_cb: Callable):
        """Allows other modes to register enter and exit calls for discord mode"""
        callbacks[mode] = {
            'enter': enter_cb,
            'exit': exit_cb,
            'exited': False,
        }

        