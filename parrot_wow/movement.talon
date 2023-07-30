mode: user.warcraft
-
parrot(clack):
    print("Got vertical move command")
    user.movement_command("clack")

parrot(hiss):
    print("Got horizontal move command")
    user.movement_command("hiss")

parrot(hiss:stop):
    print("Got horizontal move stop command")
    user.movement_command("hiss:stop")

parrot(long_e):
    print("Stationary turn command")
    user.movement_command("long_e")

parrot(long_e:stop):
    print("Stationary turn stop command")
    user.movement_command("long_e:stop")

careful:
    print("Enabling safe walk mode")
    user.set_safe_walk(true)

danger:
    print("Disabling safe walk mode")
    user.set_safe_walk(false)

jump:
    print("Jumping")
    user.movement_command("space")