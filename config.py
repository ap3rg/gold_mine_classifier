import os
import constants as const

base_path = os.path.join("data")
data_path = os.path.join(base_path, "mining")

# Paths for classification model 
model_path = os.path.join("model")
control = os.path.join(data_path, "bands_yapacana_nonMines.csv")
spectral = os.path.join(data_path, "bands_yapacana_mines.csv")

# Paths for processing (input, outputs)
grid_path = os.path.join(base_path, "geo", "guainia_ven_grid", "guainia_ven_grid.shp")
out_path = os.path.join(data_path, "classified", f'{const.satellite_name}' ,f"{const.start_date}", const.area_name)
results_path = os.path.join(out_path, "mines.tsv")
raster_path = os.path.join(out_path, "geotiff")


# Creates the folders if does not exists
for folder in [model_path, out_path, raster_path]:
    if not os.path.exists(folder):
        os.makedirs(folder)