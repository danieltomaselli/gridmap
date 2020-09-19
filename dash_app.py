import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_leaflet as dl
import dash_leaflet.express as dlx
import pandas as pd
import numpy as np

from dash.dependencies import Output, Input

minmax = get_minmax(default_state)
# Create geojson.
geojson = dl.GeoJSON(data=get_data(default_state), id="geojson", format="geobuf",
                     zoomToBounds=True,  # when true, zooms to bounds when data changes
                     cluster=True,  # when true, data are clustered
                     clusterToLayer=dlx.scatter.cluster_to_layer,  # how to draw clusters
                     zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. cluster) on click
                     options=dict(pointToLayer=dlx.scatter.point_to_layer),  # how to draw points
                     superClusterOptions=dict(radius=150),  # adjust cluster size
                     hideout=dict(colorscale=csc_map[default_csc], color_prop=color_prop, **minmax))
# Create a colorbar.
colorbar = dl.Colorbar(colorscale=csc_map[default_csc], id="colorbar", width=20, height=150, **minmax)
# Create the app.
chroma = "https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"
app = dash.Dash(external_scripts=[chroma], prevent_initial_callbacks=True)
app.layout = html.Div([
    dl.Map([dl.TileLayer(), geojson, colorbar]), html.Div([dd_state, dd_csc],
             style={"position": "relative", "bottom": "80px", "left": "10px", "z-index": "1000", "width": "200px"})
], style={'width': '100%', 'height': '150vh', 'margin': "auto", "display": "block", "position": "relative"})


if __name__ == '__main__':
    app.run_server(debug=True)
