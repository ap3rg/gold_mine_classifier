import os
import glob
import subprocess
from osgeo import gdal

import config as conf


files_to_mosaic = glob.glob(os.path.join(raster_path, 'area_*.tif'))
print(files_to_mosaic)
# print("Merging geoTiff to single file ...")
# cmd = f"gdal_merge.py -ps 30 -30 -o {os.path.join(raster_path, 'merged.tif')} -of gtiff"
# subprocess.call(cmd.split() + files_to_mosaic)

# print("Done.")