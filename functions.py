import ee
import geemap
# general imports
import numpy as np

## imports for creating raster
import pyproj
import rasterio
from shapely.ops import transform
from shapely.geometry import Point
from rasterio.transform import from_origin

# local imports 
import constants as const

# Extracts latitudes, longitudes and pixel values for a given geometry
def LatLonImg(img, aoi):
    img = img.addBands(ee.Image.pixelLonLat())
    
    # There is a limit of 262144 pixels on the sampleRectangle function. (eg. 512x512px)
    data = img.sampleRectangle(region=aoi, properties=const.classification_bands, defaultValue=0)
    
    img = img.reduceRegion(reducer=ee.Reducer.toList(),\
                                        geometry=aoi,\
                                        maxPixels=1e13,\
                                        scale=10)
    try:
        lats = np.array((ee.Array(img.get("latitude")).getInfo()))
        lons = np.array((ee.Array(img.get("longitude")).getInfo()))
    except: 
        ee.ee_exception.EEException
        return np.array([]), np.array([]), data
        
    return lats, lons, data

def get_proj(lon, lat, crs):

    wgs84_pt = Point(lon, lat)

    wgs84 = pyproj.CRS('EPSG:4326')
    proj = pyproj.CRS(crs)

    project = pyproj.Transformer.from_crs(wgs84, proj, always_xy=True).transform
    proj_point = transform(project, wgs84_pt)

    return proj_point.x, proj_point.y


def create_raster(source_array, min_x, max_y, crs, res, out_path):
    
    crs = rasterio.crs.CRS.from_string(crs)

    # form_origin(min_x, max_y, pixel_width, pixel_height)
    transform = from_origin(min_x, max_y, res, res)

    dataset = rasterio.open(out_path, 'w', driver='GTiff',
                                height = source_array.shape[0], width = source_array.shape[1],
                                count=1, dtype=str(source_array.dtype),
                                crs=crs,
                                transform=transform)

    dataset.write(source_array, 1)
    dataset.close()
