mode: user.warcraft
-
settings():
    user.mouse_enable_pop_click = 0

<phrase>: skip()
key(f20:down):
    print("Leaving warcraft mode for discord mode")
    user.enter_discord_mode()

key(f21:down):
    tracking.control_head_toggle(false)
    user.mouse_drag(2)

key(f21:up):
    tracking.control_head_toggle(true)
    user.mouse_drag_end()

key(f22:down):
    tracking.control_head_toggle(false)

key(f22:up):
    tracking.control_head_toggle(true)