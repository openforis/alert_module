import os
import ee
import time
import sys
from datetime import datetime
sys.path.append("..") # Adds higher directory to python modules path
from utils import utils
from scripts import gdrive
from utils import parameters as pm

#initialize earth engine
ee.Initialize()

def get_alerts_dates(aoi_io, year, date_range):
    """return the julian day map of the glad alerts included between the two dates of date_range"""
    
    aoi = aoi_io.get_aoi_ee()
    if year < pm.getLastUpdatedYear():
        all_alerts = ee.ImageCollection(f'projects/glad/alert/{year}final')
    else:
        all_alerts = ee.ImageCollection('projects/glad/alert/UpdResult')
        
    # create the composit band alert_date. cannot use the alertDateXX band directly because they are not all casted to the same type
    dates = all_alerts.select(f'alertDate{year%100}').map(lambda image: image.uint16()).filterBounds(aoi).mosaic()

    # extract julian dates
    start = date_range[0].timetuple().tm_yday
    end = date_range[1].timetuple().tm_yday
    
    # masked all the images that are not between the limits dates
    date_masked = dates.updateMask(dates.gt(start).And(dates.lt(end)))
    
    return date_masked    

def get_alerts(aoi_io, year, date_masked):
    """ get the alerts from the GLAD project
    
    Args:
        aoi_name (str): Id of the Aoi to retreive the alerts
        year, (str): year of alerts in format YYYY
        date_masked (ee.Image): the image of the date filter with the given date range
        
    Returns:
        alerts (ee.FeatureCollection): the Glad alert clipped on the AOI
    """
    
    aoi = aoi_io.get_aoi_ee()
    
    if year < pm.getLastUpdatedYear():
        all_alerts = ee.ImageCollection(f'projects/glad/alert/{year}final')
    else:
        all_alerts = ee.ImageCollection('projects/glad/alert/UpdResult')
    
        
    alerts = all_alerts.select(f'conf{year%100}').filterBounds(aoi).mosaic().uint16()
    
    # use the mask of the julian alerts 
    alerts = alerts.updateMask(date_masked.mask())
    
    return alerts       
    