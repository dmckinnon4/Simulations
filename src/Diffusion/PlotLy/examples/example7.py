import numpy as np
import plotly
from plotly.offline import download_plotlyjs, init_notebook_mode,  iplot
init_notebook_mode(connected=True)

pl_colors = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)',
                         'rgb(44, 160, 44)', 'rgb(214, 39, 40)',
                         'rgb(148, 103, 189)', 'rgb(140, 86, 75)',
                         'rgb(227, 119, 194)', 'rgb(127, 127, 127)',
                         'rgb(188, 189, 34)', 'rgb(23, 190, 207)']

fig = dict(
    layout = dict(width=900, height=500,
        xaxis1 = {'domain': [0.0, 0.44], 'anchor': 'y1', 'title': '1', 'range': [-2.25, 3.25]},
        yaxis1 = {'domain': [0.0, 1.0], 'anchor': 'x1', 'title': 'y', 'range': [-1, 11]},
        xaxis2 = {'domain': [0.56, 1.0], 'anchor': 'y2', 'title': '2', 'range': [-2.25, 3.25]},
        yaxis2 = {'domain': [0.0, 1.0], 'anchor': 'x2', 'title': 'y', 'range': [-1, 11]},
        title  = '',
        margin = {'t': 50, 'b': 50, 'l': 50, 'r': 50},
    ),

    data = [
        {'type': 'scatter', # This trace is identified inside frames as trace 0
         'name': 'f1', 
         'x': [-2.  , -1.  ,  0.01,  1.  ,  2.  ,  3.  ], 
         'y': [  4,   1,   1, 1,   4,   9], 
         'hoverinfo': 'name+text', 
         'marker': {'opacity': 1.0, 'symbol': 'circle', 'line': {'width': 0, 'color': 'rgba(50,50,50,0.8)'}},
         'line': {'color': 'rgba(255,79,38,1.000000)'}, 
         'mode': 'markers+lines', 
         'fillcolor': 'rgba(255,79,38,0.600000)', 
         'legendgroup': 'f1',
         'showlegend': True, 
         'xaxis': 'x1', 'yaxis': 'y1'},
        {'type': 'scatter', # This trace is identified inside frames as trace 1
        'name': 'f12', 
        'x': -1.5+4.25*np.random.rand(20),
        'y': 1.5+7.5*np.random.rand(20),
        'mode': 'markers',
        'marker': {'size': 10, 'color':'blue'},
        'xaxis': 'x1', 'yaxis': 'y1'},
        {'type': 'scatter', # # This trace is identified inside frames as trace 2
         'name': 'f2', 
         'x': [-2.  , -1.  ,  0.01,  1.  ,  2.  ,  3.  ], 
         'y': [  2.5,   1,   1, 1,   2.5,   1], 
         'hoverinfo': 'name+text', 
         'marker': {'opacity': 1.0, 'symbol': 'circle', 'line': {'width': 0, 'color': 'rgba(50,50,50,0.8)'}}, 
         'line': {'color': 'rgba(79,102,165,1.000000)'}, 
         'mode': 'markers+lines', 'fillcolor': 'rgba(79,102,165,0.600000)', 
         'legendgroup': 'f2', 'showlegend': True, 'xaxis': 'x2', 'yaxis': 'y2'},
    ]

    
)
#iplot(fig)

frames = [dict(name=k,
               data=[dict(y=10*np.random.rand(6)),
                   dict(y=1.5+7.5*np.random.rand(20),
                        marker=dict(color=np.random.choice(pl_colors))),
                   dict(y=10*np.random.rand(6),
                       )
                   ],
               traces=[0,1,2]) for k in range(10)]

updatemenus = [dict(type='buttons',
                    buttons=[dict(label='Play',
                                  method='animate',
                                  args=[[f'{k}' for k in range(10)], 
                                         dict(frame=dict(duration=500, redraw=False), 
                                              transition=dict(duration=0),
                                              easing='linear',
                                              fromcurrent=True,
                                              mode='immediate'
                                                                 )]),
                             dict(label='Pause',
                                  method='animate',
                                  args=[None,
                                        dict(frame=dict(duration=500, redraw=False), 
                                             transition=dict(duration=0),
                                             easing='linear',
                                             fromcurrent=True,
                                             mode='immediate' )])],
                    direction= 'left', 
                    pad=dict(r= 10, t=85), 
                    showactive =True, x= 0.1, y= 0, xanchor= 'right', yanchor= 'top')
            ]

sliders = [{'yanchor': 'top',
            'xanchor': 'left', 
            'currentvalue': {'font': {'size': 16}, 'prefix': 'Frame: ', 'visible': True, 'xanchor': 'right'},
            'transition': {'duration': 500.0, 'easing': 'linear'},
            'pad': {'b': 10, 't': 50}, 
            'len': 0.9, 'x': 0.1, 'y': 0, 
            'steps': [{'args': [[k], {'frame': {'duration': 500.0, 'easing': 'linear', 'redraw': False},
                                      'transition': {'duration': 0, 'easing': 'linear'}}], 
                       'label': k, 'method': 'animate'} for k in range(10)       
                    ]}]

fig.update(frames=frames),
fig['layout'].update(updatemenus=updatemenus,
          sliders=sliders)


# plotly.plotly.plot(fig, filename = 'example7.html', auto_open=True)
plotly.offline.plot(fig, filename= 'example7.html')
