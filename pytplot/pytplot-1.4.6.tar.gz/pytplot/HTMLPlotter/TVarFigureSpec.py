# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from __future__ import division
import numpy as np
import pandas as pd
import math
from bokeh.plotting.figure import Figure
from bokeh.models import (CustomJS, LogColorMapper, LogTicker, LinearColorMapper, 
                          BasicTicker, ColumnDataSource, DatetimeAxis, HoverTool, 
                          Range1d, Span, Title, BoxAnnotation)
from bokeh.models.tools import BoxZoomTool
from bokeh.models.formatters import BasicTickFormatter

import pytplot
from .CustomModels.colorbarsidetitle import ColorBarSideTitle
from pytplot import tplot_utilities
from bokeh.models.formatters import DatetimeTickFormatter


dttf = DatetimeTickFormatter(microseconds=["%H:%M:%S"],                        
                             milliseconds=["%H:%M:%S"],
                             seconds=["%H:%M:%S"],
                             minsec=["%H:%M:%S"],
                             minutes=["%H:%M:%S"],
                             hourmin=["%H:%M:%S"],
                             hours=["%H:%M"],
                             days=["%F"],
                             months=["%F"],
                             years=["%F"])


class TVarFigureSpec(object):
    
    def __init__(self, tvar_name, auto_color=False, show_xaxis=False, interactive=False, y_axis_type='log'):
        self.tvar_name = tvar_name
        self.show_xaxis = show_xaxis
        if 'show_all_axes' in pytplot.tplot_opt_glob:
            if pytplot.tplot_opt_glob['show_all_axes']:
                self.show_xaxis = True
        self.interactive = interactive

        # Variables needed across functions
        self.fig = None
        self.colors = []
        self.lineglyphs = []
        self.linenum = 0
        self.zscale = 'log'
        self.zmin = 0
        self.zmax = 1
        self.callback = None
        self.interactive_plot = None
        self.fig = Figure(x_axis_type='datetime', 
                          tools=pytplot.tplot_opt_glob['tools'],
                          y_axis_type=self._getyaxistype())
        self.fig.add_tools(BoxZoomTool(dimensions='width'))
        self._format()
        
    def getaxistype(self):
        axis_type = 'time'
        link_y_axis = False
        return axis_type, link_y_axis
    
    def getfig(self):
        if self.interactive:
            return [self.fig, self.interactive_plot]
        else:
            return [self.fig]
    
    def setsize(self, width, height):
        self.fig.plot_width = width
        if self.show_xaxis:
            self.fig.plot_height = height + 22
        else:
            self.fig.plot_height = height

    def add_title(self):
        if 'title_text' in pytplot.tplot_opt_glob:
            if pytplot.tplot_opt_glob['title_text'] != '':
                title1 = Title(text=pytplot.tplot_opt_glob['title_text'],
                               align=pytplot.tplot_opt_glob['title_align'],
                               text_font_size=pytplot.tplot_opt_glob['title_size'])  
                self.fig.title = title1
                self.fig.plot_height += 22
                
    def buildfigure(self):
        self._setminborder()
        self._setxrange()
        self._setxaxis()
        self._setyrange()
        self._setzaxistype()
        self._setzrange()
        self._addtimebars()
        self._visdata()
        self._setxaxislabel()
        self._setyaxislabel()
        self._addhoverlines()
        self._addlegend()
        
    def _format(self):
        # Formatting stuff
        self.fig.grid.grid_line_color = None
        self.fig.axis.major_tick_line_color = None
        self.fig.axis.major_label_standoff = 0
        self.fig.xaxis.formatter = dttf
        self.fig.title = None
        self.fig.toolbar.active_drag = 'auto'
        if not self.show_xaxis:
            self.fig.xaxis.major_label_text_font_size = '0pt'
            self.fig.xaxis.visible = False
        self.fig.lod_factor = 100
        self.fig.lod_interval = 30
        self.fig.lod_threshold = 100

    def _setxrange(self):
        # Check if x range is not set, if not, set good ones
        if 'x_range' not in pytplot.tplot_opt_glob:
            pytplot.tplot_opt_glob['x_range'] = [np.nanmin(pytplot.data_quants[self.tvar_name].coords['time'].values),
                                                 np.nanmax(pytplot.data_quants[self.tvar_name].coords['time'].values)]

        # Bokeh uses milliseconds since epoch for some reason
        x_range = Range1d(int(pytplot.tplot_opt_glob['x_range'][0]) * 1000.0,
                          int(pytplot.tplot_opt_glob['x_range'][1]) * 1000.0)
        if self.show_xaxis:
            pytplot.lim_info['xfull'] = x_range
            pytplot.lim_info['xlast'] = x_range

        self.fig.x_range = x_range
    
    def _setyrange(self):
        if self._getyaxistype() == 'log':
            if pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][0] < 0 \
                    or pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][1] < 0:
                return
        y_range = Range1d(pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][0],
                          pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][1])
        self.fig.y_range = y_range
        
    def _setzrange(self):
        # Get Z Range
        if 'z_range' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']:
            self.zmin = pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']['z_range'][0]
            self.zmax = pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']['z_range'][1]
        else:
            dataset_temp = pytplot.data_quants[self.tvar_name].where(pytplot.data_quants[self.tvar_name] != np.inf)
            dataset_temp = dataset_temp.where(pytplot.data_quants[self.tvar_name] != -np.inf)
            self.zmax = np.float(dataset_temp.max(skipna=True).values)
            self.zmin = np.float(dataset_temp.min(skipna=True).values)

            # Cannot have a 0 minimum in a log scale
            if self.zscale == 'log':
                df, _ = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(self.tvar_name)
                zmin_list = []
                for column in df.columns:
                    series = df[column]
                    zmin_list.append(series.iloc[series.to_numpy().nonzero()[0]].min())
                self.zmin = min(zmin_list)
        
    def _setminborder(self):
        self.fig.min_border_bottom = pytplot.tplot_opt_glob['min_border_bottom']
        self.fig.min_border_top = pytplot.tplot_opt_glob['min_border_top']
        
    def _addtimebars(self):
        for time_bar in pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar']:
            time_bar_line = Span(location=time_bar['location']*1000.0,
                                 dimension=time_bar['dimension'],
                                 line_color=time_bar['line_color'],
                                 line_width=time_bar['line_width'])
            self.fig.renderers.extend([time_bar_line])

    def _set_roi_lines(self, time):
        # Locating the two times between which there's a roi
        roi_1 = pytplot.tplot_utilities.str_to_int(pytplot.tplot_opt_glob['roi_lines'][0])
        roi_2 = pytplot.tplot_utilities.str_to_int(pytplot.tplot_opt_glob['roi_lines'][1])
        # find closest time to user-requested time
        x = np.asarray(time)
        x_sub_1 = abs(x - roi_1 * np.ones(len(x)))
        x_sub_2 = abs(x - roi_2 * np.ones(len(x)))
        x_argmin_1 = np.nanargmin(x_sub_1)
        x_argmin_2 = np.nanargmin(x_sub_2)
        x_closest_1 = x[x_argmin_1]
        x_closest_2 = x[x_argmin_2]
        # Create roi box
        roi_box = BoxAnnotation(left=x_closest_1*1000.0, right=x_closest_2*1000.0, fill_alpha=0.6, fill_color='grey',
                                line_color='red', line_width=2.5)
        self.fig.renderers.extend([roi_box])
            
    def _setxaxis(self):
        xaxis1 = DatetimeAxis(major_label_text_font_size='0pt', formatter=dttf)
        xaxis1.visible = False
        self.fig.add_layout(xaxis1, 'above')
        
    def _getyaxistype(self):
        if 'y_axis_type' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']:
            return pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_axis_type']
        else:
            return 'log'
        
    def _setzaxistype(self):
        if 'z_axis_type' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']:
            self.zscale = pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']['z_axis_type']

    def _setcolors(self):          
        if 'colormap' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']:
            for cm in pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['colormap']:
                self.colors.append(tplot_utilities.return_bokeh_colormap(cm))
        else:
            self.colors.append(tplot_utilities.return_bokeh_colormap('magma'))

    def _setxaxislabel(self):
        self.fig.xaxis.axis_label = pytplot.data_quants[self.tvar_name].attrs['plot_options']['xaxis_opt']['axis_label']
        self.fig.xaxis.axis_label_text_font_size = str(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['char_size'])+'pt'

    def _setyaxislabel(self):
        self.fig.yaxis.axis_label = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['axis_label']
        self.fig.yaxis.axis_label_text_font_size = str(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['char_size'])+'pt'
        
    def _visdata(self):
        self._setcolors()
        
        x = pytplot.data_quants[self.tvar_name].coords['time'].values.tolist()
        # Add region of interest (roi) lines if applicable
        if 'roi_lines' in pytplot.tplot_opt_glob.keys():
            self._set_roi_lines(x)
        temp = [a for a in x if (a <= (pytplot.tplot_opt_glob['x_range'][1]) and a >= (pytplot.tplot_opt_glob['x_range'][0]))]
        x = temp
    
        # Sometimes X will be huge, we'll need to cut down so that each x will stay about 1 pixel in size
        step_size = 1
        num_rect_displayed = len(x)
        if self.fig.plot_width < num_rect_displayed:
            step_size = int(math.floor(num_rect_displayed/self.fig.plot_width))
            x[:] = x[0::step_size]


        # Determine bin sizes
        if 'spec_bins' in pytplot.data_quants[self.tvar_name].coords:
            df, bins = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(self.tvar_name)
            bins_vary = len(pytplot.data_quants[self.tvar_name].coords['spec_bins'].shape) > 1
            bins_increasing = pytplot.data_quants[self.tvar_name].attrs['plot_options']['spec_bins_ascending']
        else:
            df = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(self.tvar_name)
            bins = pd.DataFrame(np.arange(len(pytplot.data_quants[self.tvar_name][0]))).transpose()
            bins_vary = False
            bins_increasing = True
        # Get length of arrays
        size_x = len(x)
        size_y = len(bins.columns)
        
        # These arrays will be populated with data for the rectangle glyphs
        color = []
        bottom = []
        top = []
        left = []
        right = []
        value = []
        corrected_time = []
        
        # left, right, and time do not depend on the values in spec_bins
        for j in range(size_x-1):
            left.append(x[j]*1000.0)
            right.append(x[j+1]*1000.0)
            corrected_time.append(tplot_utilities.int_to_str(x[j]))
            
        left = left * (size_y-1)
        right = right * (size_y-1)
        corrected_time = corrected_time * (size_y-1)
        
        # Handle the case of time-varying bin sizes
        if bins_vary:
            temp_bins = bins.loc[x[0:size_x-1]]
        else:
            temp_bins = bins.loc[0]

        if bins_increasing:
            bin_index_range = range(0, size_y-1, 1)
        else:
            bin_index_range = range(size_y-1, 0, -1)

        for i in bin_index_range:
            temp = df[i][x[0:size_x-1]].tolist()
            value.extend(temp)
            color.extend(tplot_utilities.get_heatmap_color(color_map=self.colors[0], 
                                                           min_val=self.zmin, 
                                                           max_val=self.zmax, 
                                                           values=temp, 
                                                           zscale=self.zscale))
            
            # Handle the case of time-varying bin sizes
            if bins_vary:
                bottom.extend(temp_bins[i].tolist())
                if bins_increasing:
                    top.extend(temp_bins[i+1].tolist())
                else:
                    top.extend(temp_bins[i-1].tolist())
            else:
                bottom.extend([temp_bins[i]]*(size_x-1))
                if bins_increasing:
                    top.extend([temp_bins[i+1]]*(size_x-1))
                else:
                    top.extend([temp_bins[i-1]]*(size_x-1))
        
        # Here is where we add all of the rectangles to the plot
        cds = ColumnDataSource(data=dict(x=left,
                                         y=bottom,
                                         right=right, 
                                         top=top,
                                         z=color,
                                         value=value, 
                                         corrected_time=corrected_time))
        
        self.fig.quad(bottom='y', left='x', right='right', top='top', color='z', source=cds)
            
        if self.interactive:
            if 'y_axis_type' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']:
                y_interactive_log = 'log'
            else:
                y_interactive_log = 'linear'
            self.interactive_plot = Figure(plot_height=self.fig.plot_height,
                                           plot_width=self.fig.plot_width,
                                           y_range=(self.zmin, self.zmax),
                                           x_range=(pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][0],
                                                    pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][1]),
                                           y_axis_type=y_interactive_log)
            self.interactive_plot.min_border_left = 100
            spec_bins = bins
            flux = [0]*len(spec_bins)
            interactive_line_source = ColumnDataSource(data=dict(x=spec_bins, y=flux))
            self.interactive_plot.line('x', 'y', source=interactive_line_source)
            self.callback = CustomJS(args=dict(cds=cds, source=interactive_line_source), code="""
                    var geometry = cb_data['geometry'];
                    var x_data = geometry.x; // current mouse x position in plot coordinates
                    var y_data = geometry.y; // current mouse y position in plot coordinates
                    var d2 = source.data;
                    var asdf = cds.data;
                    var j = 0;
                    x=d2['x']
                    y=d2['y']
                    time=asdf['x']
                    energies=asdf['y']
                    flux=asdf['value']
                    for (i = 0; i < time.length-1; i++) {
                        if(x_data >= time[i] && x_data <= time[i+1] ) {
                            x[j] = energies[i]
                            y[j] = flux[i]
                            j=j+1
                        }
                    }
                    j=0
                    source.change.emit();
                """)

    def _addhoverlines(self):
        # Add tools
        hover = HoverTool(callback=self.callback)
        hover.tooltips = [("Time", "@corrected_time"), ("Energy", "@y"), ("Value", "@value")]
        self.fig.add_tools(hover)
        
    def _addlegend(self):
        # Add the color bar
        if 'z_axis_type' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']:
            if pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']['z_axis_type'] == 'log':
                color_mapper = LogColorMapper(palette=self.colors[0], low=self.zmin, high=self.zmax)
                color_bar = ColorBarSideTitle(color_mapper=color_mapper, ticker=LogTicker(), border_line_color=None,
                                              location=(0, 0))
                color_bar.formatter = BasicTickFormatter(precision=2)
            else:
                color_mapper = LinearColorMapper(palette=self.colors[0], low=self.zmin, high=self.zmax)
                color_bar = ColorBarSideTitle(color_mapper=color_mapper, ticker=BasicTicker(), border_line_color=None,
                                              location=(0, 0))
                color_bar.formatter = BasicTickFormatter(precision=4)
        else:
            color_mapper = LogColorMapper(palette=self.colors[0], low=self.zmin, high=self.zmax)
            color_bar = ColorBarSideTitle(color_mapper=color_mapper, ticker=LogTicker(), border_line_color=None,
                                          location=(0, 0))
            color_bar.formatter = BasicTickFormatter(precision=2)
        color_bar.width = 10
        color_bar.major_label_text_align = 'left'
        color_bar.label_standoff = 5
        color_bar.major_label_text_baseline = 'middle'
        
        color_bar.title = pytplot.data_quants[self.tvar_name].attrs['plot_options']['zaxis_opt']['axis_label']
        color_bar.title_text_font_size = str(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['char_size'])+'pt'
        color_bar.title_text_font_style = 'bold'
        color_bar.title_standoff = 20

        self.fig.add_layout(color_bar, 'right')
