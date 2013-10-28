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

js.custompre_str = ""
while 1:
  char = fin.read(1)
  if char == chr(0):
    break
  js.custompre_str += char

js.custompre_short = H()
area_cnt = I()
assert area_cnt < 100000, "area_cnt is too big: %r" % area_cnt
js.areas = []

#print 'area_cnt:', area_cnt

for i in range(area_cnt):
  area = nuthin()

  area.id =  I()

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

  # end of documented area data
  # start of L4D2-specific stuff?

  #print "End of known area - fin.tell():", fin.tell()

  area.mystery = {}
  area.mystery['flags'] = H()
  area.mystery['poodle'] = I()
  mystery_cnt = I()
  area.mystery['cheesecake'] = I()
  area.mystery['scallywags'] = []

  for j in range(mystery_cnt):
    area.mystery['scallywags'].append({
      'byte': B(),
      'int' : I()
    })

  js.areas.append(area.__dict__)


if js.version >= 6 and False:
  ladder_cnt = I()
  js.ladders = []
  for i in range(ladder_cnt):
    js.ladders[i] = {
      'id'      : I(),
      'width'   : f(),
      'top'     : unpack( 'fff', fin.read(12) ),
      'bottom'  : unpack( 'fff', fin.read(12) ),
      'length'  : f(),
      'direc'   : ['north','east','south','west'][I()],
      'dangling': I() if js.version == 6 else 0,
      'connects': [ I(), I(), I(), I(), I() ]
    }

js.custom_bytes = []
try:
  while 1:
    js.custom_bytes.append( B() )
except:
  pass

fin.close()

print json.dumps( js.__dict__, sort_keys=True, indent=4 )

