import plotly.plotly as py
import plotly.graph_objs as go

trace1 = {"x": [72, 67, 73, 80, 76, 79, 84, 78, 86, 93, 94, 90, 92, 96, 94, 112], 
          "y": ["Brown", "NYU", "Notre Dame", "Cornell", "Tufts", "Yale",
                "Dartmouth", "Chicago", "Columbia", "Duke", "Georgetown",
                "Princeton", "U.Penn", "Stanford", "MIT", "Harvard"], 
          "marker": {"color": "pink", "size": 12}, 
          "mode": "markers", 
          "name": "Women", 
          "type": "scatter"
}

trace2 = {"x": [92, 94, 100, 107, 112, 114, 114, 118, 119, 124, 131, 137, 141, 151, 152, 165], 
          "y": ["Brown", "NYU", "Notre Dame", "Cornell", "Tufts", "Yale",
                "Dartmouth", "Chicago", "Columbia", "Duke", "Georgetown",
                "Princeton", "U.Penn", "Stanford", "MIT", "Harvard"], 
          "marker": {"color": "blue", "size": 12}, 
          "mode": "markers", 
          "name": "Men", 
          "type": "scatter", 
}

data = [trace1, trace2]
layout = {"title": "Gender Earnings Disparity", 
          "xaxis": {"title": "Annual Salary (in thousands)", }, 
          "yaxis": {"title": "School"}}

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='basic_dot-plot')