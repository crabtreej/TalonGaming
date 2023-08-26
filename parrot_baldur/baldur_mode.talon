mode: user.baldur
-
key(f20:down):
    print("Entering baldur's gate discord mode")
    user.enter_discord_mode_baldur()

key(f21:down):
    tracking.control_head_toggle(false)
    user.mouse_drag(2)

key(f21:up):
    tracking.control_head_toggle(true)
    user.mouse_drag_end()
    
parrot(whistle):
    print("Returning to command mode from baldur's gate mode")
    user.return_to_command_mode_baldur()
