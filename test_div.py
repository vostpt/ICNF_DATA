# -*- coding: utf-8 -*-

# Cards Dashboard

# Import Libraries 

import time
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import dash
from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc


# Define APP

app = dash.Dash(
    external_stylesheets=[dbc.themes.CYBORG],
    #suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)



x = ["A","B","C"]
y = [10,20,30]

fig_main = px.bar(x=x,y=y)
fig_main.update_layout(template='plotly_dark')
fig_pie = px.pie(names=x,values=y,hole=0.7,template='plotly_dark')
fig_line = px.line(x=x,y=y,template='plotly_dark')


# ---------------------- DESIGN MAIN --------------------------
row = html.Div(
    [
        dbc.Row(
            [
            	dbc.Col(
            		[
	                    html.H1("AMAZING TITLE GOES HERE",style={"color":"white"}),
	                    dcc.Graph(figure=fig_main,style={"height": "90%"}),
	                    html.Div(dcc.Graph(figure=fig_line,style={"height":"40%"}),style={"height":"60%","background-color":"orange"})

                    ],
                    width=8,
                    style={"height": "100%", "background-color": "#11111"},
                ),
                dbc.Col(
                	dbc.Row(
                		[
	                		dbc.Col(

			                    html.H1("TOP H1",style={"color":"white"}),
			                    width=12,
			                    style={"height": "100%", "background-color": "#FF7634"},
			                ),
			                dbc.Col(
			                	children=[
			                    html.H4("AMAZING DONUT",style={"color":"white"}),
			                    dcc.Graph(figure=fig_pie), 
			                    ],
			                    width=12,
			                    style={"height": "40%", "background-color": "#11111"},

			                ),
			                dbc.Col(
			                	children=[
			                    html.H4("AMAZING LINE",style={"color":"white","height":"40%"}),
			                    dcc.Graph(figure=fig_line,style={"height":"20%"}), 
			                    ],
			                    width=6,
			                    style={"height": "100%", "background-color": "#11111"}
			                ),
			                dbc.Col(
			                	children=[
			                    html.H4("AMAZING BARS",style={"color":"white","height":"40%"}),
			                    dcc.Graph(figure=fig_main,style={"height":"20%"}), 
			                    ],
			                    width=6,
			                    style={"height": "100%", "background-color": "#11111"}
			                ),
			               
                		],
                	)
                ),
                dbc.Col(
                    html.H1("INFORMATION PANEL",style={"color":"white"}),
                    width=12,
                    style={"height": "15%", "background-color": "#111111"},
                ),
            ],
            className="h-75",
            align="left"
        )
            ],
    style={"height": "100vh","background-color":"#111111"},
)


# -------------------------- APP LAYOUT ------------------------
app.layout = dbc.Container(
  	[
		dbc.Row(row),
		
	],
)


# --------------------- RUN APP --------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)

