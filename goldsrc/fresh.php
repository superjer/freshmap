<?php

error_reporting(E_ALL ^ E_NOTICE);

include 'config.php';
include 'local.php';

$f = null;
$rooms = array();
$buildable = array();
$itemable = array();
$lights = array();
$blocks = array();
$items = array();

$algo = 0; //algorithm version

//pick a seed and set the mapname
if( $seed=='random' )
  $seed = time();
mt_srand($seed);
$freshname = "fresh_{$algo}_".dechex($seed);

//make initial room
new_room(-30,-30,0,30,30,mt_rand(15,30));
$buildable[] = 0;

//generate rooms
$nextparent = 0;
$nextcount = 0;
$i = 0;
while($i<8000) {
  $force = false;
  $stairs = 0;
  $tmp = array();
  if( $nextcount>0 ) {
    $n = $nextparent;
    $nextcount--;
  } else
    $n = $buildable[mt_rand(0,count($buildable)-1)];
  $r = $rooms[$n];
  if($r[children]>=2 && $r[children]>mt_rand(0,6) )
    continue;
  $i++;
  $parent = $n;
  switch(mt_rand(0,3)) { //pick one of the four walls
    case 0: $x0 = $r[x0]; $x1 = $r[x0]; $y0 = $r[y0]; $y1 = $r[y1]; break;
    case 1: $x0 = $r[x1]; $x1 = $r[x1]; $y0 = $r[y0]; $y1 = $r[y1]; break;
    case 2: $x0 = $r[x0]; $x1 = $r[x1]; $y0 = $r[y0]; $y1 = $r[y0]; break;
    case 3: $x0 = $r[x0]; $x1 = $r[x1]; $y0 = $r[y1]; $y1 = $r[y1]; break;
  }
  $z0 = $r[z0];
  $z1 = $r[z1];
  if( $z1-$z0<10 ) //not tall enough to stand
    $z1 = mt_rand($z0+10,$z0+30);
  if( mt_rand(0,5)==0 ) $z0 += mt_rand(0,14)-7;
  if( mt_rand(0,5)==0 ) $z1 += mt_rand(0,40)-20;
  if( mt_rand(0,9)==0 ) $z1 = $z0+20;
  if( $z1-$z0<LOW ) $z1=$z0+LOW+mt_rand(0,10);
  if( min($z1,$r[z1]) - max($z0,$r[z0])<LOW ) //not tall enough to pass thru
    $z1 += LOW;
  if( $x0 != $x1 ) { //east-west wall
    $mode = 'E/W';
    $a0 =& $x0;
    $a1 =& $x1;
    $b0 =& $y0;
    $b1 =& $y1;
    $abound = XBOUND;
    $bbound = YBOUND;
  } else {
    $mode = 'N/S';
    $a0 =& $y0;
    $a1 =& $y1;
    $b0 =& $x0;
    $b1 =& $x1;
    $abound = YBOUND;
    $bbound = XBOUND;
  }

  if( mt_rand(0,10)<6 ) { //doorway!
    $min = min($a0,$a1)+THIN;
    $max = max($a0,$a1)-THIN;
    if( $min<=$max ) {
      $a0 = mt_rand($min,$max);
      $a1 = $a0 + mt_rand(THIN,THIN*2)*(mt_rand(0,1)?1:-1);
    }
    if( $a1<$a0 ) { $tmp=$a1; $a1=$a0; $a0=$tmp; }
    $extrmax = min(100,($a1-$a0)*5);
    $extr = mt_rand(0,10) ? mt_rand(2,$extrmax) : mt_rand(2,20);
    $extr *= (mt_rand(0,1)?1:-1);
    $b1 += $extr;
    if( $b1<$b0 ) { $tmp=$b1; $b1=$b0; $b0=$tmp; }
    if( $extr>-7 && $extr<7 ) { //staircase?!
      if( $z0>$r[z0] ) $z0 = $r[z0];
      $step = 2;
      while(1) {
        $res=new_room($x0,$y0,$z0,$x1,$y1,$z1,$parent);
        if( !$res ) { $z1 = $z0+16; $res=new_room($x0,$y0,$z0,$x1,$y1,$z1,$parent); }
        if( !$res ) break;
        $parent = $res;
        $stairs++;
        if( $stairs>=20 || max(abs($b0),abs($b1))>$bbound-30 || mt_rand(0,12)==0 ) break;
        $b0 += $extr;
        $b1 += $extr;
        $z0 -= $step;
        if( $z1-$z0>30 ) $z1=$z0+20;
      }
      if(!$res) { //undo the stairs
        if($stairs) echo "Undoing $stairs stairs ($mode)\n";
        while($stairs--) array_pop($rooms);
        continue;
      }
      echo "Built $stairs stairs ($mode)\n";
      $b0 += $extr;
      $b1 += $extr;
      if( $extr>0 ) $b1 += 4;
      else          $b0 -= 4;
      $z0 -= $step;
      $force = true;
    }
  } else { //roomextension
    switch(mt_rand(0,2)) {
      case 0: $a0 = $a1 - mt_rand(5,100); break;
      case 1: $a1 = $a0 + mt_rand(5,100); break;
      case 2: $a0 -= mt_rand(1,100); $a1 += mt_rand(1,100); break;
    }
    $extrmax = min(80,($a1-$a0)*5);
    $extr = mt_rand(5,$extrmax)*(mt_rand(0,1)?1:-1);
    $b1 += $extr;
  }

  $res = new_room($x0,$y0,$z0,$x1,$y1,$z1,$parent,$force);
  if( !$res )
    $res = new_room($x0,$y0,$z0,$x1,$y1,$z0+12,$parent);
  if( $res && $force ) {
    $nextparent = $res;
    $nextcount = 4;
  }

   if( $nextcount==0 && count($rooms)>ROOMLIMIT )
    break;

  if(mt_rand(0,100)==0) { //re-index
    $winz = 4096;
    foreach($buildable as $n) { if($rooms[$n][z0]<$winz) $winz=$rooms[$n][z0]; }
    if($winz<-ZBOUND+20)
      break;
    $winz += 4;
    $newbuildable = array();
    foreach($buildable as $n) {
      if( $rooms[$n][z0]<=$winz )
        $newbuildable[] = $n;
    }
    $buildable = $newbuildable;
  }
}

//find sky level and base level
$skylevel = -4096;
$toplevel = -4096;
$baselevel = 4096;
foreach($rooms as $n => $r) {
  if( $r[z1]>$skylevel  ) $skylevel  = $r[z1];
  if( $r[z0]>$toplevel  ) $toplevel  = $r[z0];
  if( $r[z0]<$baselevel ) $baselevel = $r[z0];
}
$level1 = intval((($toplevel-$baselevel)/3)*1 + $baselevel);
$level2 = intval((($toplevel-$baselevel)/3)*2 + $baselevel);
$rooms[0][z1] = $skylevel;

//grow some rooms
$grown = 0;
for($i=count($itemable);$grown<8 && $i>=0;$i--) {
  $n = $itemable[$i];
  $r = $rooms[$n];
  if( $r[x1]-$r[x0]>=15 && $r[y1]-$r[y0]>=15 ) {
    grow($n);
    $grown++;
  }
}


//add lights
for($i=0;$i<count($itemable);$i++) {
  $n = $itemable[mt_rand(0,count($itemable)-1)];
  $r = $rooms[$n];
  if($r[z1]==$skylevel)
    continue;
  $x0 = intval(($r[x0]+2)/4)*4;
  $x1 = intval(($r[x1]-2)/4)*4;
  $y0 = intval(($r[y0]+2)/4)*4;
  $y1 = intval(($r[y1]-2)/4)*4;
  if( $x0<$x1 && $y0<$y1 && $r[z1]-$r[z0]>6 ) {
    $x = mt_rand($x0/4,$x1/4)*4;
    $y = mt_rand($y0/4,$y1/4)*4;
    $lights[] = point($x,$y,$r[z1]);
  }
}


//add items
$entcount = 0;
$itemmax = count($itemable);
echo "itemmax = $itemmax\n";
for($i=0;$i<$itemmax;$i++) {
  $n = $itemable[mt_rand(0,count($itemable)-1)];
  $r = $rooms[$n];
  if( $r[children]==0 && mt_rand(0,1)==0 ) { //guns or ammo
    if( mt_rand(0,2)==0 ) { //guns
      $choice = weighted_rand($weap_fr);
      new_item($n,$weap[$choice],4,4);
    } else { //ammo
      $choice = weighted_rand($ammo_fr);
      new_item($n,$ammo[$choice],4,4);
      new_item($n,$ammo[$choice],4,4);
    }
  } else if($n>=12) { //monster (not in 1st 12 rooms)
    $attempts++;
    $choice = weighted_rand($mons_fr);
    for($j=0;$j<$mons_cl[$choice];$j++) {
      new_item($n,$mons[$choice],$mons_w[$choice],$mons_h[$choice]);
      if( mt_rand(0,3)==0 ) break;
    }
  }
  if( ++$entcount>400 ) break;
}
echo "Items:\n failed b/c height: $heightfail\n failed b/c width: $widthfail\n failed b/c collision: $collidefail\n succeeded: $itemsuccess\n";
echo "Attempted to make $attempts monsters\n";


//build outside of sweetawesome tower
new_room(-XBOUND-40,-YBOUND-40,$baselevel,-XBOUND   , YBOUND+40,$skylevel,false,true);
new_room( XBOUND   ,-YBOUND-40,$baselevel, XBOUND+40, YBOUND+40,$skylevel,false,true);
new_room(-XBOUND   ,-YBOUND-40,$baselevel, XBOUND   ,-YBOUND   ,$skylevel,false,true);
new_room(-XBOUND   , YBOUND   ,$baselevel, XBOUND   , YBOUND+40,$skylevel,false,true);


$f = fopen("./zhlt/$freshname.map",'w');
writehead();

echo "Padding ".count($rooms)." rooms...\n";
//pad rooms with wall blocks
foreach($rooms as $n=>$r) {
  if( $r[z1]==$skylevel )     $ceiltex ='SKY';
  else                        $ceiltex ='PIPE_CEILING';
  if( $r[z0]==$baselevel )  { $floortex='OUT_SND2C';    $walltex='TNNL_W5A';      }
  else if( $r[z0]<$level1 ) { $floortex='TNNL_FLR6B';   $walltex='CRETE2_WALL03'; }
  else if( $r[z0]<$level2 ) { $floortex='CRETE2_FLR02'; $walltex='BRICKERS';      }
  else                      { $floortex='CRETE2_FLR01'; $walltex='BRICKERS';      }
  if( $r[y0]<=-YBOUND-39 ) $swalltex='SKY';
  else                    $swalltex=$walltex;
  if( $r[y1]>= YBOUND+39 ) $nwalltex='SKY';
  else                    $nwalltex=$walltex;
  if( $r[x0]<=-XBOUND-39 ) $wwalltex='SKY';
  else                    $wwalltex=$walltex;
  if( $r[x1]>= XBOUND+39 ) $ewalltex='SKY';
  else                    $ewalltex=$walltex;

  sliceandwrite($r[x0]  ,$r[y0]  ,$r[z0]-2,$r[x1]  ,$r[y1]  ,$r[z0]  ,$floortex, 0 ); //floor
  sliceandwrite($r[x0]  ,$r[y0]  ,$r[z1]  ,$r[x1]  ,$r[y1]  ,$r[z1]+2,$ceiltex,  0 ); //ceiling
  sliceandwrite($r[x0]  ,$r[y0]-2,$r[z0]  ,$r[x1]  ,$r[y0]  ,$r[z1]  ,$swalltex, 0 ); //southwall
  sliceandwrite($r[x0]  ,$r[y1]  ,$r[z0]  ,$r[x1]  ,$r[y1]+2,$r[z1]  ,$nwalltex, 0 ); //northwall
  sliceandwrite($r[x0]-2,$r[y0]  ,$r[z0]  ,$r[x0]  ,$r[y1]  ,$r[z1]  ,$wwalltex, 0 ); //westwall
  sliceandwrite($r[x1]  ,$r[y0]  ,$r[z0]  ,$r[x1]+2,$r[y1]  ,$r[z1]  ,$ewalltex, 0 ); //eastwall
  echo "$n ";
}
echo " done.\n";

foreach($lights as $l) {
  $b = block( ($l[x]-2)*XSCALE, ($l[y]-2)*YSCALE, $l[z]*ZSCALE-2, ($l[x]+2)*XSCALE, ($l[y]+2)*YSCALE, $l[z]*ZSCALE );
  $t = defaultprops('GENERIC027');
  $t[btex] = 'LITEPANEL1';
  $t[bxs] = '1';
  $t[bys] = '1';
  $t[bxo] = '32';
  $t[byo] = '32';
  writeblockspecific($b,$t);
}

writefoot();

echo "$invalidblocks invalid blocks ignored.\n";

//point entities
writeent(0,0,10,'info_player_start','"angles" "0 0 0"');
writeent(-10,-10,10,'info_player_deathmatch','"angles" "0 45 0"');
writeent( 10,-10,10,'info_player_deathmatch','"angles" "0 135 0"');
writeent( 10, 10,10,'info_player_deathmatch','"angles" "0 225 0"');
writeent(-10, 10,10,'info_player_deathmatch','"angles" "0 315 0"');
writeent(0,0,12,'light_environment','"angles" "0 15 0"'."\r\n".'"_light" "255 255 255 80"'."\r\n".'"pitch" "-77"');

//items n monsters
$entcount = 0;
foreach($items as $it) {
  $addtl = '"angles" "0 '.mt_rand(0,359).' 0"';
  switch($it[name]) {
    case 'monster_sentry':
      $addtl .= "\r\n".'"spawnflags" "32"';
      break;
    case 'monster_human_grunt':
      $val = mt_rand(0,2) ? (1+2*(mt_rand(0,3)%3)) : (8+2*(mt_rand(0,2)%2));
      $addtl .= "\r\n".'"weapons" "'.$val.'"';
      break;
  }
  writeent($it[x],$it[y],$it[z]+1,$it[name],$addtl);
  if( ++$entcount>400 ) break;
}

//the barnacle
$winz = 4096;
foreach($rooms as $n => $r)
  if($r[z0]<=$winz && $r[z1]-$r[z0]>10 && $r[x1]-$r[x0]>6 && $r[y1]-$r[y2]>6) {
    $winz = $r[z0];
    $win = $n;
  }
$r = $rooms[$win];
$x = intval(($r[x0]+$r[x1])/2);
$y = intval(($r[y0]+$r[y1])/2);
writeent($x,$y,$r[z1],'monster_barnacle','"angles" "0 0 0"');

fclose($f);

/*
$img = imagecreatetruecolor(1024,1024);
foreach($rooms as $r)
  imagefilledrectangle($img,$r[x0]+512,$r[y0]+512,$r[x1]+512,$r[y1]+512,255);
foreach($rooms as $r) {
  imagerectangle($img,$r[x0]+512,$r[y0]+512,$r[x1]+512,$r[y1]+512,16777215);
}
imagegif($img,"./out.gif");
imagedestroy($img);
*/


//compile!
if( $do_compile )
{
  if( !chdir('zhlt') )
    die("Failed to enter zhlt directory!\n");
  if( !putenv("WADROOT=$wadroot") )
    die("Failed to set WADROOT in the environment!\n");
  passthru( "./hlcsg -nowadtextures $freshname", $return );
  if( $return!=0 )
    die("hlcsg failed!\n");
  passthru( "./hlbsp $freshname", $return );
  if( $return!=0 )
    die("hlbsp failed!\n");
  passthru( "./hlvis -full $freshname", $return );
  if( $return!=0 )
    die("hlvis failed!\n");
  passthru( "./hlrad -bounce 2 -chop 128 $freshname", $return );
  if( $return!=0 )
    die("hlrad failed!\n");
  if( $gamemapsdir )
    if( !copy( "$freshname.bsp", "$gamemapsdir/$freshname.bsp" ) )
      die("Failed to move bsp to maps directory!\n");
  if( $storemapsdir )
    if( !copy( "$freshname.bsp", "$storemapsdir/$freshname.bsp" ) )
      echo "Failed to move bsp to sv_downloadurl directory!\n";
  foreach($shell_cmds as $cmd)
    shell_exec( $cmd );
  if( $serverscreen )
  {
    passthru( "screen -r $serverscreen -X stuff \"changelevel $freshname\n\"", $return );
    if( $return!=0 )
      die("Failed to changelevel on hlserver!\n");
  }
}


exit;
////////////////////// DONE /////////////////////////






function new_room($_x0,$_y0,$_z0,$_x1,$_y1,$_z1,$parent=false,$force=false) {
  global $rooms;
  global $buildable;
  global $itemable;
  $big = true;
  $room = array();
  $room[x0] = min($_x0,$_x1);
  $room[x1] = max($_x0,$_x1);
  $room[y0] = min($_y0,$_y1);
  $room[y1] = max($_y0,$_y1);
  $room[z0] = min($_z0,$_z1);
  $room[z1] = max($_z0,$_z1);
  $room[children] = 0;
  if( ($room[x1]-$room[x0]) * ($room[y1]-$room[y0]) < 25 ) //not enough floorspace
    $big = false;
  if( ($room[x1]-$room[x0]<5 || $room[y1]-$room[y0]<5) ) //too thin
    $big = false;
  if( $force || collide($room)===false ) {
    $rooms[] = $room;
    $n = count($rooms)-1;
    if($big) {
      $buildable[] = $n;
      $itemable[] = $n;
    }
    if($parent!==false)
      $rooms[$parent][children]++;
    return true;
  }
  return false;
}

function collide($_room,$mode=COLLIDE_NORMAL,$offset=0) {
  global $rooms;
  if( $mode!=COLLIDE_NOBOUND ) {
    if( $_room[x0]<-XBOUND || $_room[x1]>XBOUND ||
        $_room[y0]<-YBOUND || $_room[y1]>YBOUND ||
        $_room[z0]<-ZBOUND || $_room[z1]>ZBOUND )
      return -1; //collides with edge of map
  }
  $winz = $mode==COLLIDE_LOWEST ? 4096 : -4096;
  $win = false;
  $count = count($rooms);
  for($n=$offset;$n<$count;$n++) { //find intersection space
    $r = $rooms[$n];
    $lox = max($r[x0],$_room[x0]);
    $loy = max($r[y0],$_room[y0]);
    $loz = max($r[z0],$_room[z0]);
    $hix = min($r[x1],$_room[x1]);
    $hiy = min($r[y1],$_room[y1]);
    $hiz = min($r[z1],$_room[z1]);
    if($lox<$hix && $loy<$hiy && $loz<$hiz) {
      switch($mode) {
        case COLLIDE_NORMAL:
        case COLLIDE_NOBOUND:
          return $n;
        case COLLIDE_LOWEST:
          if( $r[z0] < $winz ) { $winz=$r[z0]; $win=$n; }
          break;
        case COLLIDE_HIGHEST:
          if( $r[z0] > $winz ) { $winz=$r[z0]; $win=$n; }
          break;
        default:
          die('Invalid collision mode!');
      }
    }
  }
  return $win;
}

function sliceandwrite($x0,$y0,$z0,$x1,$y1,$z1,$tex,$offs) {
  global $rooms;
  $b = block($x0,$y0,$z0,$x1,$y1,$z1);
  $coll = collide($b,COLLIDE_NOBOUND,$offs);
  $offs = $coll+1;
  if( $coll===-1 || $coll===false ) {
    $scaledb = block($x0*XSCALE,$y0*YSCALE,$z0*ZSCALE,$x1*XSCALE,$y1*YSCALE,$z1*ZSCALE);
    writeblock($scaledb,$tex);
  } else { //slice and recurse
    $c = $rooms[$coll];
    if($z1>$c[z1]) { sliceandwrite($x0   ,$y0   ,$c[z1],$x1   ,$y1   ,$z1   ,$tex, $offs); $z1=$c[z1]; }
    if($z0<$c[z0]) { sliceandwrite($x0   ,$y0   ,$z0   ,$x1   ,$y1   ,$c[z0],$tex, $offs); $z0=$c[z0]; }
    if($y1>$c[y1]) { sliceandwrite($x0   ,$c[y1],$z0   ,$x1   ,$y1   ,$z1   ,$tex, $offs); $y1=$c[y1]; }
    if($y0<$c[y0]) { sliceandwrite($x0   ,$y0   ,$z0   ,$x1   ,$c[y0],$z1   ,$tex, $offs); $y0=$c[y0]; }
    if($x1>$c[x1]) { sliceandwrite($c[x1],$y0   ,$z0   ,$x1   ,$y1   ,$z1   ,$tex, $offs); }
    if($x0<$c[x0]) { sliceandwrite($x0   ,$y0   ,$z0   ,$c[x0],$y1   ,$z1   ,$tex, $offs); }
  }
}

function grow($n) {
  global $rooms;
  global $skylevel;
  $baseroom = $rooms[$n];
  $b = block($baseroom[x0],$baseroom[y0],$baseroom[z1],$baseroom[x1],$baseroom[y1],$skylevel);

  if($b[x1]<=$b[x0] || $b[y1]<=$b[y0] || $b[z1]<=$b[z0]) {
    echo "WHOOPS! ";
    return;
  }
  echo "OK ";

  $m = collide($b,COLLIDE_LOWEST);
  if( $m===false || $m===-1 ) {
    $rooms[] = $b;
    return;
  }
  $c = $rooms[$m];
  $c[x0]--;
  $c[x1]++;
  $c[y0]--;
  $c[y1]++;

  //build underhang space
  $x0 = max($b[x0],$c[x0]);
  $x1 = min($b[x1],$c[x1]);
  $y0 = max($b[y0],$c[y0]);
  $y1 = min($b[y1],$c[y1]);
  $z0 = $b[z0];
  $z1 = $c[z0]-4;
  if( $z0<$z1 ) $rooms[] = block($x0,$y0,$z0,$x1,$y1,$z1);

  //grow remaining space upward
  $b[z1] = $c[z0];
  if($b[y1]>$c[y1]) {        /////
    $rooms[] = block($b[x0],$c[y1],$b[z0],$b[x1],$b[y1],$b[z1]);
    grow(count($rooms)-1);
    $b[y1] = $c[y1];
  }
  if($b[y0]<$c[y0]) {                             /////
    $rooms[] = block($b[x0],$b[y0],$b[z0],$b[x1],$c[y0],$b[z1]);
    grow(count($rooms)-1);
    $b[y0] = $c[y0];
  }
  if($b[x1]>$c[x1]) { /////
    $rooms[] = block($c[x1],$b[y0],$b[z0],$b[x1],$b[y1],$b[z1]);
    grow(count($rooms)-1);
  }
  if($b[x0]<$c[x0]) {                      /////
    $rooms[] = block($b[x0],$b[y0],$b[z0],$c[x0],$b[y1],$b[z1]);
    grow(count($rooms)-1);
  }
}

function new_item($n,$name,$w,$h) {
  global $rooms;
  global $items;
  global $heightfail;
  global $widthfail;
  global $collidefail;
  global $itemsuccess;
  $r = $rooms[$n];
  if( $r[z1]-$r[z0] < $h )
    {$heightfail++; return;}
  $x0 = intval($r[x0]+$w/2);
  $x1 = intval($r[x1]-$w/2);
  $y0 = intval($r[y0]+$w/2);
  $y1 = intval($r[y1]-$w/2);
  if( $x0>$x1 || $y0>$y1 )
    {$widthfail++; return;}
  $x = mt_rand($x0,$x1);
  $y = mt_rand($y0,$y1);
  $z = $r[z0];
  foreach($items as $i) {
    $testh = ($i[z]<$z) ? $i[h] : $h;
    if( abs($i[x]-$x)<(($i[w]+$w)/2) && abs($i[y]-$y)<(($i[w]+$w)/2) && abs($i[z]-$z)<$testh ) {
      $collidefail++;
      return;
    }
  }
  $item = array(x=>$x,y=>$y,z=>$r[z0],w=>$w,h=>$h,name=>$name);
  $items[] = $item;
  $itemsuccess++;
}

function weighted_rand($arr) {
  $sum = array_sum($arr);
  $n = mt_rand(1,$sum);
  $sum = 0;
  foreach($arr as $k=>$v) {
    $sum += $v;
    if( $n<=$sum ) return $k;
  }
}

function point($x,$y,$z) {
  return array(x=>$x,y=>$y,z=>$z);
}

function block($x0,$y0,$z0,$x1,$y1,$z1) {
  return array(x0=>$x0,y0=>$y0,z0=>$z0,x1=>$x1,y1=>$y1,z1=>$z1);
}

function writeblock($b,$tex) {
  $t = defaultprops($tex);
  writeblockspecific($b,$t);
}

function defaultprops($tex) {
  return array(tu1=> 1,tu2=> 0,tu3=> 0,txo=> 0,tv1=> 0,tv2=>-1,tv3=> 0,tyo=> 0,trot=> 0,txs=> 1,tys=> 1,ttex=>$tex,
               bu1=> 1,bu2=> 0,bu3=> 0,bxo=> 0,bv1=> 0,bv2=>-1,bv3=> 0,byo=> 0,brot=> 0,bxs=> 1,bys=> 1,btex=>$tex,
               wu1=> 0,wu2=> 1,wu3=> 0,wxo=> 0,wv1=> 0,wv2=> 0,wv3=>-1,wyo=> 0,wrot=> 0,wxs=> 1,wys=> 1,wtex=>$tex,
               eu1=> 0,eu2=> 1,eu3=> 0,exo=> 0,ev1=> 0,ev2=> 0,ev3=>-1,eyo=> 0,erot=> 0,exs=> 1,eys=> 1,etex=>$tex,
               nu1=> 1,nu2=> 0,nu3=> 0,nxo=> 0,nv1=> 0,nv2=> 0,nv3=>-1,nyo=> 0,nrot=> 0,nxs=> 1,nys=> 1,ntex=>$tex,
               su1=> 1,su2=> 0,su3=> 0,sxo=> 0,sv1=> 0,sv2=> 0,sv3=>-1,syo=> 0,srot=> 0,sxs=> 1,sys=> 1,stex=>$tex);
}

function writeblockspecific($b,$t) {
  global $f;
  global $invalidblocks;
  extract($b);
  extract($t);
  if( $z1-$z0<=0 ) { $invalidblocks++; return; }
  if( $y1-$y0<=0 ) { $invalidblocks++; return; }
  if( $x1-$x0<=0 ) { $invalidblocks++; return; }
  fwrite($f,<<<EOT
{
( $x0 $y1 $z1 ) ( $x1 $y1 $z1 ) ( $x1 $y0 $z1 ) $ttex [ $tu1 $tu2 $tu3 $txo ] [ $tv1 $tv2 $tv3 $tyo ] $trot $txs $tys
( $x0 $y0 $z0 ) ( $x1 $y0 $z0 ) ( $x1 $y1 $z0 ) $btex [ $bu1 $bu2 $bu3 $bxo ] [ $bv1 $bv2 $bv3 $byo ] $brot $bxs $bys
( $x0 $y1 $z1 ) ( $x0 $y0 $z1 ) ( $x0 $y0 $z0 ) $wtex [ $wu1 $wu2 $wu3 $wxo ] [ $wv1 $wv2 $wv3 $wyo ] $wrot $wxs $wys
( $x1 $y1 $z0 ) ( $x1 $y0 $z0 ) ( $x1 $y0 $z1 ) $etex [ $eu1 $eu2 $eu3 $exo ] [ $ev1 $ev2 $ev3 $eyo ] $erot $exs $eys
( $x1 $y1 $z1 ) ( $x0 $y1 $z1 ) ( $x0 $y1 $z0 ) $ntex [ $nu1 $nu2 $nu3 $nxo ] [ $nv1 $nv2 $nv3 $nyo ] $nrot $nxs $nys
( $x1 $y0 $z0 ) ( $x0 $y0 $z0 ) ( $x0 $y0 $z1 ) $stex [ $su1 $su2 $su3 $sxo ] [ $sv1 $sv2 $sv3 $syo ] $srot $sxs $sys
}

EOT
  );
}

function writehead() {
  global $f;
  fwrite($f,<<<EOT
{
"classname" "worldspawn"
"MaxRange" "8192"
"mapversion" "220"
"message" "Generated by Freshmap 2 Alpha 1.0"
"skyname" "desert"
"chaptertitle" ""
"wad" "fresh.wad;"

EOT
  );
}

function writefoot() {
  global $f;
  fwrite($f,"}\r\n");
}

function writeent($x,$y,$z,$class,$addtl) {
  global $f;
  $x *= XSCALE;
  $y *= YSCALE;
  $z *= ZSCALE;
  if( $addtl ) $addtl .= "\r\n";
  fwrite($f,<<<EOT
{
"classname" "$class"
$addtl"origin" "$x $y $z"
}

EOT
  );
}

?>
