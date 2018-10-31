import plotly
import pickle
import numpy as np
import re

dataset =  pickle.load( open( "data.pkl", "rb" ) )
xdata = dataset[0]
ydata = dataset[1]

# make figure
figure = {
    'data': [],
    'layout': {},
    'frames': []
}

# fill in most of layout
figure['layout']['xaxis'] = {'range': [-4, 4], 'showticklabels': False, 'showgrid': False, 'mirror': True,
                            'showline': True, 'zeroline': True, 'zerolinecolor': '#808080', 
                            'zerolinewidth': 4,'showspikes': False}
figure['layout']['yaxis'] = {'range': [-4, 4], 'showticklabels': False, 'showgrid': False, 'mirror': True,
                            'showline': True, 'zeroline': False, 'showspikes': False}
figure['layout']['hovermode'] = False
figure['layout']['height'] = 300
figure['layout']['width'] = 400
figure['layout']['margin'] = {'b': 2, 'l': 2, 'r': 2, 't': 2}
figure['layout']['sliders'] = {'args': ['transition', {'duration': 0,'easing': 'cubic-in-out'}],
                               'plotlycommand': 'animate','visible': True}
figure['layout']['updatemenus'] = [
    {'buttons': [
        {'args': [None, {'frame': {'duration': 0, 'redraw': False}, 'fromcurrent': True, 
                         'transition': {'duration': 0, 'easing': 'quadratic-in-out'}}],
        'label': 'Play', 'method': 'animate' },
        {'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                           'transition': {'duration': 0}}],
        'label': 'Pause', 'method': 'animate' }
        ],
    'direction': 'left', 'pad': {'r': 10, 't': 10}, 'showactive': False,
    'type': 'buttons', 'x': 0.1, 'xanchor': 'right', 'y': 0, 'yanchor': 'top' }
    ]

sliders_dict = {
    'active': 0, 'yanchor': 'top', 'xanchor': 'left',
    'currentvalue': {'visible': False},
    'transition': {'duration': 0, 'easing': 'cubic-in-out'},
    'pad': {'b': 0, 't': 10},
    'len': 0.8, 'x': 0.1, 'y': 0, 'steps': [],
    'tickcolor': 'white', 'font': {'color': 'white'} # hack to hide ticks and labels, transparent would be better
    }


# make data for first frame
data_dict = {
    'x': np.around(xdata[0,:], decimals=3), # reduce precision to reduce file size
    'y': np.around(ydata[0,:], decimals=3),
    'mode': 'markers',
    'marker': {'size': 8, 'color': '#3b528b'}
    }
figure['data'].append(data_dict)
    
# all frames
for i in range(np.size(xdata,0)):
    frame = {'data': [], 'name': str(i),}
    data_dict = {
        'x': np.around(xdata[i,:], decimals=3),
        'y': np.around(ydata[i,:], decimals=3),
        'mode': 'markers',
        'marker': {'size': 8,'color': '#3b528b'}
    }
    frame['data'].append(data_dict)
    figure['frames'].append(frame)
    
    slider_step = {'args': [
        [i],
        {'frame': {'duration': 0, 'redraw': False},
        'mode': 'immediate',
        'transition': {'duration': 0}}
     ],
     'label': i,
     'method': 'animate'}
    sliders_dict['steps'].append(slider_step)
 
figure['layout']['sliders'] = [sliders_dict]


# output for testing 
pl1 = plotly.offline.plot(figure, filename='BrownianPlotly.html', include_plotlyjs=True,
            config={'displayModeBar': False}, show_link=False)

# Hack to remove autoplay output for textbook
# pl1 = plotly.offline.plot(figure, output_type='div', include_plotlyjs=False, 
#                           config={'displayModeBar': False}, show_link=False)
# pl1 = re.sub("\\.then\\(function\\(\\)\\{Plotly\\.animate\\(\\'[0-9a-zA-Z-]*\\'\\)\\;\\}\\)", "", pl1)
# with open('plot1.html', 'w') as fd:
#     fd.write(pl1)
