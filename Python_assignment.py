from osgeo import ogr, osr
import os, os.path,  mapnik,  urllib

#Set working directory
os.chdir("/home/user/Git/Python_project")
print os.getcwd()
os.chdir("data")

#Create Driver
#Set drivername to either "KML" or "ESRI Shapefile"
driverName = "ESRI Shapefile"

drv = ogr.GetDriverByName( driverName )
if drv is None:
    print "%s driver not available.\n" % driverName
else:
    print  "%s driver IS available.\n" % driverName

if driverName == "ESRI Shapefile":
    fn = "points.shp"
elif driverName == "KML":
    fn = "points.kml"

layername = "pointLayer"

# Create shape file
ds = drv.CreateDataSource(fn)
print ds.GetRefCount()

# Set spatial reference
spatialReference = osr.SpatialReference()
spatialReference.ImportFromEPSG(4326)

# Create Layer
layer=ds.CreateLayer(layername, spatialReference, ogr.wkbPoint)
layerDefinition = layer.GetLayerDefn()

# Points
coordinates = ((-122.827820, 49.140194),  (172.636225,  -43.532054))
for i in range(len(coordinates)):
    point = ogr.Geometry(ogr.wkbPoint)
    point.SetPoint(0,  coordinates[i][0],  coordinates[i][1])
    feature = ogr.Feature(layerDefinition)
    feature.SetGeometry(point)
    layer.CreateFeature(feature)
    
ds.Destroy()

##Create Mapnik map

# Set point symbol
arrow_download = urllib.URLopener()
arrow_download.retrieve("http://maps.google.com/mapfiles/arrow.png",  "arrow.png")
arrow = os.path.join("data", "arrow.png")

os.chdir("/home/user/Git/Python_project")

# Create map
map = mapnik.Map(600, 400)
map.background = mapnik.Color("steelblue")

#Create the rule and style obj
r = mapnik.Rule()
s = mapnik.Style()

polyStyle= mapnik.PolygonSymbolizer(mapnik.Color("darkred"))
pointStyle = mapnik.PointSymbolizer(mapnik.PathExpression(arrow))
r.symbols.append(polyStyle)
r.symbols.append(pointStyle)

s.rules.append(r)
map.append_style("mapStyle", s)

# Adding point layer
layerPoint = mapnik.Layer("pointLayer")
layerPoint.datasource = mapnik.Shapefile(file =os.path.join("data", "points.shp"))
layerPoint.styles.append("mapStyle")

#adding polygon
layerPoly = mapnik.Layer("polyLayer")
layerPoly.datasource = mapnik.Shapefile(file = os.path.join("data", "ne_110m_land.shp"))
layerPoly.styles.append("mapStyle")

#Add layers to map
map.layers.append(layerPoly)
map.layers.append(layerPoint)

#Set boundaries 
boundsLL = (-180, -90, 180,  90  ) #(minx, miny, maxx,maxy)
map.zoom_to_box(mapnik.Box2d(*boundsLL)) # zoom to bbox

mapnik.render_to_file(map, os.path.join("data", "endmap.png"), "png")
print "All done - check content"


