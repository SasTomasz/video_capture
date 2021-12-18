from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource
from main import df
# import pandas

# df = pandas.read_csv('times.csv', parse_dates=['Start Moving', 'End Moving'])
df['Start_str'] = df['Start Moving'].dt.strftime("%Y-%m-%d %H:%M:%S")
df['End_str'] = df['End Moving'].dt.strftime("%Y-%m-%d %H:%M:%S")
cds = ColumnDataSource(df)

f = figure(x_axis_type='datetime', height=400, width=100, sizing_mode="stretch_width")
p = f.quad(left='Start Moving', right='End Moving', top=1, bottom=0, color="Green", source=cds)

f.yaxis.minor_tick_line_color = None
f.yaxis.ticker = [0,1]
hover = HoverTool(tooltips = [("Start", "@Start_str"), ("End", "@End_str")])
f.add_tools(hover)

output_file("show.html")

show(f)