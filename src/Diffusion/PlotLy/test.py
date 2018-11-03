# import plotly
# plotly.tools.set_credentials_file(username='harry11733', api_key='LIM7c2UloW7RB8QnaFMR')

import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import time

def J(z, lam, alpha):
    return z+(np.exp(-1j*2*alpha)*lam**2)/z

def circle(C, R):
    t=np.linspace(0,2*np.pi, 200)
    return C+R*np.exp(1j*t)

def deg2radians(deg):
    return deg*np.pi/180

def flowlines(alpha=10, beta=5, V_inf=1, R=1, ratio=1.2):
    #alpha, beta are given in degrees
    #ratio =R/lam
    alpha=deg2radians(alpha)# angle of attack
    beta=deg2radians(beta)# -beta is the argument of the complex no (Joukowski parameter - circle center)
    if ratio<=1: #R/lam must be >1
        raise ValueError('R/lambda must be >1')
    lam=R/ratio#lam is the parameter of the Joukowski transformation
   
    center_c=np.exp(-1j*alpha)*(lam-R*np.exp(-1j*beta))

    Circle=circle(center_c,R)
    Airfoil=J(Circle, lam, alpha)
    X=np.arange(-3,3, 0.1)
    Y=np.arange(-3,3, 0.1)

    x,y=np.meshgrid(X,Y)
    z=x+1j*y
    z=ma.masked_where(np.absolute(z-center_c)<=R, z)
    w=J(z, lam, alpha)
    beta=beta+alpha
    Z=z-center_c

    Gamma=-4*np.pi*V_inf*R*np.sin(beta)#circulation
    U=np.zeros(Z.shape, dtype=np.complex)
    with np.errstate(divide='ignore'):#
        for m in range(Z.shape[0]):
            for n in range(Z.shape[1]):# due to this numpy bug https://github.com/numpy/numpy/issues/8516
                                       #we evaluate  this term of the flow elementwise
                U[m,n]=Gamma*np.log((Z[m,n])/R)/(2*np.pi)
    c_flow=V_inf*Z + (V_inf*R**2)/Z - 1j*U #the complex flow 
   
    
    return w, c_flow.imag, Airfoil

def get_contours(mplcont):
    conts=mplcont.allsegs  #  get the segments of line computed via plt.contour
    xline=[]
    yline=[]

    for  cont in conts:
        if len(cont)!=0:
            for arr in cont: 
                
                xline+=arr[:,0].tolist()
                yline+=arr[:,1].tolist()
                xline.append(None) 
                yline.append(None)

    return xline, yline

import plotly.plotly as py
from plotly.grid_objs import Grid, Column

# py.sign_in('harry11733', 'api_key')

levels=np.arange(-3, 3.7, 0.25).tolist()
plt.figure(figsize=(0.05,0.05))
plt.axis('off')
Alpha = list(range(0,19))+list(range(17,-19, -1))+list(range(-17, 1))

my_columns=[]
for k, alpha in enumerate(Alpha):
    Jz, stream_func, Airfoil=flowlines(alpha=alpha)
    #Define an instance of the mpl class contour
    cp= plt.contour(Jz.real, Jz.imag, stream_func, levels=levels, colors='blue')
   
    xline, yline=get_contours(cp)
    # append contour lines to my_columns to be uploaded to Plotly cloud
    my_columns+=[Column(xline, 'x{}'.format(2*k+1)), Column(yline, 'y{}'.format(2*k+1))]
    my_columns+=[Column(Airfoil.real, 'x{}'.format(2*k+2)), Column(Airfoil.imag, 'y{}'.format(2*k+2))]
grid = Grid(my_columns)
py.grid_ops.upload(grid, 'rot-airfoilstrems+str(time.time())', auto_open=False)

frames=[]
for k, alpha in enumerate(Alpha):
    frames.append( dict( data=[dict(xsrc=grid.get_column_reference('x{}'.format(2*k+1)), 
                                    ysrc= grid.get_column_reference('y{}'.format(2*k+1))),
                               dict(xsrc=grid.get_column_reference('x{}'.format(2*k+2)), 
                                    ysrc= grid.get_column_reference('y{}'.format(2*k+2))),
                               ],
                         traces=[0,1],
                         name='frame{}'.format(k)   
                        ) )

data=[dict(type='scatter', 
           xsrc=grid.get_column_reference('x1'), 
           ysrc= grid.get_column_reference('y1'),
           mode='lines',
           line=dict(color='blue', width=1),
           name=''
          ),
      dict(type='scatter', 
           xsrc=grid.get_column_reference('x2'), 
           ysrc= grid.get_column_reference('y2'),
           mode='lines',
           line=dict(color='blue', width=2),
           name=''
          )
      ]

def get_sliders(Alpha, n_frames, fr_duration=100, x_pos=0.0, y_pos=0, slider_len=1.0):
    # n_frames= number of frames
    #fr_duration=duration in milliseconds of each frame
    #x_pos x-coordinate where the slider starts
    #slider_len is a number in (0,1] giving the slider length as a fraction of x-axis length 
    return [dict(steps= [dict(method= 'animate',#Sets the Plotly method to be called when the
                                                #slider value is changed.
                              args= [ [ 'frame{}'.format(k) ],#Sets the arguments values to be passed to 
                                                              #the Plotly method set in method on slide
                                      dict(mode= 'immediate',
                                           frame= dict( duration=fr_duration, redraw= False ),
                                           transition=dict( duration= 0)
                                          )
                                    ],
                              label=str(alpha)
                             ) for k, alpha in enumerate(Alpha)], 
                transition= dict(duration= 0 ),
                x=x_pos,
                y=y_pos, 
                currentvalue=dict(font=dict(size=12), 
                                  prefix="Angle of attack: ", 
                                  visible=True, 
                                  xanchor= "center"
                                 ),  
                len=slider_len)
           ]
    
axis=dict(showline=True, zeroline=False, ticklen=4, mirror=True, showgrid=False)


layout=dict(title="Streamlines of a flow past a rotating Joukowski airfoil",
            font=dict(family='Balto'),
            showlegend=False, 
            autosize=False, 
            width=600, 
            height=600, 
            xaxis=dict(axis, **{'range': [ma.min(Jz.real), ma.max(Jz.real)]}),
            yaxis=dict(axis, **{'range':[ma.min(Jz.imag), ma.max(Jz.imag)]}),
            
            plot_bgcolor='#c1e3ff',
            hovermode='closest',
            
            updatemenus=[dict(type='buttons', showactive=False,
                                y=1,
                                x=1.15,
                                xanchor='right',
                                yanchor='top',
                                pad=dict(t=0, l=10),
                                buttons=[dict(
                                label='Play',
                                method='animate',
                                args=[None, dict(frame=dict(duration=50, redraw=False), 
                                                 transition=dict(duration=0),
                                                 fromcurrent=True,
                                                 mode='immediate'
                                                )
                                     ]
                                             )
                                        ]
                               )
                          ]   

           )

layout.update(sliders=get_sliders(Alpha, len(frames), fr_duration=50))
fig=dict(data=data,layout=layout, frames=frames)

py.icreate_animations(fig, filename='streamlJouk'+str(time.time()))



