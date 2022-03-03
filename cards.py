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


# Get data from CSV 

df_in = pd.read_csv('https://raw.githubusercontent.com/vostpt/ICNF_DATA/main/ICNF_2013_2022_full.csv')


# DATA CLEAN UP 

# Deal with some duplicates names across source and target
df_in["CONCELHO"] = df_in["CONCELHO"].str.capitalize()
# Sort values in dataframe
df_in = df_in.sort_values(['ANO','MES','DIA', 'DISTRITO','CONCELHO'])

# --------------------------------------#  START APP #------------------------------------------------------------------------------------------------------------------

app = dash.Dash(
    external_stylesheets=[dbc.themes.CYBORG],
    #suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

# Bring dataframe into the app cycle



df_app = df_in.groupby(['ANO','DISTRITO','NCCO'],as_index=False)['AREATOTAL'].sum()
df_app["DISTRITO"] = df_app["DISTRITO"].str.capitalize()
df_app['ANO']=df_app['ANO'].astype(str)

print(df_app.info())

print("HELLO")

print(df_app.head())


# Create First Variables 

var_burnt_area = round(df_in.AREATOTAL.sum(),2)
var_total_fires = df_in.NCCO.count()
var_distrito = "All"

# Create first graph 

fig = px.bar(df_app, x='ANO', y='AREATOTAL',template='plotly_dark')

# Design Cards 

card_burnt_area = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Total Burnt Area (ha)", className="card-title"),
            html.H2(var_burnt_area,id="card_total_burnt_area"),
        ]
    ), color="danger",
)

card_total_fires = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Total Rural Fires", className="card-title"),
            html.H2(var_total_fires,id="card_total_fires"),
        ],
    ),color="info",
)

card_district = dbc.Card(
    dbc.CardBody(
        [
        	html.H5("District", className="card-title"),
            html.H2(var_distrito,id="card_district_name"),
        ],
    ),color="primary",
)

# Create Cards Layout 

cards = dbc.Row(
    [
        dbc.Col(card_district,width=6),
        dbc.Col(card_total_fires, width=3),
        dbc.Col(card_burnt_area, width=3),
        
    ],className="g-0",
)



# Create App Layout 


app.layout = dbc.Container(
    [
    	# First Row
        dbc.Row(
            [
                dbc.Col(
                    html.Hr(
                        style={
                            "borderWidth": "2vh",
                            "width": "100%",
                            "borderColor": "#FFFFFF",
                            "opacity": "unset",
                        }
                    ),
                    width={"size": 12},
                ),
                
            ],
            className="g-0",
        ),  # end of first row

        cards,
      	dbc.Row(
      		dbc.Col(
                    dcc.Dropdown(
                                id="dropdown_district",
                                options=[
                                    {"label": i, "value": i}
                                    for i in df_app.DISTRITO.unique()]+
                                    [{'label': 'Todos', 'value': 'all_values'}],
                                
                                optionHeight=35,  # height/space between dropdown options
                                value='all_values',  # dropdown value selected automatically when page loads
                                disabled=False,  # disable dropdown value selection
                                multi=False,  # allow multiple dropdown values to be selected
                                searchable=True,  # allow user-searching of dropdown values
                                search_value="",  # remembers the value searched in dropdown
                                placeholder="Please select District",  # gray, default text shown when no option is selected
                                clearable=True,  # allow user to removes the selected value
                                style={
                                    "width": "100%"
                                },  # use dictionary to define CSS styles of your dropdown
                                # className='select_box',               #activate separate CSS document in assets folder
                                # persistence=True,                     #remembers dropdown value. Used with persistence_type
                                # persistence_type='memory'             #remembers dropdown value selected until...
                            ), 
                ),

      	),

        dbc.Row(
            dbc.Col(dcc.Graph(id="graph", figure=fig))
        ),

        
    ], # end container
) # end layout 

# APP CALL BACKS FROM DROPDOWN 

@app.callback(
    Output(component_id="graph",component_property="figure"),
    Input(component_id="dropdown_district", component_property="value"),
)

def build_graph(dropdown_district):
		if dropdown_district == 'all_values':
			dff = df_app
		else:
			dff= df_app[df_app['DISTRITO'].eq(dropdown_district)]

		df_graph = dff
		df_graph['ANO']=df_graph['ANO'].astype(str)
		dff_graph = df_graph.groupby(['ANO','DISTRITO'],as_index=False)['AREATOTAL'].sum()

		fig = px.bar(dff_graph, x=dff_graph['ANO'], y='AREATOTAL',template='plotly_dark',color='ANO')

		return fig

@app.callback(
	Output(component_id="card_total_fires",component_property="children"),
	Output(component_id="card_total_burnt_area",component_property="children"),
	Output(component_id="card_district_name",component_property="children"),
	Input(component_id="dropdown_district", component_property="value"),

)

def cards_vars(dropdown_district):
		if dropdown_district == 'all_values':
				dff = df_app
				
		else:
				dff= df_app[df_app['DISTRITO'].eq(dropdown_district)]
		var_total_fires = dff.NCCO.count()
		var_burnt_area = round(dff.AREATOTAL.sum(),2)

		if dropdown_district == 'all_values':
			var_distrito = "All"
		else:
			var_distrito = dff.DISTRITO.iloc[0]
		return var_total_fires, var_burnt_area,var_distrito






# Load APP 

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)


# APP ENDS HERE 



