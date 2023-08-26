mode: user.warcraft
-
<phrase>: skip()
key(f20:down):
    print("Leaving warcraft mode for discord mode")
    user.enter_discord_mode()

parrot(whistle):
    print("Leaving warcraft mode for menus mode")
    user.enter_menus_mode()