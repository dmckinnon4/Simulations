import plotly
import pickle
import numpy as np

plotData=[dict(type='scatter',
      x=list(range(24)),
      y=test_data[:0],
      mode='markers',
      marker=dict(size=10, color='red')
          )
 ]

frames=[dict(data=[dict(y=test_data[:,k])],
         traces=[0],
         name=f'{k+1}',
         layout=dict(yaxis=dict(range=[-1, test_data[:, k].max()+100]))) for k in range(31)]

sliders=[dict(steps= [dict(method= 'animate',
                       args= [[ f'{k+1}'],
                              dict(mode= 'e',
                              frame= dict( duration=1000, redraw= False ),
                                       transition=dict( duration= 0)
                                      )
                                ],
                        label=f' {k+1}'
                         ) for k in range(31)], 
            transition= dict(duration= 30 ),
            x=0,#slider starting position  
            y=0, 
            currentvalue=dict(font=dict(size=12), 
                              prefix='Day: ', 
                              visible=True, 
                              xanchor= 'center'
                             ),  
            len=1.0,
            active=1) #slider length)
            
       ]

axis_style=dict(showline=True,
           mirror=True,
           zeroline=False,
           ticklen=4)

layout=dict(title='Mayıs-Günlük Kullanıcı Sayıları',
        width=900,
        height=600,
        autosize=False,
        xaxis=dict(axis_style, dtick=1, tit='s', title='Zaman (saat)', **dict(range=[0,24])),
        yaxis=dict(axis_style, title='Kullanıcı Sayısı',autorange=False),
        #plot_bgcolor="rgba(66,134,244, 0.2)",
        shapes= [dict(
                    # Sabah
                    type= 'rect',
                    xref= 'x',
                    yref= 'paper',
                    x0= '0',
                    y0= 0,
                    x1= '8',
                    y1= 1,
                    fillcolor= 'rgba(66, 134, 244, 0.5)',
                    opacity= 0.2,
                    line= dict(width= 0)
                ),
                 # Oglen
                dict(
                    type= 'rect',
                    xref= 'x',
                    yref= 'paper',
                    x0= '8',
                    y0= 0,
                    x1= '16',
                    y1= 1,
                    fillcolor= '#rgba(255, 252, 117,1)',
                    opacity= 0.2,
                    line= dict(width=0)
                ),
                  # Aksam
                dict(
                    type= 'rect',
                    xref= 'x',
                    yref= 'paper',
                    x0= '16',
                    y0= 0,
                    x1= '24',
                    y1= 1,
                    fillcolor= 'rgba(2, 0, 168, 1)',
                    opacity= 0.2,
                    line= dict(width=0)
                )
        ],
        hovermode='closest',
        updatemenus=[dict(type='buttons', showactive=True,
                            y=0,
                            x=1.15,
                            xanchor='right',
                            yanchor='top',
                            pad=dict(t=0, r=10),
                            buttons=[dict(label='Play',
                                          method='animate',
                                          args=[None, 
                                                dict(frame=dict(duration=4000, 
                                                                redraw=True),
                                                     transition=dict(duration=4000),
                                                     fromcurrent=True,
                                                     mode='immediadate'
                                                    )
                                               ]
                                         ),
                                     dict(label='Pause',
                                          method='animate',
                                          args=[[None], 
                                                dict(frame=dict(duration=0, 
                                                                redraw=False),
                                                     transition=dict(duration=30),
                                                     fromcurrent=True,
                                                     mode='immediate'
                                                    )
                                               ]
                                         )
                                    ]
                           )
                      ],
          sliders=sliders
       )

# Animated Plot
figure = {
'data': plotData,
'layout': layout,
'frames': frames
}  
fig=dict(data=plotData, frames=frames, layout=layout)
fig['data'][0].update(mode='markers+lines',
                 line=dict(width=1.5, color='blue'))
plot(fig, auto_open=False)