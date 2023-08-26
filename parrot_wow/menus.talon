mode: user.warcraftmenus
-
open talents:
    key(n)
open quest log:
    key(l)
open spellbook:
    key(p)
open backpack:
    key(shift-b)
open map:
    key(m)
open character:
    key(c)
open achievements:
    key(y)
open social:
    key(o)
open group finder:
    key(i)
open main:
    key(escape)

parrot(clack):
    print("Leaving menus mode for warcraft mode")
    user.enter_warcraft_mode()

parrot(whistle):
    print("Leaving menus mode for command mode")
    user.return_to_command_mode()