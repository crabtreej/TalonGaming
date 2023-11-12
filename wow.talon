mode: user.warcraftnew
-
parrot(clack):
    print("Testing")
    user.handle_parrot_action("Cluck")

parrot(hiss):
    print("Got horizontal move command")
    user.handle_parrot_action("Hiss")

parrot(hiss:repeat):
    print("Got horizontal move repeat command")
    user.handle_parrot_action("Hiss")

parrot(hiss:stop):
    #print("Got horizontal move stop command")
    user.handle_parrot_action("Hiss:stop")

parrot(quack):
    user.handle_parrot_action("quack")