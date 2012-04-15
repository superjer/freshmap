<?php


# do_compile
# Set to TRUE to do the compile and possible load the map on the game server
$do_compile = false;

# wadroot
# This is the location of the .wad files needed by the compilers
$wadroot = '/home/gameserver/freshmap';

# gamemapsdir
# This is the location where the maps need to be placed to load in the game
$gamemapsdir = '/home/gameserver/hlds_l/valve/maps';

# storemapsdir
# Location to also store maps (like on a webserver, for example)
# Leave blank to skip this step
$storemapsdir = '/var/www/valve/maps';

# serverscreen
# The name of the screen in which the game server is running
# Leave blank to skip doing a changelevel in the server after compile
$serverscreen = 'hlserver';

# shell_execs
# Commands to run after the compile in the default shell, in the zhlt directory
$shell_cmds = array();
$shell_cmds[] = "rm -f $fresh_*";


?>
