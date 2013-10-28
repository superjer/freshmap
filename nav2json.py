#!/usr/bin/python

import sys
import json
from struct import unpack, pack, pack_into

if len(sys.argv) == 2:
  fin = open(sys.argv[1], "rb")
else:
  fin = sys.stdin

if not fin:
  sys.exit("Can't open input file or stream!")

class nuthin: pass
js = nuthin()

# shorthand unpackin!
I = lambda: unpack( 'I', fin.read(4) )[0]
H = lambda: unpack( 'H', fin.read(2) )[0]
B = lambda: unpack( 'B', fin.read(1) )[0]
f = lambda: unpack( 'f', fin.read(4) )[0]

goodfloat = lambda x: abs(x) > 0.001 and abs(x) < 4096.0

magic = "%X" % I()
if magic != 'FEEDFACE':
  sys.exit("This is not a nav file!")

js.version = I()
if js.version > 16 or js.version <= 2:
  sys.exit("Version %d not supported! (3-16 only)" % js.version)

if js.version >= 10:
  js.subversion = I()

if js.version <= 8:
  aflags_sz = 1
elif js.version < 13:
  aflags_sz = 2
else:
  aflags_sz = 4

js.bsp_size = I()

if js.version >= 14:
  js.is_anal = B()

if js.version >= 5:
  place_cnt = H()
  assert place_cnt < 1024, "place_cnt is too big: %r" % place_cnt
  js.places = {}

  for i in range(place_cnt):
    sz = H()
    js.places[i+1] = fin.read(sz-1)
    B() # throw away null terminator byte

  if js.version > 11:
    js.has_unnamed_areas = B()

js.custom_str = ""
while 1:
  char = fin.read(1)
  if char == chr(0):
    break
  js.custom_str += char

js.custom_short = H()
area_cnt = I()
assert area_cnt < 100000, "area_cnt is too big: %r" % area_cnt
js.areas = []

print 'area_cnt:', area_cnt

next_area = 1

for i in range(area_cnt):
  area = nuthin()

  area.id =  I()
  if area.id != next_area:
    print "area.id (%d) != next_area (%d)" % (area.id, next_area)
  next_area = max(area.id, next_area) + 1

  if aflags_sz == 1:
    area.flags = B()
  elif aflags_sz == 2:
    area.flags = H()
  else:
    area.flags = I()

  area.corner_nw = unpack( 'fff', fin.read(12) )
  area.corner_se = unpack( 'fff', fin.read(12) )
  area.corner_ne_z = f()
  area.corner_sw_z = f()

  area.connections = { 'north': [], 'east': [], 'south': [], 'west': [] }

  for direc in area.connections:
    conn_cnt = I()
    assert conn_cnt < 100, "conn_cnt for %s is too big: %r" % (direc, conn_cnt)
    #print "conn_cnt:", direc, conn_cnt
    for k in range(conn_cnt):
      area.connections[direc].append( I() )

  #print area.connections

  spot_cnt = B()
  assert spot_cnt < 10, "spot_cnt is too big: %r" % spot_cnt
  #print "spot_cnt:", spot_cnt
  area.hiding_spots = []
  for j in range(spot_cnt):
    area.hiding_spots.append({
      'id':    I(),
      'pos':   unpack( 'fff', fin.read(12) ),
      'flags': B()
    })

  #print area.hiding_spots

  if js.version < 15:
    eatme = B()
    assert eatme < 1000000, "eatme is too big: %r" % eatme
    #print "eatme:", eatme
    for j in range(eatme):
      I()
      I()
      B()
      I()
      B()

  encounter_cnt = I()
  assert encounter_cnt < 100, "encounter_cnt is too big: %r" % encounter_cnt
  #print "encounter_cnt:", encounter_cnt
  area.encounters = []
  for j in range(encounter_cnt):
    encounter = {
      'from_id' : I(),
      'from_dir': B(),
      'to_id'   : I(),
      'to_dir'  : B(),
    }
    spot_cnt = B()
    spots = []
    for k in range(spot_cnt):
      spots.append({
        'id': I(),
        't' : B(),
      })
    encounter['spots'] = spots
    area.encounters.append(encounter)

  if js.version >= 5:
    area.place_id = H()

  if js.version >= 7:
    area.ladders = { 'up':[], 'down':[] }
    for direc in area.ladders:
      ladder_cnt = I()
      assert ladder_cnt < 10, "ladder_cnt is too big: %r" % ladder_cnt
      for j in range(ladder_cnt):
        area.ladders[direc].append( I() )

  if js.version >= 8:
    area.earliest = unpack( 'ff', fin.read(8) )

  if js.version >= 11:
    area.light_nw = f()
    area.light_ne = f()
    area.light_se = f()
    area.light_sw = f()

  if js.version >= 16:
    vis_area_cnt = I()
    assert vis_area_cnt < 100, "vis_area_cnt is too big: %r" % vis_area_cnt
    area.vis_areas = []
    for j in range(vis_area_cnt):
      area.vis_areas.append({
        'id'   : I(),
        'attrs': B()
      })
    area.inherit_vis_from = I()

  print "End of known area - fin.tell():", fin.tell()

  # let's attempt to suss out the start of the next area :/
  seekto = fin.tell()
  area.xtra = []
  readahead = 4 + aflags_sz + 12
  for j in range(readahead):
    area.xtra.append( B() )

  while 1:
    possible_next = area.xtra[-readahead]
    should_be_zeros = area.xtra[-readahead+1:-readahead+4]
    zeros_ok = (should_be_zeros == [ 0, 0, 0 ])
    fx = unpack( 'f', pack( 'BBBB', area.xtra[-12], area.xtra[-11], area.xtra[-10], area.xtra[-9] ) )[0]
    fy = unpack( 'f', pack( 'BBBB', area.xtra[ -8], area.xtra[ -7], area.xtra[ -6], area.xtra[-5] ) )[0]
    fz = unpack( 'f', pack( 'BBBB', area.xtra[ -4], area.xtra[ -3], area.xtra[ -2], area.xtra[-1] ) )[0]
    if zeros_ok:
      print "IDOK (%d) for (%d) -- floats: %f %f %f" % (possible_next, next_area, fx, fy, fz)
    if zeros_ok and goodfloat(fx) and goodfloat(fy) and goodfloat(fz):
      break
    try:
      area.xtra.append( B() )
    except:
      break
    seekto += 1

  if i != area_cnt - 1:
    del area.xtra[-readahead:]
    fin.seek(seekto)

  print "======= Area read ======="
  print area.__dict__
  print ''

  js.areas.append(area.__dict__)

print json.dumps( js.__dict__, sort_keys=True, indent=4 )

