"""
Plots the output of smartpca or flashpca
"""

__author__ = 'Cesar Fortes-Lima'
import matplotlib.pyplot as plt
import argparse
import pandas as pd
import numpy as np
import warnings
import sys, random, csv
warnings.filterwarnings('ignore')

import pdb
from io import StringIO
from tabulate import tabulate

# Bokeh imports
from bokeh.plotting import figure, output_file, show, save
from bokeh.layouts import column
from bokeh.core.properties import value
from bokeh.palettes import all_palettes
from bokeh.models import Legend, HoverTool, LegendItem, WheelZoomTool, ColumnDataSource
from bokeh.transform import linear_cmap
from bokeh.palettes import inferno, Spectral6
#from bokeh.transform import factor_cmap, factor_mark

reload(sys)
sys.setdefaultencoding('utf8')

parser = argparse.ArgumentParser(description='Parse some args')
parser.add_argument('-i', '--input') #assumes eval in same place
parser.add_argument('-o', '--output', help='uses png or pdf suffix to determine type of file to plot')
parser.add_argument('-p', '--pattern', default=None)
parser.add_argument('--which_pcs', default='1,2', help='comma-separated list of PCs')
parser.add_argument('--title', default='')

args = parser.parse_args()


# Usage: 
# python bokeh_PCA_plot.py -i *.pca.evec -o output_name --title "" --which_pcs 1,2

evec = open(args.input)
which_pcs = map(int, args.which_pcs.split(','))
print ['PC' + str(p) + ' ' for p in which_pcs]
out = args.output+'_PC'+str(which_pcs[0])+'vsPC'+str(which_pcs[1])

eigs = {}
evec.readline()
evec_all = pd.read_csv(evec, header=None, sep='\s+')
pcs = ['ID']
pcs.extend(['PC' + str(x) for x in range(1, evec_all.shape[1]-1)])
pcs.append('PC')
evec_all.columns = pcs
iid_fid = pd.DataFrame(evec_all['ID'].str.split(':').tolist())
df = pd.concat([iid_fid, evec_all], axis=1)
df.rename(columns={0: 'FID', 1: 'IID'}, inplace=True)
source = df
source.set_index('FID')
source  = source.rename(columns={0: "FID", 1: "IID"})
fids = source.FID.unique()

if args.pattern==None:
	labels = fids
	markers = ['x', 'asterisk', 'cross', 'hex', 'circle', 'circle_cross', 'circle_x', 'diamond', 'diamond_cross', 'square', 'square_x', 'square_cross', 'triangle', 'inverted_triangle']#, 'dash'
	while len(markers) < len(fids):
		markers.extend(markers)
		markers=markers[0:len(fids)]
	
	filling = ['white']
	while len(filling) < len(fids):
		filling.extend(filling)
		filling=filling[0:len(fids)]
	
	# Gradient color pattern such as infernoor Spectral6
	#colours = inferno(len(fids))
	#filling = colours
	
	# To select random colours
	#get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF),range(n)))
	#colours = get_colors(len(fids))
	
	# To avoid light and white colours
	#Light colours: 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightsteelblue', 
	#White colors: 'antiquewhite', 'floralwhite', 'ghostwhite', 'navajowhite', 'white', 'whitesmoke', 'snow', 'honeydew', 'mintcream', 'azure', 'beige', 'aliceblue', 'seashell', 'oldlace', 'cornsilk', 'ivory', 'linen', 'lavenderblush', 'mistyrose', 'lightyellow',
	colours = ['aqua', 'aquamarine', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgray', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dodgerblue', 'firebrick', 'forestgreen', 'fuchsia', 'gainsboro', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'hotpink', 'indianred', 'indigo', 'khaki', 'lavender', 'lawngreen', 'lemonchiffon', 'lime', 'limegreen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'moccasin', 'navy', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'yellow', 'yellowgreen']
	while len(colours) < len(fids):
		colours.extend(colours)
	colours = random.sample(colours, len(fids))

# Set your own pattern
title=args.title
#title=''

# Create .csv file
# awk '$1=$1' pattern.txt > pattern.csv; sed -i 's/ | /,/g' pattern.csv; sed -i 's/ | /,/g' pattern.csv; sed -i 's/| //g' pattern.csv; sed -i 's/ |/,/g' pattern.csv; sed -i '/-----+-----/d' pattern.csv; sed -i '1d' pattern.csv
# head pattern.csv

if args.pattern!=None:
	pattern = csv.reader(open(args.pattern, 'rb'), delimiter=",")
	labels, colours, markers, filling = [], [], [], []
	
	for row in pattern:
		labels.append(row[1])
		colours.append(row[2])
		markers.append(row[3])
		filling.append(row[4])
		filling = [d if d!='None' else None for d in filling]

# Plot
output_file(args.output+'.html', mode='inline')
plot = figure(title=title, toolbar_location="above", x_axis_label="PC"+str(which_pcs[0]),y_axis_label="PC"+str(which_pcs[1]),plot_width = 2000, plot_height = 1182, 
	tools='pan,box_zoom,wheel_zoom,ywheel_zoom,undo,xzoom_in,redo,reset,save', active_scroll='wheel_zoom')
#, background_fill_color="#fafafa"

leg_1 = []

if args.pattern!=None:
	for counter,pop in enumerate(labels):
		#labels.append(pop)
		leg_1.append(( pop, [plot.scatter(x='PC'+str(which_pcs[0]), y='PC'+str(which_pcs[1]), source=source.loc[source['FID'] == pop],
			marker=markers[counter], size=8, color=colours[counter], alpha=1, muted_alpha=0.1, fill_color=filling[counter] ) ] ))

#print "labels (N=",len(fids),") = \n",labels
#print "colours = ",colours
#print "markers = ",markers
#print "filling = ",filling

if args.pattern==None:
	for counter,pop in enumerate(fids):
		#labels.append(pop)
		leg_1.append(( pop, [plot.scatter(x='PC'+str(which_pcs[0]), y='PC'+str(which_pcs[1]), source=source.loc[source['FID'] == pop],
			marker=markers[counter], size=8, color=colours[counter], alpha=1, muted_alpha=0.1, fill_color=filling[counter] ) ] ))
	f = open('pattern.txt', 'w')
	pattern = pd.DataFrame({'1_Labels':labels,'2_Colours':colours,'3_Markers':markers,'4_Filling':filling})
	f.write(tabulate(pattern, headers='keys', tablefmt='psql'))
	f.close()

plot.title.text_font_size = '25pt'
#plot.xaxis.axis_label="PC1"
plot.xaxis.axis_label_text_font_size = "23pt"
plot.xaxis.major_label_text_font_size = "20pt"
plot.xaxis.axis_label_text_font = "arial"
plot.xaxis.axis_label_text_color = "black"

#plot.yaxis.axis_label="PC2"
plot.yaxis.axis_label_text_font_size = "23pt"
plot.yaxis.major_label_text_font_size = "20pt"
plot.yaxis.axis_label_text_font = "arial"
plot.yaxis.axis_label_text_color = "black"

#Grid lines
plot.xgrid.visible = False
plot.xgrid.grid_line_alpha = 0.8
plot.xgrid.grid_line_dash = [6, 4]
plot.ygrid.visible = False
plot.ygrid.grid_line_alpha = 0.8
plot.ygrid.grid_line_dash = [6, 4]

#Legend
#legend1 = Legend(items=leg_1)#, location = (20, 20))
#plot.add_layout(legend1, 'right')

ncolumn=(len(fids)+2)/3
print "populations=",len(fids),"pop/column",ncolumn
legend1 = Legend(
    items=leg_1[0:ncolumn], location=(0, 30))

legend2 = Legend(
    items=leg_1[ncolumn:ncolumn*2], location=(0, 30))

legend3 = Legend(
    items=leg_1[ncolumn*2:], location=(0, 30))

plot.add_layout(legend1, 'right')
plot.add_layout(legend2, 'right')
plot.add_layout(legend3, 'right')
plot.legend.location = "top_right"
plot.legend.click_policy="hide"#"mute"
plot.legend.label_text_font_size = '12pt'

plot.add_tools(WheelZoomTool(), HoverTool(
 tooltips = [
	 ('ID', '@FID @IID'),
		 ]
	 ))

output_file('{}.html'.format(out))
print "Saving output to {}.html".format(out) 

save(plot)
#show(plot)
exit()

#######################

