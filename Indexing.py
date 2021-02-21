import fiona,time
from shapely.geometry import shape
import rtree

filename1 = 'districts.shp'
filename2 = 'building_areas.shp'

if __name__ == '__main__':
    with fiona.open(filename1, 'r') as layer1:
        with fiona.open(filename2, 'r') as layer2:

            index = rtree.index.Index()
            for feat1 in layer1:
                fid = int(feat1['id'])
                geom1 = shape(feat1['geometry'])
                index.insert(fid, geom1.bounds)

            for feat2 in layer2:
                geom2 = shape(feat2['geometry'])
                for fid in list(index.intersection(geom2.bounds)):
                    feat1 = layer1[fid]
                    geom1 = shape(feat1['geometry'])
                    if geom1.intersects(geom2):
                        print ('{} intersects {}'.format(feat2['id'], feat1['id']))
