from bokeh.plotting import figure, output_file, show
from main import df

f = figure(x_axis_type='datetime', height=400, width=100, sizing_mode="stretch_width")
p = f.quad(left=df['Start Moving'], right=df['End Moving'], top=1, bottom=0, color="Green")

output_file("show.html")

show(f)