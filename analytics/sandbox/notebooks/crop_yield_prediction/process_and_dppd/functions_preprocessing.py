# Import packages
import pandas as pd
import os
import geopandas as gpd
import matplotlib.pyplot as plt
import rasterio
from statsmodels.tsa.seasonal import STL
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime as dt
from matplotlib.colors import TwoSlopeNorm
import time
from rasterstats import zonal_stats
from osgeo import gdal
import re
import os
import geopandas as gpd
import numpy as np
import rasterio
import rasterio.mask

import warnings
warnings.filterwarnings('ignore')

# We start by rescaling
def rescale(j, file_path, nodata_value, Scaling, Offset, dest_path, new_name):
    tiff_open = gdal.Open(file_path) # open the GeoTIFF we want to rescale
    band = tiff_open.GetRasterBand(1) # Select the band
    tiff_array = band.ReadAsArray() # Assign raster values to a numpy nd array

    old_ndv = tiff_open.GetRasterBand(1).GetNoDataValue()
    #tiff_open.GetRasterBand(1).SetNoDataValue(nodata_value) # value which has been assigned for the nodata
    #nodata_value_new = -9999 # new data value
    if old_ndv != None:
        tiff_array_new = np.where(tiff_array == old_ndv, nodata_value, tiff_array) # Rescale pixel values and change nodatavalue to -9999
    else:
        tiff_array_new = np.copy(tiff_array)

    tiff_array_new = np.where(tiff_array_new != nodata_value, tiff_array_new * Scaling + Offset, nodata_value) # Rescale pixel values and change nodatavalue to -9999

    col = tiff_open.RasterXSize # number of columns
    rows = tiff_open.RasterYSize # number of rows
    driver = tiff_open.GetDriver()

    # Create a new raster to save the average-values
    new_raster = driver.Create(dest_path + new_name, col, rows, 1, gdal.GDT_Float32)

    # Copy the properties of the original raster
    new_raster.SetGeoTransform(tiff_open.GetGeoTransform())
    new_raster.SetProjection(tiff_open.GetProjection())

    # Add the average values to newly created raster
    new_raster.GetRasterBand(1).WriteArray(tiff_array_new)
    new_raster.GetRasterBand(1).SetNoDataValue(nodata_value)

    # close the raster
    new_raster = None
    del new_raster

def rescale_unstable(j, file_path, nodata_value, Scaling, Offset, dest_path, new_name, date_format):
    date = re.search('.*\_(.\d+?)\_.*', j).group(1)
    date_time = str(date[date_format[0]:date_format[1]]) + '-' + str(date[date_format[2]:date_format[3]]) + '-' + str(date[date_format[4]:date_format[5]]) # YEAR-MONTH-DAY

    tiff_open = gdal.Open(file_path) # open the GeoTIFF we want to rescale
    band = tiff_open.GetRasterBand(1) # Select the band
    tiff_array = band.ReadAsArray() # Assign raster values to a numpy nd array

    old_ndv = tiff_open.GetRasterBand(1).GetNoDataValue()
    #tiff_open.GetRasterBand(1).SetNoDataValue(nodata_value) # value which has been assigned for the nodata
    #nodata_value_new = -9999 # new data value
    if old_ndv != None:
        tiff_array_new = np.where(tiff_array == old_ndv, nodata_value, tiff_array) # Rescale pixel values and change nodatavalue to -9999
    else:
        tiff_array_new = np.copy(tiff_array)

    tiff_array_new = np.where(tiff_array_new != nodata_value, tiff_array_new * Scaling + Offset, nodata_value) # Rescale pixel values and change nodatavalue to -9999

    col = tiff_open.RasterXSize # number of columns
    rows = tiff_open.RasterYSize # number of rows
    driver = tiff_open.GetDriver()

    # Create a new raster to save the average-values
    new_raster = driver.Create(dest_path + new_name + date_time + '.tif', col, rows, 1, gdal.GDT_Float32)

    # Copy the properties of the original raster
    new_raster.SetGeoTransform(tiff_open.GetGeoTransform())
    new_raster.SetProjection(tiff_open.GetProjection())

    # Add the average values to newly created raster
    new_raster.GetRasterBand(1).WriteArray(tiff_array_new)
    new_raster.GetRasterBand(1).SetNoDataValue(nodata_value)

    # close the raster
    new_raster = None
    del new_raster

# For each of the NDVI images, we crop the Geotiff file to Leaf Area Index in Telangana
def crop_image(j, file_path, boundary, dest_path):
    with rasterio.open(file_path) as src:
        out_image, out_transform = rasterio.mask.mask(src, boundary.geometry, crop=True)
        out_meta = src.meta

    out_meta.update({"driver": "GTiff",
                        "height": out_image.shape[1],
                        "width": out_image.shape[2],
                        "transform": out_transform})#,
                        #"nodata": ndv,
                        #"dtype": rasterio.float64})

    # photometric = 'YCbCr'
    # photometric = 'RGB', compress = 'JPEG'
    # Save the Geotiff file to Leaf Area Index in Telangana
    with rasterio.open(dest_path + j, "w", **out_meta) as dest:
        dest.write(out_image)