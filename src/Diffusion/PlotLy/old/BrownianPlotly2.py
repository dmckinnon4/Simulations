import plotly
import pickle
import numpy as np
import re
# get and unpack data
data =  pickle.load( open( "data.pkl", "rb" ) )
params, x1data, y1data, x2data, y2data = data 
numFrames, numParticles, frameChange = params

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
    dict1 = {'frame': {'duration': 0, 'easing': 'linear', 'redraw': True}, 'transition': {'duration': 0, 'easing': 'linear'}}
    list1 = [[str(i)], dict1]
    dict2 = {'args': list1, 'method': 'animate'}
    steps.append(dict2)
    
layout1 = dict(
    xaxis1 = {'domain': [0.0, 0.44], 'anchor': 'y1', 'range': [-4, 4], 'showticklabels': False, 
              'showgrid': False, 'mirror': True, 'showline': True, 'zeroline': True, 
              'zerolinecolor': '#808080', 'zerolinewidth': 4,'showspikes': False},
    yaxis1 = {'domain': [0.0, 1.0], 'anchor': 'x1', 'range': [-4, 4], 'showticklabels': False, 
              'showgrid': False, 'mirror': True, 'showline': True, 'zeroline': False, 'showspikes': False},
    xaxis2 = {'domain': [0.6, 0.95], 'anchor': 'y2', 'title': 'Time', 'automargin': True, 'range': [0, numFrames]},
    yaxis2 = {'domain': [0.0, 0.95], 'anchor': 'x2', 'title': 'Entropy', 'range': [0, 300]},
    title  = '',
    height = 300,
    width = 600,
    hovermode = False,
    margin = {'t': 2, 'b': 2, 'l': 2, 'r': 2},
    updatemenus = [{'buttons': [{'args': [buttonArgs, {'frame': {'duration': 0, 'redraw': True}, 'fromcurrent': True, 'transition': {'duration': 0, 'easing': 'linear'}}], 
                                'label': 'Play', 'method': 'animate'}, 
                                {'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 0}}], 
                                'label': 'Pause', 'method': 'animate'}], 
                                'direction': 'left', 'pad': {'r': 10, 't': 10}, 'showactive': True, 'type': 'buttons', 'x': 0.1, 'y': 0, 'xanchor': 'right', 'yanchor': 'top'}],
    sliders = [{'active': 0, 'yanchor': 'top', 'xanchor': 'left', 'currentvalue': {'visible': False}, 
                'transition': {'duration': 0, 'easing': 'linear'},
                'pad': {'b': 0, 't': 10}, 'len': 0.4, 'x': 0.1, 'y': 0, 
                'tickcolor': 'white', 'font': {'color': 'white'}, # hack to hide ticks and labels, transparent would be better
                'steps': steps}]
    )

figure['layout'] = layout1

dataList = [
    {'type': 'scatter', 'name': 'f1', 
    'x': np.around(x1data[0,:], decimals=3), # reduce precision to reduce file size 
    'y': np.around(y1data[0,:], decimals=3),  
    'mode': 'markers',
    'marker': {'size': 8, 'color': '#3b528b'}, 'showlegend': False, 'xaxis': 'x1', 'yaxis': 'y1'},
    {'type': 'scatter', 'name': 'f2', 
    'x': np.around(x2data[0,:], decimals=3),
    'y': np.around(y2data[0,:], decimals=3),
    'mode': 'markers',
    'marker': {'size': 3, 'color': '#3b528b'}, 'showlegend': False, 'xaxis': 'x2', 'yaxis': 'y2'},
    ]
figure['data'] = dataList

            
# all frames
for i in range(np.size(x1data,0)):
    frame = {'name': str(i),'data': [], 'layout': {}}
    if i < frameChange:
        data_dict1 = {
            'x': np.around(x1data[i,:], decimals=3),
            'y': np.around(y1data[i,:], decimals=3),
            'mode': 'markers',
            'marker': {'size': 8,'color': '#3b528b'}
            }
        frame['layout'] = dict(xaxis1 = {'zeroline': True})
        
    else:
        data_dict1 = {
            'x': np.around(x1data[i,:], decimals=3),
            'y': np.around(y1data[i,:], decimals=3),
            'mode': 'markers',
            'marker': {'size': 8,'color': '#3b528b'}
            }
        frame['layout'] = dict(xaxis1 = {'zeroline': False})

    data_dict2 = {
        'x': np.around(x2data[i,:], decimals=3),
        'y': np.around(y2data[i,:], decimals=3),
        'mode': 'markers',
        'marker': {'size': 3,'color': '#3b528b'}
        }
    frame['data'] = [data_dict1, data_dict2]
    figure['frames'].append(frame)



# output for testing 
# pl1 = plotly.offline.plot(figure, filename='BrownianPlotly.html', include_plotlyjs=True,
#             config={'displayModeBar': False}, show_link=False)

# Hack to remove autoplay output for textbook
pl1 = plotly.offline.plot(figure, output_type='div', include_plotlyjs=False, 
                          config={'displayModeBar': False}, show_link=False)
pl1 = re.sub("\\.then\\(function\\(\\)\\{Plotly\\.animate\\(\\'[0-9a-zA-Z-]*\\'\\)\\;\\}\\)", "", pl1)
with open('plot1.html', 'w') as fd:
    fd.write(pl1)
