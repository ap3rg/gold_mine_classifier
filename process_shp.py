## General imports
import ee
import os
import time
import geemap
import pickle
import numpy as np
import pandas as pd
import geopandas as gpd

# Innit gee
ee.Initialize()

from shapely import wkt

# local imports
import config as conf
import functions as fun
import constants as const


# Load model
print('Loading model ...')
model = pickle.load(open(os.path.join(conf.model_path, const.model_name), 'rb'))

# get shapefle
gdf_grid = gpd.read_file(conf.grid_path).reset_index()
total_num_images = gdf_grid.geometry.shape[0]

print(f'Processing data between {const.start_date} and {const.end_date}. Name: {const.name}')
with open(conf.results_path, 'w') as results:

    results.write(f"idx\ttotal_pixels\tmine_pixels\tcloud_cover\tgeometry\n")
    start = time.time()

    with open(os.path.join(conf.out_path, "cloud_cover.tsv"), 'w') as cloud_file:
        
        for idxx, aoi in enumerate(gdf_grid.geometry):

            idx = const.start_idx + idxx

            # Load polygon to GEE to get satelite images
            polygon = ee.Geometry(aoi.__geo_interface__)

            # Get colelction
            collection = ee.ImageCollection(const.landsat_8_T1) \
                .filterDate(const.start_date, const.end_date) \
                .filterBounds(polygon) \
                .sort("CLOUD_COVER")

            image = collection.first()
            
            # Write cloud cover stats
            cloud_cover_list = list(collection.aggregate_array("CLOUD_COVER").getInfo())
            cloud_cover_str = ",".join(str(v) for v in cloud_cover_list)
            cloud_file.write(f'{idx}\t{cloud_cover_str}\n')

            try:
                cloud_cover = image.getInfo()["properties"]["CLOUD_COVER"]
            except KeyError:
                cloud_cover = None

            if idx % 50 == 0:
                print_log = True
            else:
                print_log = False

            if ((idx % 100 == 0) and (idx != 0)) or (idx == 10):
                runtime = time.time() - start
                time_left = ((runtime / idx) * total_num_images) - runtime
                print(f'\tTime elapsed: {round(runtime, 2)}.')
                print(f'\tExpected time remaining: {round(time_left, 2)}.')

            if print_log:
                print(f'Processing aoi number {idx} of {total_num_images}')


            # get data
            lats, lons, data = fun.LatLonImg(image, polygon)
            if lats.size == 0 or lons.size == 0:
                results.write(f"{idx}\t{np.nan}\t{np.nan}\t{cloud_cover}\t{wkt.dumps(aoi)}\n")
                continue

            tmp_img = image.clip(polygon)

            # Ready data for SVM
            band_arr_b1 = data.get('B1')
            band_arr_b2 = data.get('B2')
            band_arr_b3 = data.get('B3')
            band_arr_b4 = data.get('B4')
            band_arr_b5 = data.get('B5')
            band_arr_b6 = data.get('B6')
            band_arr_b7 = data.get('B7')
            band_arr_b10 = data.get('B10')
            band_arr_b11 = data.get('B11')

            # Transfer the arrays from server to client and cast as np array.
            original_size = np.array(band_arr_b1.getInfo()).shape

            np_arr_b1 = np.array(band_arr_b1.getInfo()).reshape(-1)
            np_arr_b2 = np.array(band_arr_b2.getInfo()).reshape(-1)
            np_arr_b3 = np.array(band_arr_b3.getInfo()).reshape(-1)
            np_arr_b4 = np.array(band_arr_b4.getInfo()).reshape(-1)
            np_arr_b5 = np.array(band_arr_b5.getInfo()).reshape(-1)
            np_arr_b6 = np.array(band_arr_b6.getInfo()).reshape(-1)
            np_arr_b7 = np.array(band_arr_b7.getInfo()).reshape(-1)
            np_arr_b10 = np.array(band_arr_b10.getInfo()).reshape(-1)
            np_arr_b11 = np.array(band_arr_b11.getInfo()).reshape(-1)

            data = np.stack((np_arr_b1, np_arr_b2, np_arr_b3, np_arr_b4, np_arr_b5, np_arr_b6, np_arr_b7, np_arr_b10, np_arr_b11), axis=1)
            
            y_classified = model.predict(data)
            results.write(f"{idx}\t{y_classified.shape[0]}\t{y_classified.sum()}\t{cloud_cover}\t{wkt.dumps(aoi)}\n")

            # reshape classified array to imgae size
            classified_img = y_classified.reshape(original_size)

            # Get upper left coordinate for raster centering
            min_x = lons.min()
            max_y = lats.max()

            # Cast array to float
            source_array = classified_img.astype(float)

            # Get metadata from original image
            projection = tmp_img.select('B1').projection().getInfo()["transform"]
            crs = tmp_img.select('B1').projection().getInfo()["crs"]
            res = abs(projection[0])

            # Project to correct crs
            min_x, max_y = fun.get_proj(min_x, max_y, crs)

            # Create raster
            out_path = os.path.join(conf.raster_path, f'area_{idx}.tif')
            fun.create_raster(source_array, min_x, max_y, crs, res, out_path)

        

print(f'Done. Time elapsed: {round(time.time() - start, 2)}')
