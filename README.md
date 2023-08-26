This is mostly a personal projects so this read me as really barebones, but if people find value in what I've made I can flesh out what I've done more.

The basic gist of it is that in world_of_warcraft_mode.py when I register the keyboard I can pass an a dictionary of arguments that should be given to the handler, in particular which region. Then in movement.py whenever movement_command is called from movement.talon I also pass in the command name. This + the handler get passed through a second callback args dictionary which is merged with the first one (so you don't want the key names to intersect). virtual_key_region_activated  gets called with the movement handler as the target handler, and that in turn gets us to action_called_for_region. 

The upshot of this is that it means that I don't have to define a bunch of keyboards to have different actions in the same region because I can filter on the region and the command to check what should actually be done. Otherwise, as far as I know if I wanted to be able to look at region one to cast with one command and also wanted to be able to move it by looking at region one with another command I would either have to have multiple keyboards or I would have to have a command to change modes between moving and casting. This lets me do it all seamlessly by filtering on what command was sent for what region, so I can move and then immediately cast something without having to have an extra command where I switch modes in between. Obviously, sometimes it can result in like it picking up a movement when you meant to cast because there isn't that separation of a mode but I think it still makes it way more playable

This does require some hackiness, I have to sync the names of the commands from the talon file into the python file for the filters, but I've also gotten a lot of really nice functionality out of it and have been able to play realtime games like world of warcraft. Not retail, but something slower like classic. I think a better microphone and better parrot sounds mapped to my casts (using numbers really doesn't cut it, but I had issues getting it to pick up sounds like ee,ah,oh) it's probably playable at a higher level