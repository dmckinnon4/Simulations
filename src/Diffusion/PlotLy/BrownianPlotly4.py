import numpy as np
import plotly
import pickle
import re

# get and unpack data
data =  pickle.load( open( "data.pkl", "rb" ) )
params, x1data, y1data, x2data, y2data = data 
numFrames, numParticles, frameChange = params

# create color list for membrane
pl_colors = []
for i in range(numFrames):
    if i < frameChange: pl_colors.append('red')
    else: pl_colors.append('green')
# colors
dot1Col = '#990000'
dot2Col = '#3b528b'
plotBcgdCol = 'white'
lineCol = '#808080'
        
fig = dict(
    layout = dict(width=500, height=240,
        xaxis1 = {'domain': [0.0, 0.44], 'anchor': 'y1', 'range': [-4.0, 4.0], 'showticklabels': False, 
            'showgrid': False, 'mirror': True, 'showline': True, 'linewidth': 3, 'linecolor': lineCol,
            'zeroline': False, 'showspikes': False},
        yaxis1 = {'domain': [0.0, 1.0], 'anchor': 'x1', 'range': [-4.0, 4.0], 'showticklabels': False, 
            'showgrid': False, 'mirror': True, 'showline': True, 'linewidth': 3, 'linecolor': lineCol, 
            'zeroline': False, 'showspikes': False},
        xaxis2 = {'domain': [0.62, 1.0], 'anchor': 'y2', 'title': 'Time', 'range': [0, numFrames], 'showline': True, 'zeroline': False,
                'showgrid': False,'showticklabels': False},
        yaxis2 = {'domain': [0.0, 1.0], 'anchor': 'x2', 'title': 'Entropy', 'range': [-10, 300], 'showline': True, 'zeroline': False,
                'ticktext': ['Equil.'], 'tickvals': [250],'tickmode': 'array','showticklabels': True},
        hovermode = False,
        plot_bgcolor = plotBcgdCol,
        margin = {'t': 4, 'b': 2, 'l': 2, 'r': 2},
    ),

    data = [
        {'type': 'scatter', # trace 0, particles
        'name': 'f12', 
        'x': np.around(x1data[0,:], decimals=3),
        'y': np.around(y1data[0,:], decimals=3),
        'mode': 'markers',
        'showlegend': False,
        'marker': {'size': 6, 'color':dot1Col},
        'xaxis': 'x1', 'yaxis': 'y1'},
            
        {'type': 'scatter', # trace 1, membrane
        'name': 'f1', 
        'x': [0.0  , 0.0], 
        'y': [-4.0,   4.0],   
        'mode': 'lines', 
        'showlegend': False,
        'line': {'color': pl_colors[0],'width': 3},
        'xaxis': 'x1', 'yaxis': 'y1'},
            
        {'type': 'scatter', # trace 2, entropy
        'name': 'f2', 
        'x': np.around(x2data[0,:], decimals=3),
        'y': np.around(y2data[0,:], decimals=3), 
        'mode': 'markers',
        'marker': {'size': 3, 'color': dot2Col}, 
        'showlegend': False, 'xaxis': 'x2', 'yaxis': 'y2'},
    ] 
)

# test initial graph layout
# plotly.offline.plot(fig, config={'displayModeBar': False}, show_link=False)

# load data into frames
frames = [dict(name=k,
               data=[dict(x = np.around(x1data[k,:], decimals=3), 
                          y = np.around(y1data[k,:], decimals=3)),  # particles
                    dict(x = [0.0  , 0.0], y = [-4.0,   4.0],       # membrane
                        line=dict(color=(pl_colors[k]))),  
                    dict(x = np.around(x2data[k,:], decimals=3),    # entropy
                         y = np.around(y2data[k,:], decimals=3), 
                       )
                   ],
               traces=[0,1,2]) for k in range(numFrames)]

updatemenus = [dict(type='buttons',
                    buttons=[dict(label='Play',
                                  method='animate',
                                  args=[[f'{k}' for k in range(numFrames)], 
                                         dict(frame=dict(duration=0, redraw=False), 
                                              transition=dict(duration=0),
                                              easing='linear',
                                              fromcurrent=True,
                                              mode='immediate')]),
                             dict(label='Pause',
                                  method='animate',
                                  args=[[None],
                                        dict(frame=dict(duration=0, redraw=False), 
                                             transition=dict(duration=0),
                                             easing='linear',
                                             fromcurrent=True,
                                             mode='immediate' )])],
                    direction= 'left', 
                    pad=dict(r=10, t=10), 
                    showactive=True, x= 0.1, y= 0, xanchor= 'right', yanchor= 'top')
            ]

sliders = [{'yanchor': 'top',
            'xanchor': 'left', 
            'currentvalue': {'font': {'size': 14, 'color': '#666'}, 'prefix': ' ', "suffix": " µs", 'visible': True, 'xanchor': 'right'},
            'transition': {'duration': 0.0, 'easing': 'linear'},
            'pad': {'b': -25, 't': 10}, # Hack to deal with transparent ticks and labels
            'len': 0.4, 'x': 0.1, 'y': 0, 
            'tickcolor': 'rgba(0,0,0,0)', 'font': {'color': 'rgba(0,0,0,0)'}, # hide ticks and labels, set transparent, leaves empty space below figure
            'steps': [{'args': [[k], {'frame': {'duration': 0.0, 'easing': 'linear', 'redraw': False},
                                      'transition': {'duration': 0, 'easing': 'linear'}}], 
                       'label': k, 'method': 'animate'} for k in range(numFrames)       
                    ]}]

fig.update(frames=frames),
fig['layout'].update(updatemenus=updatemenus,
          sliders=sliders)

 

testing = True
testing = False
if testing:
    pl1 = plotly.offline.plot(fig, filename='BrownianPlotly.html', include_plotlyjs=True,
                config={'displayModeBar': False}, show_link=False)
else:
    # Hack to remove autoplay output to include in textbook
    pl1 = plotly.offline.plot(fig, output_type='div', include_plotlyjs=False, 
                              config={'displayModeBar': False}, show_link=False)
    pl1 = re.sub("\\.then\\(function\\(\\)\\{Plotly\\.animate\\(\\'[0-9a-zA-Z-]*\\'\\)\\;\\}\\)", "", pl1)
    with open('plot1.html', 'w') as fd:
        fd.write(pl1)
