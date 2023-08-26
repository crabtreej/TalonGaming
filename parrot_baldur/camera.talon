mode: user.baldur
-
parrot(hiss):
    user.move_camera_command("hiss")

parrot(hiss:repeat):
    user.move_camera_command("hiss:repeat")
    
parrot(hiss:stop):
    user.stop_camera()