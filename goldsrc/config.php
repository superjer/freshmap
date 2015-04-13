<?php

// FRESHMAP CONFIG

define(ROOMLIMIT,400);
define(XBOUND,80);
define(YBOUND,80);
define(ZBOUND,500);
define(XSCALE,16);
define(YSCALE,16);
define(ZSCALE,8);
define(LOW,6);
define(THIN,8);
define(COLLIDE_NORMAL,1);
define(COLLIDE_NOBOUND,2);
define(COLLIDE_LOWEST,3);
define(COLLIDE_HIGHEST,4);

$mons = array('monster_alien_grunt','monster_alien_slave','monster_headcrab','monster_bullchicken','monster_houndeye','monster_human_grunt','monster_human_assassin','monster_sentry','monster_zombie');
$mons_fr = array(               10 ,                  30 ,               20 ,                  15 ,               40 ,                  80 ,                     10 ,              5 ,             20 );
$mons_cl = array(                5 ,                  10 ,               15 ,                   1 ,               20 ,                  20 ,                      8 ,              5 ,             10 ); 
$mons_w = array(                16 ,                  14 ,               10 ,                  16 ,               10 ,                  14 ,                     12 ,              8 ,             12 );
$mons_h = array(                15 ,                  10 ,                5 ,                   8 ,                7 ,                  10 ,                     10 ,             10 ,             10 );
$weap = array('weapon_357','weapon_9mmAR','weapon_9mmhandgun','weapon_crossbow','weapon_egon','weapon_gauss','weapon_hornetgun','weapon_rpg','weapon_shotgun');
$weap_fr = array(       5 ,            3 ,                10 ,               3 ,           1 ,            2 ,                1 ,          1 ,              4 );
$ammo = array('ammo_357','ammo_9mmclip','ammo_9mmAR','ammo_crossbow','ammo_gaussclip','ammo_rpgclip','ammo_buckshot','weapon_handgrenade','weapon_satchel','weapon_tripmine','item_healthkit','item_battery');
$ammo_fr = array(    20 ,           20 ,          4 ,             4 ,              5 ,            2 ,             8 ,                  7 ,              3 ,               4 ,              2 ,            1 );

$seed = 'random';
