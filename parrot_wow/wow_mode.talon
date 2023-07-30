mode: user.warcraft
-
<phrase>: skip()
parrot(whistle):
    print("Leaving warcraft mode for discord mode")
    user.enter_discord_mode()

parrot(quack):
    print("Leaving warcraft mode for command mode")
    user.return_to_command_mode()