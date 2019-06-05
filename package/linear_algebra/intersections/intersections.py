import plotly.plotly as py
import plotly.graph_objs as go
import plotly

trace1 = go.Scatter(x=[1, 2, 3], y=[4, 5, 6], marker={'color': 'red', 'symbol': 104, 'size': 10},
                    mode="markers+lines", text=["one", "two", "three"], name='1st Trace')

data = go.Data([trace1])
layout = go.Layout(title="First Plot", xaxis={'title': 'x1'}, yaxis={'title': 'x2'})
figure = go.Figure(data=data, layout=layout)
plotly.offline.plot(figure, filename='plot.html')

class Intersect:

    def intersection(
            self,
            normal_vector1,
            k1,
            normal_vector2,
            k2
    ): pass
        # Ax + Bx = k
        # normal_vector is [A, B]
        #
