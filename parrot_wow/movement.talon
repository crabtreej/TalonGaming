mode: user.warcraft
-
parrot(pop):
    print("Got vertical move command")
    user.move_in_direction("pop")

parrot(long_e):
    print("Got horizontal move command")
    user.move_in_direction("long_e")

parrot(long_e:stop):
    print("Got horizontal move stop command")
    user.move_in_direction("long_e")

parrot(clack):
    print("stopping all movement")
    user.stop_movement()