import tempfile
import lanelet2
import os
from lanelet2.core import AttributeMap, TrafficLight, Lanelet, LineString3d, Point2d, Point3d, getId, \
    LaneletMap, BoundingBox2d, BasicPoint2d, CompoundLineString3d
from lanelet2.projection import UtmProjector


def get_linestring_at_x(x):
    return LineString3d(getId(), [Point3d(getId(), x, i, 0) for i in range(0, 3)])


def get_linestring_at_y(y):
    return LineString3d(getId(), [Point3d(getId(), i, y, 0) for i in range(0, 3)])


def get_a_lanelet():
    return Lanelet(getId(), get_linestring_at_y(2), get_linestring_at_y(0))
    
def basic_2d():
    print(getId())
    p = Point2d(getId(), 1, 1)
    print(p)
    print(dir(p))
    print(p.attributes)

def basic_3d_point():
    p = Point3d(getId(), 1, 2, 3)
    p2d = lanelet2.geometry.to2D(p)
    print(p)
    print(p2d)

def basic_line_string():
    p1 = Point3d(getId(), 0, 0, 0)
    p2 = Point3d(getId(), 1, 0, 0)
    ls = LineString3d(getId(), [p1, p2])
    print(ls)
    print(ls[0])
    print(ls[1])
    print(ls.invert())
    ls.append(Point3d(getId(), 2, 0, 0))
    print(ls)

def basic_compound_line_string():
    ls1 = get_linestring_at_y(2)
    ls2 = get_linestring_at_y(0)
    compound_ls = CompoundLineString3d([ls1, ls2])
    print(compound_ls)
    print(dir(compound_ls))
    print(compound_ls.lineStrings())

def basic_lanelet():
    left_bound = get_linestring_at_y(2)
    right_bound = get_linestring_at_y(0)
    lanelet = Lanelet(getId(), left_bound, right_bound)
    lanelet.centerline = get_linestring_at_y(1)
    print(lanelet)
    print(dir(lanelet))
    print(lanelet.rightBound == right_bound)
    print(lanelet.leftBound == left_bound)
    print(lanelet.speedLimits())
    print(lanelet.centerline)

def regulatory_elements():
    lanelet = get_a_lanelet()
    light = get_linestring_at_y(3)
    regelem = TrafficLight(getId(), AttributeMap(), [light])
    lanelet.addRegulatoryElement(regelem)
    print(lanelet.regulatoryElements)

def lanelet_map():
    map = LaneletMap()
    lanelet = get_a_lanelet()
    map.add(lanelet)
    path = os.path.join(tempfile.mkdtemp(), 'mapfile.osm')
    projector = UtmProjector(lanelet2.io.Origin(49, 8.4))
    lanelet2.io.write(path, map, projector)
    mapLoad, errors = lanelet2.io.loadRobust(path, projector)
    assert mapLoad.laneletLayer.exists(lanelet.id)

if __name__ == '__main__':
    lanelet_map()