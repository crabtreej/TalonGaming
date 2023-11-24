mode: user.warcraft
-
parrot(Cluck):
    print("Cluck")
    user.handle_parrot_action("Cluck")

parrot(Hiss):
    print("Hiss")
    user.handle_parrot_action("Hiss")

parrot(Hiss:repeat):
    print("Hiss")
    user.handle_parrot_action("Hiss")

parrot(Hiss:stop):
    print("Hiss:stop")
    user.handle_parrot_action("Hiss:stop")

parrot(Whistle):
    print("Whistle")
    user.handle_parrot_action("Whistle")

parrot(Ae):
    print("Ae")
    user.handle_parrot_action("Ae")

parrot(Ah):
    print("Ah")
    user.handle_parrot_action("Ah")

parrot(Iy):
    print("Iy")
    user.handle_parrot_action("Iy")

parrot(Oh):
    print("Oh")
    user.handle_parrot_action("Oh")

parrot(U):
    print("U")
    user.handle_parrot_action("U")

parrot(Suck):
    print("Suck")
    user.handle_parrot_action("Suck")

parrot(Sh):
    print("Sh")
    user.handle_parrot_action("Sh")

parrot(Sh:repeat):
    print("Sh")
    user.handle_parrot_action("Sh")

parrot(Sh:stop):
    print("Sh:stop")
    user.handle_parrot_action("Sh:stop")

parrot(Oah):
    print("Oah")
    tracking.control_toggle(false)
    mouse_click(1)
    tracking.control_toggle(true)
