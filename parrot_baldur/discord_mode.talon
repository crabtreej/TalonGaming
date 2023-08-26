mode: user.discordbaldur
-
<phrase>: skip()
key(f20:down):
    print("Leaving discord mode for baldur mode")
    user.enter_baldur_mode()

key(f21:down):
    tracking.control_head_toggle(false)
    user.mouse_drag(2)

key(f21:up):
    tracking.control_head_toggle(true)
    user.mouse_drag_end()