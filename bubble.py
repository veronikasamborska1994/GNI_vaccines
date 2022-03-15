

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
import geopandas as gpd
import json
from datetime import date
import datetime as dt
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter
from bokeh.palettes import brewer

from bokeh.io.doc import curdoc
from bokeh.models import Slider, HoverTool, Select, Label
from bokeh.layouts import widgetbox, row, column
from bokeh.models import Div, Column, CustomJS

# read in population data

from os import listdir
from os.path import isfile, join

#mypath = '/Users/veronikasamborska/Desktop/GNI-Fellowship-at-The-Guardian/data_vaccines/vaccines/'
#onlyfiles = [f for f in listdir(mypath) if (isfile(join(mypath, f)) and ('.xlsx' in f ) and ('~' not in f ))]
#onlyfiles = sorted(onlyfiles)

mypath = ['https://raw.githubusercontent.com/veronikasamborska1994/GNI_vaccines/master/data/vaccines/2021-01-10.xlsx',
          'https://raw.githubusercontent.com/veronikasamborska1994/GNI_vaccines/master/data/vaccines/2021-01-17.xlsx', 
          'https://raw.githubusercontent.com/veronikasamborska1994/GNI_vaccines/master/data/vaccines/2021-01-24.xlsx', 
          'https://raw.githubusercontent.com/veronikasamborska1994/GNI_vaccines/master/data/vaccines/2021-01-31.xlsx',
          'https://raw.githubusercontent.com/veronikasamborska1994/GNI_vaccines/master/data/vaccines/2021-02-07.xlsx', 
          'https://raw.githubusercontent.com/veronikasamborska1994/GNI_vaccines/master/data/vaccines/2021-02-14.xlsx',
          'https://raw.githubusercontent.com/veronikasamborska1994/GNI_vaccines/master/data/vaccines/2021-02-21.xlsx',
          'https://raw.githubusercontent.com/veronikasamborska1994/GNI_vaccines/master/data/vaccines/2021-02-28.xlsx',
          'https://raw.githubusercontent.com/veronikasamborska1994/GNI_vaccines/master/data/vaccines/2021-03-07.xlsx', 
          'https://raw.githubusercontent.com/veronikasamborska1994/GNI_vaccines/master/data/vaccines/2021-03-14.xlsx',
          'https://raw.githubusercontent.com/veronikasamborska1994/GNI_vaccines/master/data/vaccines/2021-03-21.xlsx']




area_codes = ['East Of England','London','Midlands','North East And Yorkshire','North West','South East','South West']
date_column = []
cumulatives_names = []
cumulatives_values = []
for file in mypath:
    df = pd.ExcelFile(file) 
    names = df.sheet_names
    if 'Vaccinations by Region & Age' in names:
        df = pd.read_excel(file, 'Vaccinations by Region & Age') 
    elif 'NHS Region' in names:
        df = pd.read_excel(file, 'NHS Region') 
        
    cumulative_total_to_date = {}
  
    for i in area_codes:
        cumulative_total_to_date[i] = None
    for key in df.keys():
        if'Cumulative Total Doses to Date' in np.asarray(df[key]):
           k = key

    for code in area_codes:
        n = df[k][np.where(df['Unnamed: 1'] == code)[0]]
        cumulative_total_to_date[code] =  n.iloc[0]/50000
        
        
        
    date_column.append(np.repeat(file[-15:-5],7))
    
    cumulatives_names.append(list(cumulative_total_to_date.keys()))
    cumulatives_values.append(list(cumulative_total_to_date.values()))

import datetime
df = pd.read_excel('https://raw.githubusercontent.com/veronikasamborska1994/GNI_vaccines/master/data/Weekly-covid-admissions-and-beds-publication-210325-1.xlsx',
                  'Hosp ads & diag')


for key in df.keys():
    if 'Name' in np.asarray(df[key]):
        area_key = key
    elif datetime.datetime(2021, 1, 3, 0, 0) in np.asarray(df[key]):
        start_key = key
    end_key =df.keys()[-1]
    
week = np.arange(int(start_key[-3:]),int(end_key[-3:]),7)
columns = []
for w,ww in enumerate(week):
    columns.append([end_key[:8]+' '+str(week[w]),end_key[:8]+' '+str(week[w]+1),end_key[:8]+' '+str(week[w]+2),end_key[:8]+' '+str(week[w]+3),\
                   end_key[:8]+' '+str(week[w]+4),end_key[:8]+' '+str(week[w]+5),end_key[:8]+' '+str(week[w]+6), end_key[:8]+' '+str(week[w]+7)])
  
hosp_areas = []
hosp_values = []
area_codes = ['East of England','London','Midlands','North East and Yorkshire','North West','South East','South West']

for c in columns:
    cumulative_total_admissions = {}
      
    for i in area_codes:
        cumulative_total_admissions[i] = None
        k = 0
    for area in area_codes:
        sum_ = df[c[:]].iloc[np.where(df[area_key]== area)].sum(axis = 1)
        cumulative_total_admissions[area_codes[k]] = sum_.iloc[0]
        k+=1
    hosp_areas.append(list(cumulative_total_admissions.keys()))
    hosp_values.append(list(cumulative_total_admissions.values()))

death_df = pd.read_excel('https://raw.githubusercontent.com/veronikasamborska1994/GNI_vaccines/master/data/publishedweek112021.xlsx',
                         'Weekly figures 2021')

for key in death_df.keys():
    if 'North East' in np.asarray(death_df[key]):
        area_key_death = key
    elif datetime.datetime(2021, 1, 8, 0, 0) in np.asarray(death_df[key]):
        start_key_death = key
end_key_death = start_key_death[:8]+' '+ str(int(start_key_death[-2:])+10)

death_areas = []
death_values = []
area_codes = ['East','London','East Midlands', 'West Midlands','North East','North West','South East','South West', 'Yorkshire and The Humber']
# Combine North East with Yorkshire
date = np.repeat(np.arange(int(start_key_death[-2:]),int(end_key_death[-2:])),9)
date_str = []
for w,ww in enumerate(week): 
    date_str.append(start_key_death[:8]+' '+ str(int(float(start_key_death[-1])+w)))
    
death_areas = []
death_values = []
for d in date_str:     
    cumulative_total_death = {}
    for i in area_codes:
        cumulative_total_death[i] = None
    for area in area_codes:
        ind_area = np.where(death_df[area_key_death]== area)[0]
        cumulative_total_death[area] = death_df[d].iloc[ind_area].iloc[0] 
    cumulative_total_death['East Midlands'] = cumulative_total_death['East Midlands'] + cumulative_total_death['West Midlands']
    cumulative_total_death['North East'] = cumulative_total_death['North East'] + cumulative_total_death['Yorkshire and The Humber']
    cumulative_total_death.pop('East Midlands', None)
    cumulative_total_death.pop('Yorkshire and The Humber', None)
    death_areas.append(list(cumulative_total_death.keys()))
    death_values.append(list(cumulative_total_death.values()))

data_frame = pd.DataFrame(np.asarray([np.asarray(hosp_areas).flatten(),np.asarray(date_column).flatten(),np.asarray(hosp_values).flatten(),
                            pd.to_numeric(np.asarray(cumulatives_values).flatten()),\
                            pd.to_numeric(np.asarray(death_values).flatten())]).T,\
columns = ['area','date','hospitalisations','cumulative_vaccine','death'])

data_frame['hospitalisations'] = pd.to_numeric(data_frame.hospitalisations)
data_frame['cumulative_vaccine'] = pd.to_numeric(data_frame.cumulative_vaccine)
data_frame['death'] = pd.to_numeric(data_frame.death)

data = {}
dates = np.unique(data_frame['date'])
for year in dates:
    df_year = data_frame.iloc[np.where(data_frame['date']==year)[0]]
    df_year = df_year.drop(columns=['date'])
    data[year] = df_year.to_dict('series')

import pandas as pd
from bokeh.io import output_notebook, show, output_file

from bokeh.io import curdoc
from bokeh.layouts import layout as layout
from bokeh.models import (Button, CategoricalColorMapper, ColumnDataSource,
                          HoverTool, Label, SingleIntervalTicker, Slider,)
from bokeh.palettes import BuPu
from bokeh.plotting import figure

source = ColumnDataSource(data=data[dates[0]])

plot = figure(x_range=(float(data_frame['hospitalisations'].min())-1000, float(data_frame['hospitalisations'].max())+100),\
              y_range=(float(data_frame['death'].min())-1000, float(data_frame['death'].max())+1000), title='covid vaccines, death and hospitalisations', plot_height=300,\
             plot_width = 1000)

plot.xgrid.grid_line_color = None
plot.ygrid.grid_line_color = None

#plot.xaxis.ticker = SingleIntervalTicker(interval=100)
plot.xaxis.axis_label = "Hospitalisations"

#plot.yaxis.ticker = SingleIntervalTicker(interval=1000)
plot.yaxis.axis_label = "Deaths"

plot.xaxis.major_label_text_font_style = 'normal'
plot.yaxis.major_label_text_font_style = 'normal'
plot.yaxis.axis_label_text_font_size='15px'
plot.xaxis.axis_label_text_font_size='15px'

label = Label(x=50, y=100, text=str(data_frame['date'][0]), text_font_size='60px', text_color='#eeeeee')
plot.add_layout(label)
regions_list = np.unique(data_frame['area'])
color_mapper = CategoricalColorMapper(palette=BuPu[7], factors=list(regions_list))

source = ColumnDataSource(data=data[dates[-1]])
plot.circle( x = 'hospitalisations', y = 'death', size= 'cumulative_vaccine', source=source, fill_color={'field': 'area', 'transform': color_mapper}, fill_alpha=0.8, line_color='#7c7e71', line_width=0.5, line_alpha=0.5, legend_group='area', )

plot.add_tools(HoverTool(tooltips="@area", show_arrow=False, point_policy='follow_mouse'))

def animate_update():
    year = slider.value + 1
    if year > len(dates):
        year = -1
    slider.value = year


def slider_update(attrname, old, new):
    year = slider.value
    source.data = data[dates[year]]
    label.text = str(dates[year])

number_dates = np.arange(len(dates))
slider = Slider(start = number_dates[0], end= number_dates[-1], value=number_dates[0], step=1, title="Date")
slider.on_change('value', slider_update)


callback_id = None

def animate():
    global callback_id
    if button.label == '► Play':
        button.label = '❚❚ Pause'
        callback_id = curdoc().add_periodic_callback(animate_update, 400)
    else:
        button.label = '► Play'
        curdoc().remove_periodic_callback(callback_id)

button = Button(label='► Play', width=60)
button.on_click(animate)

layout = column(plot, widgetbox([slider,button]),sizing_mode='scale_width')


curdoc().add_root(layout)
curdoc().title = "covid vaccines, death and hospitalisations"



