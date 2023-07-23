mode: user.warcraft_mode
-
^command mode$:
    mode.disable("user.warcraft_mode")
    mode.enable("command")