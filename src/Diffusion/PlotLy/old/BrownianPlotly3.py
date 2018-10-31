import plotly
import pickle
import numpy as np
import re

import plotly.graph_objs as go
# get and unpack data
data =  pickle.load( open( "data.pkl", "rb" ) )
params, x1data, y1data, x2data, y2data = data 
numFrames, numParticles, frameChange = params

dot1Col = '#990000'
dot2Col = '#3b528b'
plotBcgdCol = 'white'
lineCol = '#808080'
zeroLineCol = '#cccccc'

# make figure
figure = {
    'data': [],
    'layout': {},
    'frames': []
}

# make arrays for frames
buttonArgs = []
for i in range(numFrames):
    buttonArgs.append(str(i))
steps = []
for i in range(numFrames):
    dict1 = {'frame': {'duration': 0, 'easing': 'linear', 'redraw': False}, 'transition': {'duration': 0, 'easing': 'linear'}}
    list1 = [[str(i)], dict1]
    dict2 = {'args': list1, 'method': 'animate'}
    steps.append(dict2)
    
layout1 = dict(
    xaxis1 = {'domain': [0.0, 0.44], 'anchor': 'y1', 'range': [-4, 4], 'showticklabels': False, 
              'showgrid': False, 'mirror': True, 'showline': True, 'linewidth': 3, 'linecolor': lineCol,
              'zeroline': True, 'zerolinecolor': zeroLineCol, 'zerolinewidth': 2,'showspikes': False},
    yaxis1 = {'domain': [0.0, 1.0], 'anchor': 'x1', 'range': [-4, 4], 'showticklabels': False, 
              'showgrid': False, 'mirror': True, 'showline': True, 'linewidth': 3, 'linecolor': lineCol, 
              'zeroline': False, 'showspikes': False},
    xaxis2 = {'domain': [0.6, 1.0], 'anchor': 'y2', 'title': 'Time', 'automargin': True, 'range': [0, numFrames], 
              'showticklabels': False},
    yaxis2 = {'domain': [0.0, 1.0], 'anchor': 'x2', 'title': 'Entropy', 'range': [0, 300], 
              'showticklabels': False},
    title  = '',
    height = 250,
    width = 500,
    hovermode = False,
    plot_bgcolor = plotBcgdCol,
    margin = {'t': 4, 'b': 2, 'l': 2, 'r': 2},
    updatemenus = [{'buttons': [{'args': [buttonArgs, {'frame': {'duration': 0, 'redraw': False}, 'fromcurrent': True, 'transition': {'duration': 0, 'easing': 'linear'}}], 
                                'label': 'Play', 'method': 'animate'}, 
                                {'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}], 
                                'label': 'Pause', 'method': 'animate'}], 
                                'direction': 'left', 'pad': {'r': 10, 't': 10}, 'showactive': True, 'type': 'buttons', 'x': 0.1, 'y': 0, 'xanchor': 'right', 'yanchor': 'top'}],
    sliders = [{'active': 0, 'yanchor': 'top', 'xanchor': 'left', 'currentvalue': {'visible': True, "prefix": "", "suffix": " µs", 'xanchor': 'right', 'font': {'size': 14, 'color': '#666'}},
                'transition': {'duration': 0, 'easing': 'linear'},
                'pad': {'b': 0, 't': 10}, 'len': 0.4, 'x': 0.1, 'y': 0, 
                'tickcolor': 'rgba(0,0,0,0)', 'font': {'color': 'rgba(0,0,0,0)'}, # hack to hide ticks and labels, set transparent
                'steps': steps}]
    )

figure['layout'] = layout1

dataList = [
    {'type': 'scatter', 'name': 'f1', 
    'x': np.around(x1data[0,:], decimals=3), # reduce precision to reduce file size 
    'y': np.around(y1data[0,:], decimals=3),  
    'mode': 'markers',
    'marker': {'size': 6, 'color': dot1Col}, 'showlegend': False, 'xaxis': 'x1', 'yaxis': 'y1'},
    {'type': 'scatter', 'name': 'f2', 
    'x': np.around(x2data[0,:], decimals=3),
    'y': np.around(y2data[0,:], decimals=3),
    'mode': 'markers',
    'marker': {'size': 3, 'color': dot2Col},'showlegend': False, 'xaxis': 'x2', 'yaxis': 'y2'},
    ]
figure['data'] = dataList

            
# all frames
for i in range(np.size(x1data,0)):
    frame = {'name': str(i),'data': [], 'layout': {}}
    
    trace0 = go.Scatter(
        x = np.around(x1data[i,:], decimals=3),
        y = np.around(y1data[i,:], decimals=3),
        mode = 'markers',
        marker = dict(
            size = 6,
            color = dot1Col
        )
    )
    # change zeroline to give appearance of losing barrier
    if i < frameChange:
        frame['layout'] = dict(xaxis1 = {'zeroline': True})
    else:
        frame['layout'] = dict(xaxis1 = {'zeroline': False})        
    
    trace1 = go.Scatter(
        x = np.around(x2data[i,:], decimals=3),
        y = np.around(y2data[i,:], decimals=3),
        mode = 'markers',
        marker = dict(
            size = 3,
            color = dot2Col
        )
    ) 

    frame['data'] = [trace0, trace1]
    figure['frames'].append(frame)


testing = True
# testing = False
if testing:
    pl1 = plotly.offline.plot(figure, filename='BrownianPlotly.html', include_plotlyjs=True,
                config={'displayModeBar': False}, show_link=False)
else:
    # Hack to remove autoplay output to include in textbook
    pl1 = plotly.offline.plot(figure, output_type='div', include_plotlyjs=False, 
                              config={'displayModeBar': False}, show_link=False)
    pl1 = re.sub("\\.then\\(function\\(\\)\\{Plotly\\.animate\\(\\'[0-9a-zA-Z-]*\\'\\)\\;\\}\\)", "", pl1)
    with open('plot1.html', 'w') as fd:
        fd.write(pl1)

# # plot to plotly web site. Not working.
# plotly.plotly.plot(figure, filename='Diffusion.html')
