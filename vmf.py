from random import randint

# boilerplate at top of file
class Vmf:
	def __init__(self, filename):
		self.num = 1
		self.f = open(filename, 'w')
		data = """versioninfo
{
	"editorversion" "400"
	"editorbuild" "5454"
	"mapversion" "2"
	"formatversion" "100"
	"prefab" "0"
}
visgroups
{
}
viewsettings
{
	"bSnapToGrid" "1"
	"bShowGrid" "1"
	"bShowLogicalGrid" "0"
	"nGridSpacing" "32"
	"bShow3DGrid" "0"
}
"""
		self.f.write(data)

	# start writing the worldspawn
	def worldspawn(self):
		data = """world
{
	"id" "%d"
	"mapversion" "2"
	"classname" "worldspawn"
	"detailmaterial" "detail/detailsprites"
	"detailvbsp" "detail.vbsp"
	"maxpropscreenwidth" "-1"
	"musicpostfix" "Waterfront"
	"skyname" "sky_l4d_rural02_hdr"
"""
		self.f.write(data % self.num)
		self.num += 1

	# write a solid axis-aligned block in an entity or the worldspawn
	def block(self, block, tex, displacement=None):
		data = '\tsolid\n\t{\n\t\t"id" "%d"\n'
		self.f.write(data % self.num)
		self.num += 1

		x0,x1,y0,y1,z0,z1 = block.x0,block.x1,block.y0,block.y1,block.z0,block.z1 

		#      point a                        uaxis            vaxis              rotation
		#      |         point b              |      ushift    |        vshift    |
		#      |         |         point c    |      |  uscale |        |  vscale |
		#      |         |         |          |      |  |      |        |  |      |
		ls = [[x0,y1,z1, x1,y1,z1, x1,y0,z1,  1,0,0, 0, 0.25,  0,-1, 0, 0, 0.25,  0],
		      [x0,y0,z0, x1,y0,z0, x1,y1,z0,  1,0,0, 0, 0.25,  0,-1, 0, 0, 0.25,  0],
		      [x0,y1,z1, x0,y0,z1, x0,y0,z0,  0,1,0, 0, 0.25,  0, 0,-1, 0, 0.25,  0],
		      [x1,y1,z0, x1,y0,z0, x1,y0,z1,  0,1,0, 0, 0.25,  0, 0,-1, 0, 0.25,  0],
		      [x1,y1,z1, x0,y1,z1, x0,y1,z0,  1,0,0, 0, 0.25,  0, 0,-1, 0, 0.25,  0],
		      [x1,y0,z0, x0,y0,z0, x0,y0,z1,  1,0,0, 0, 0.25,  0, 0,-1, 0, 0.25,  0]]

		for (sidenum,side) in enumerate(ls):
			ax,ay,az, bx,by,bz, cx,cy,cz,  ux,uy,uz, uh, us,  vx,vy,vz, vh, vs,  rot = side
			data = """		side
		{
			"id" "%d"
			"plane" "(%f %f %f) (%f %f %f) (%f %f %f)"
			"material" "%s"
			"uaxis" "[%f %f %f %f] %f"
			"vaxis" "[%f %f %f %f] %f"
			"rotation" "%f"
			"lightmapscale" "16"
			"smoothing_groups" "0"
"""
			self.f.write(data % (self.num, ax,ay,az, bx,by,bz, cx,cy,cz,
			                     tex,  ux,uy,uz, uh, us,  vx,vy,vz, vh, vs,  rot))

			if( displacement and displacement.sidenum==sidenum ):
				self.displace(displacement)

			self.f.write("		}\n")
			self.num += 1
		self.f.write('\t}\n')

	# output displacement information
	def displace(self,dis):
		n = dis.nverts

		data = """			dispinfo
			{
				"power" "%d"
				"startposition" "[%d %d %d]"
				"flags" "0"
				"elevation" "0"
				"subdiv" "0"
				normals
				{
"""
		self.f.write(data % (dis.power, dis.x,dis.y,dis.z))

		#output normals
		for i in range(n):
			self.f.write('\t\t\t\t\t"row%d" "' % i)
			self.f.write(' '.join( n*["0 0 1"] ))
			self.f.write('"\n')

		#close normals, open distances
		self.f.write("\t\t\t\t}\n\t\t\t\tdistances\n\t\t\t\t{\n")

		#output distances
		for i in range(n):
			self.f.write('\t\t\t\t\t"row%d" "' % i)
			self.f.write(' '.join( [str(x) for x in dis.dists[n*i:n*(i+1)]] ))
			self.f.write('"\n')

		#close distances, open alphas
		self.f.write("\t\t\t\t}\n\t\t\t\talphas\n\t\t\t\t{\n")

		#output alphas
		for i in range(n):
			self.f.write('\t\t\t\t\t"row%d" "' % i)
			self.f.write(' '.join( [str(x) for x in dis.alphas[n*i:n*(i+1)]] ))
			self.f.write('"\n')

		#close alphas, close dispinfo
		self.f.write("\t\t\t\t}\n\t\t\t}\n")

	# end of any entity or the worldspawn
	def end_ent(self):
		self.f.write("}\n")

	# boilerplate at end of file
	def close(self):
		data = """cameras
{
	"activecamera" "-1"
}
cordons
{
	"active" "0"
}
"""
		self.f.write(data)
		self.f.close()

	def fog_controller(self,z,y,x):
		data = """entity
{
	"id" "%d"
	"classname" "env_fog_controller"
	"angles" "0 0 0"
	"farz" "2200"
	"fogblend" "0"
	"fogcolor" "35 43 50"
	"fogcolor2" "255 255 255"
	"fogdir" "1 0 0"
	"fogenable" "1"
	"fogend" "2200"
	"foglerptime" "5"
	"fogmaxdensity" "1"
	"fogstart" "0"
	"HDRColorScale" "1"
	"heightFogDensity" "0.0"
	"heightFogMaxDensity" "1.0"
	"heightFogStart" "0.0"
	"maxcpulevel" "0"
	"maxdxlevel" "0"
	"maxgpulevel" "0"
	"mincpulevel" "0"
	"mindxlevel" "0"
	"mingpulevel" "0"
	"spawnflags" "1"
	"targetname" "AutoInstance1-fog_master"
	"use_angles" "0"
	"origin" "%d %d %d"
}
"""
		self.f.write(data % (self.num,x,y,z))
		self.num += 1

	def light_environment(self,z,y,x):
		data = """
entity
{
	"id" "%d"
	"classname" "light_environment"
	"_ambient" "235 236 183 20"
	"_ambientHDR" "235 236 183 20"
	"_AmbientScaleHDR" "0.7"
	"_light" "255 255 255 200"
	"_lightHDR" "-1 -1 -1 1"
	"_lightscaleHDR" "0.7"
	"angles" "-60 236 0"
	"pitch" "-19"
	"SunSpreadAngle" "5"
	"origin" "%d %d %d"
}
"""
		self.f.write(data % (self.num,x,y,z))
		self.num += 1

	def info_survivor_position(self,z,y,x):
		data = """
entity
{
	"id" "%d"
	"classname" "info_survivor_position"
	"angles" "0 0 0"
	"Order" "1"
	"origin" "%d %d %d"
}
"""
		self.f.write(data % (self.num,x,y,z))
		self.num += 1

	def info_player_start(self,z,y,x):
		data = """
entity
{
	"id" "%d"
	"classname" "info_player_start"
	"angles" "0 0 0"
	"Order" "1"
	"origin" "%d %d %d"
}
"""
		self.f.write(data % (self.num,x,y,z))
		self.num += 1

# vim: ts=8 sw=8 noet
