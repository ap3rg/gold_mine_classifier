# Constants for classification

name = "guainia"
model_name = "model_l8_16908px.pkl"

start_idx = 0
start_date = '2019-01-01'
end_date = '2020-01-01'
satelite_bands = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6_VCID_1', 'B6_VCID_2', 'B7', 'B8', "index", "BQA", ".geo"]
# classification_bands = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6_VCID_1', 'B6_VCID_2', 'B7']

classification_bands = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B10", 'B11']

landsat7_T1_RT = 'LANDSAT/LE07/C01/T1_RT' # USGS Landsat 7 Collection 1 Tier 1 and Real-Time data Raw Scenes
landsat7_T1_TOA = 'LANDSAT/LE07/C01/T1_TOA' # USGS Landsat 7 Collection 1 Tier 1 TOA Reflectance
landsat8_T1_L2 = 'LANDSAT/LC08/C02/T1_L2' # USGS Landsat 8 Level 2, Collection 2, Tier 1
landsat_8_T1 = 'LANDSAT/LC08/C01/T1' # USGS Landsat 8 Collection 1 Tier 1 Raw Scenes

sentinel_5 = 'COPERNICUS/S2_SR' # Sentinel-2 MSI: MultiSpectral Instrument, Level-2A 
