try:
    import plotly
    from plotly.graph_objs import *
    from plotly.offline import download_plotlyjs, iplot
except:
    print('Plotly failed to be loaded')
import numpy as np
import utm

def plot_layout(wtl, fig_size=(1000, 500), data={}, layout={}, **kwargs):
    """Plot the wind turbine layout of a wind farm

    Parameters
    ----------
    wtl: WTLayout
        The wind turbine layout
    fig_size: tuple, optional
        The figure size in pixels
    data: dict, optional
        Additional data inputs
    layout: dict, optional
        Additional layout inputs

    Returns
    -------
    h: Plotly instance
        The instance of the Plot.ly plot
    """
    # Hack to enforce aspect ratio with plot.ly
    # You need to use the ratio of the figure as well as the ratio between the two axis x and y.
    xr = xmin, xmax = wtl.positions[:,0].min(), wtl.positions[:,0].max()
    yr = ymin, ymax = wtl.positions[:,1].min(), wtl.positions[:,1].max()
    fx, fy = fig_size
    aspect_ratio = (fy * (xmax - xmin) + 0.0) / (fx * (ymax - ymin)  + 0.0)
    disp = (1.0 - aspect_ratio)/2.0 # Simple displacement to center the plot
    wt = {
        'type': 'scatter',
        'x': wtl.positions[:,0],
        'y': wtl.positions[:,1],
        'text': ['%s<br>x=%8.1f<br>y=%8.1f'%(name, pos[0], pos[1]) for name, pos in zip(wtl.wt_names, wtl.positions)],
        'mode': 'markers',
        'marker': {
            'symbol': "y-down-open",
            'size': 10,
        },
        'name': 'Wind Turbines'
    }
    wt.update(data)
    mm = {
        'type': 'scatter',
        'x': [m['position'][0] for m in wtl['metmasts']],
        'y': [m['position'][1] for m in wtl['metmasts']],
        'text': ['%s<br>x=%8.1f<br>y=%8.1f'%(m['name'], m['position'][0], m['position'][1]) for m in wtl['metmasts']],
        'mode': 'markers',
        'marker': {
            'color': 'black',
            'symbol':"star-square-open-dot",
            'size': 10,
        },
        'name': 'Met Masts'
    }
    if 'transformers' in wtl.data.keys():
        tp = {
            'type': 'scatter',
            'x': [t['position'][0] for t in wtl['transformers']],
            'y': [t['position'][1] for t in wtl['transformers']],
            'text': ['%s<br>x=%8.1f<br>y=%8.1f'%(t['name'], t['position'][0], t['position'][1]) for t in wtl['transformers']],
            'mode': 'markers',
            'marker': {
                'color': 'green',
                'symbol':"hexagon2-open-dot",
                'size': 14,
            },
            'name': 'Transformer Platforms'
        }
    else:
        tp = {}
    layout.update({
        'autosize': True,
        'width': fx,
        'height': fy,
        'xaxis':{
            'range': xr,
            'type': "linear",
            'autorange': True,
            'domain': [disp, disp + aspect_ratio] # <- note the aspect ratio trick here.
        },
        'yaxis':{
            'range': yr,
            'type': "linear",
            'autorange': True
        },
        'hovermode': 'closest'
    })
    h = iplot(Figure(data=[wt, mm, tp], layout=layout), **kwargs)
    return h


def plot_location(wt_positions, UTM, buffers=(16,8), fig_size=(1000, 500), data={}, layout={}, **kwargs):
    """Plot the wind farm location on a map

    Parameters
    ----------
    wt_positions: np.ndarray of float
        The wind turbine position
    UTM: tuple
        The UTM region number and letter e.g.: UTM=(32, 'U')
    buffers: tuple, optional
        The longitude and latitude buffer region to plot around the wind farm location
    fig_size: tuple, optional
        The figure size in pixels
    data: dict, optional
        Additional data inputs
    layout: dict, optional
        Additional layout inputs

    Returns
    -------
    h: Plotly instance
        The instance of the Plot.ly plot

    """
    lat, lon = np.array([utm.to_latlon(x, y, UTM[0], UTM[1]) for x, y in wt_positions]).T

    data.update({
        'type': 'scattergeo',
        'lon': [lon[0]],
        'lat': [lat[0]],
        'mode': 'markers',
        'marker': {
            'color': 'red',
            'size': 20},
        'geo': 'geo',
    })
    layout.update({
        'geo':{
            'resolution': 50,
            'showland': True,
            'showlakes': True,
            'showsubunits': True,
            'showcountries': True,
            'projection': {
              'type': 'Mercator',
            },
            'lonaxis': {
                'showgrid': True,
                'gridwidth': 0.5,
                'range': [ lon.min() - buffers[0], lon.max() + buffers[0]],
                'dtick': 5
            },
            'lataxis': {
                'showgrid': True,
                'gridwidth': 0.5,
                'range': [ lat.min() - buffers[1], lat.max() + buffers[1]],
                'dtick': 5
            }},
        'width': fig_size[0],
        'height':  fig_size[1],
        'hovermode': 'closest'})
    h = iplot(Figure(data=[data], layout=layout, **kwargs))
    return h
