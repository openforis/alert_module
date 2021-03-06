########################
##         GEE        ##
########################
GEE_SELECT = 'Select a year'
GEE_INTRO = 'Click on "Run GEE process" to launch the process on your GEE account'
GEE_BTN = "Run GEE process"
NO_AOI = "The input are not correctly set up, please provide an asset in step 1"
NO_YEAR = "The input are not correctly set up, please provide a year for your alerts"
GLAD_TXT = """
This data set, created by the [GLAD](https://glad.geog.umd.edu) (Global Land Analysis & Discovery) lab at the University of Maryland is the first Landsat-based alert system for tree cover loss. To retreive the alert you just need to select the date range you're interested in.  

- dates need to be in the same year
"""
LOCAL_TXT ="""
The locally produced files need to be in the following format:  
  
- the alert file : a **.TIF** file with value 1 if an alert exist 0 elsewhere. You can use other value to described other type of alerts (likely etc...). Contact the contributors via the issue panel if help is needed.
- The date file : a **.TIF** file with the julian date of the alerts (number of days since 01/01/0001), 0 elsewhere. it will be used by the driver to filter the useful alerts. If you don't have this file and you want to consider every alerts in your alert file. duplicate it and replace all the non zero by a know date (21/09/2020 = 737689).
"""
GEE_TXT = """
The alerts system coming from GEE need to be :  

- the alerts : any gee **ImageCollection** with an alert band. 1 when there is an alert 0 elsewhere  
- the alert dates : any gee **ImageCollection** with an date band. the julian date of the alerts (number of days since 01/01/0001), 0 elsewhere. it will be used by the driver to filter the useful alerts. If you don't have this file and you want to consider every alerts in your alert file. duplicate it and replace all the non zero by a know date (21/09/2020 = 737689).  
"""

RADD_TXT = """
The RADD dataset (RAdar for Detecting Deforestation) developed by [Wageningen University](https://www.wur.nl/en/Research-Results/Chair-groups/Environmental-Sciences/Laboratory-of-Geo-information-Science-and-Remote-Sensing/Research/Sensing-measuring/RADD-Forest-Disturbance-Alert.htm) is a alert system based on sentinel-1 radar imagery.

- Covering Primary humid tropical forest of Africa (25 countries)
"""
NO_FILES = "The Downloading of your alerts on GEE has failed. Please see your GEE code editor for more information about the crash. It is usely because you are out of the geographic boundaries of your alert system."

######################
##     sepal        ##
######################
SEPAL_BTN = "Run Sepal process"
NO_PROCESS = "No process to display"
NO_TASK = "The GEE process has not been completed, launch it or run a status check through step 2."
ALREADY_DONE = "This computation has already been performed. You can find your results in the alert_result folder of your computer"
COMPUTAION_COMPLETED = "Computation complete"
START_SEPAL = "The process has been launch on your SEPAL account"
CSV_BTN = "Download .csv distribution"
PNG_BTN = "Download hist in .png"
TIF_BTN = "Download .tif alerts tile"
MERGE_TILE = "Merge gee tiles"
IDENTIFY_PATCH = "Identify all unique patch"
PATCH_SIZE = "Compute patch size"
COMPRESS_FILE= "Compress file"
DISPLAY_RESULT = "Displaying the results"
NO_DISPLAY = "The computation is completed but the file is to big to be open on the fly. Please download the .tif file and open it on your local GIS."
PROCESS_TXT = """
Alert analysis process steps are:  

- Create patches of alerts as a raster (`.tif`)
- Compute the distribution of the alerts patches (`.csv`)
"""
NO_ALERTS = "the alert map is empty. There are no deforestation alerts on this area for the selected time period."

#####################################
##           msg drivers           ##
#####################################
WRONG_DRIVER = "The selected alert type is not supported by this module"
SELECT_ALERTS = "Select these alerts"
SELECT_TYPE = "Select the alert type"
SELECT_DATE_FILE = "Select the date file"
SELECT_ALERTS_FILE = "Select the alerts file"
SELECT_DATE_ASSET = "Select date asset"
SELECT_ALERTS_ASSET = "Select alerts asset"
WRONG_YEAR = "The GLAD alert dataset is build to work only on one single year. Please provide two dates in the same year instead of your first choice"
TOO_EARLY = 'The GLAD alert dataset has been released in 2017 no alerts are provided for previous years.'
RADD_TOO_EARLY = 'The RADD alert dataset has been released in 2019 no alerts are provided for previous years.'
TASK_COMPLETED = "The task {0} launched on your GEE account is now completed"
ALREADY_COMPLETED = "The task {0} has already been completed on your GEE account"
TASK_RUNNING = "The task {} is runnning on your GEE account"
