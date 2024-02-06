
key(f20:down):
    user.enter_discord_mode()

key(f21:down):
    tracking.control_head_toggle(false)
    user.mouse_drag(0)

key(f21:up):
    tracking.control_head_toggle(true)
    user.mouse_drag_end()

key(f22:down):
    tracking.control_toggle(false)

key(f22:up):
    tracking.control_toggle(true)