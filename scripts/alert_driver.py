#singleton object to get the alerts images (dates and alerts)
from utils import messages as ms 
import ipyvuetify as v
from ipywidgets import jslink
from sepal_ui import sepalwidgets as sw
import glob
import os
from functools import partial
import ee 

ee.Initialize()

available_drivers = [
    'Asset from Google Earth Engine',
    'Local alert system',
    'GLAD alerts',
    'RADD alerts'
]

class AlertIo:
    
    def __init__(self):
        # input
        self.alert_type = None
        self.start = None
        self.end = None
        self.date_file = None
        self.alert_file = None
        self.date_asset = None
        self.alert_asset = None
        self.asset_date_band = None
        self.asset_alerts_band = None
        
        # output 
        self.date = None
        self.alert = None
        
# tile class of the driver 
class DriverTile(sw.Tile):
    
    def __init__(self, io, **kwargs):
        self.io = io
        
        self.btn = sw.Btn(ms.SELECT_ALERTS, 'mdi-map-marker-check')
        self.output = sw.Alert()
        
        
        # create the inputs 
        self.set_inputs()
        inputs = [
            self.select_type,
            self.local_txt,
            self.gee_txt,
            self.glad_txt,
            self.radd_txt,
            self.picker_line,
            self.select_date_file,
            self.select_alerts_file,
            self.asset_date_line,
            self.asset_alerts_line
        ]
         
        # hide all inputs but select_type
        self.show_inputs()
        
        
        # misc
        id_ = "driver_widget"
        title = "Select your alerts"
        
        super().__init__(
                id_,
                title,
                btn=self.btn,
                output=self.output,
                inputs=inputs,
                **kwargs
        )
        
    def set_inputs (self):
        
        root_dir = os.path.expanduser('~')
        
        # select type 
        self.select_type = v.Select(items=available_drivers, label=ms.SELECT_TYPE, v_model=None)
        
        # text for each driver 
        self.local_txt = sw.Markdown(ms.LOCAL_TXT)
        self.gee_txt = sw.Markdown(ms.GEE_TXT)
        self.glad_txt = sw.Markdown(ms.GLAD_TXT)
        self.radd_txt = sw.Markdown(ms.RADD_TXT)
        
        # start/end line
        self.start_picker = sw.DatePicker('Start', xs6=True)
        self.output.bind(self.start_picker, self.io, 'start')
        
        self.end_picker = sw.DatePicker('End', xs6=True)
        self.output.bind(self.end_picker, self.io, 'end')
        
        self.picker_line = v.Layout(xs=12, row=True,  children=[self.start_picker, self.end_picker])
        
        # date file
        self.select_date_file = sw.FileInput(['.tif', '.tiff'], label=ms.SELECT_DATE_FILE)
        self.output.bind(self.select_date_file, self.io, 'date_file')
        
        # alert file 
        self.select_alerts_file = sw.FileInput(['.tif', '.tiff'], label=ms.SELECT_ALERTS_FILE)
        self.output.bind(self.select_alerts_file, self.io, 'alert_file')
        
        def update_asset_bands(widget, event, data, dropdown, obj, variable):
            
            setattr(obj.io, variable, widget.v_model)
            obj.output.add_msg(f"You selected: {widget.v_model}")
            
            # read and add the bands to the dropdown
            try:
                ee_image = ee.ImageCollection(widget.v_model).first()
                dropdown.items = [band['id'] for band in ee_image.getInfo()['bands']]
            except Exception as e: 
                obj.output.add_msg(str(e), 'error')
            return
        
        # date asset
        self.select_date_asset = v.TextField(xs8=True, label=ms.SELECT_DATE_ASSET, placeholder='users/[username]/[asset_name]', v_model=None)
        self.select_date_asset_band = v.Select(xs4=True, class_='pl-5', label= 'band', items=None, v_model=None)
        self.output.bind(self.select_date_asset_band, self.io, 'asset_date_band')
        self.select_date_asset.on_event('change', partial(update_asset_bands, dropdown= self.select_date_asset_band, obj=self, variable='date_asset'))
        
        self.asset_date_line = v.Layout(class_='pa-5', xs12=True, row=True, children=[self.select_date_asset, self.select_date_asset_band])
        
        # alert asset 
        self.select_alerts_asset = v.TextField(label=ms.SELECT_ALERTS_ASSET, placeholder='users/[username]/[asset_name]', v_model=None)
        self.select_alerts_asset_band = v.Select(xs4=True, class_='pl-5', label= 'band', items=None, v_model=None)
        self.output.bind(self.select_alerts_asset_band, self.io, 'asset_alerts_band')
        self.select_alerts_asset.on_event('change', partial(update_asset_bands, dropdown= self.select_alerts_asset_band, obj=self, variable='alert_asset'))
        
        self.asset_alerts_line = v.Layout(class_='pa-5', xs12=True, row=True, children=[self.select_alerts_asset, self.select_alerts_asset_band])
        
        return self
    
    def show_inputs(self):
        
        # hide them all but select_type
        inputs_list = [
            self.picker_line, 
            self.local_txt, 
            self.gee_txt, 
            self.glad_txt, 
            self.radd_txt,
            self.select_date_file, 
            self.select_alerts_file, 
            self.asset_date_line, 
            self.asset_alerts_line
        ]
        
        self.toggle_inputs([], inputs_list)
        
        def on_change(widget, data, event, inputs_list, obj):
            base_list = [obj.picker_line] # the date pickers are used for every type of alerts
            
            setattr(obj.io, 'alert_type', widget.v_model)
            
            if widget.v_model == available_drivers[0]: # gee assets
                fields_2_show = base_list + [obj.gee_txt, obj.asset_date_line, obj.asset_alerts_line]
                obj.toggle_inputs(fields_2_show, inputs_list)
            elif widget.v_model == available_drivers[1]: #file
                fields_2_show = base_list + [obj.local_txt, obj.select_date_file, obj.select_alerts_file]
                obj.toggle_inputs(fields_2_show, inputs_list)
            elif widget.v_model == available_drivers[2]: #glad alerts
                fields_2_show = base_list + [obj.glad_txt]
                obj.toggle_inputs(fields_2_show, inputs_list)
            elif widget.v_model == available_drivers[3]: #radd alerts
                fields_2_show = base_list + [obj.radd_txt]
                obj.toggle_inputs(fields_2_show, inputs_list)
            else:  # the type is not suported
                obj.toggle_inputs([], inputs_list)
            
            return 
        
        self.select_type.on_event('change', partial(
            on_change,
            inputs_list = inputs_list,
            obj = self
        ))
        
        return     
    