mode: user.warcraft
-
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

parrot(whistle):
    print("Leaving warcraft mode for menus mode")
    user.enter_menus_mode()