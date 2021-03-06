# -*- coding: utf-8 -*-

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


# First Data Treatment 

# Data Treatment 

df_in = pd.read_csv('https://raw.githubusercontent.com/vostpt/ICNF_DATA/main/ICNF_2013_2022_SANKEY.csv') #generated by updater.py 


dummy_year=[2017,2020]
dummy_district = ['Faro','Bragança']


# Cleanup where DISTRITO and CONCELHO have the same value 
df_in["CONCELHO"] = np.where(df_in["DISTRITO"]==df_in["CONCELHO"], df_in["CONCELHO"]+"_concelho", df_in["CONCELHO"])
# Deal with some duplicates names across source and target
df_in["CONCELHO"] = df_in["CONCELHO"].str.capitalize()
# Sort values in dataframe
df_in = df_in.sort_values(["ANO", "DISTRITO","CONCELHO"])


# Use isin function to filter dataframe
# by district from dropdown 
df_filter_district = df_in[df_in['DISTRITO'].isin(dummy_district)].reset_index()
# by year 
df_filter = df_filter_district[df_filter_district['ANO'].isin(dummy_year)].reset_index()


# More Data Treatment 

# Filter by ANO and DISTRITO while summing NCCO. 
# Also renaming columns for readibility 
df = df_in.groupby(["ANO","DISTRITO"], as_index=False)["NCCO"].sum().rename(columns={"ANO":"source","DISTRITO":"target","NCCO":"value"})
# Change ANO type to string 
df["source"] = df["source"].astype(int).astype(str)
# Concatenate previous dataframe with a new dataframe that 
# groups DISTRITO and CONCELHO. 
# This can be done enumerous times to create more steps for the Sankey 
df = pd.concat([df, df_in.groupby(["DISTRITO","CONCELHO"], as_index=False)["NCCO"].sum().rename(columns={"DISTRITO":"source","CONCELHO":"target", "NCCO":"value"})])


# Create Nodes
nodes = np.unique(df[["source","target"]], axis=None)
nodes = pd.Series(index=nodes, data=range(len(nodes)))
# Create Node Colors 
# node_colors = [np.random.choice(colors) for node in nodes]

# define color scale 
colors = px.colors.qualitative.Plotly
# define one random color for every node
node_colors_mappings = dict([(node,np.random.choice(colors)) for node in nodes])
node_colors = [node_colors_mappings[node] for node in nodes]
edge_colors = [node_colors_mappings[node] for node in nodes]

# Plot Graphs 
fig = go.Figure(
    go.Sankey(
        node=dict(
          label = nodes.index,
          line = dict(color = "white", width = 1.0),
          color = node_colors,
          ),
        link={
            "source": nodes.loc[df["source"]],
            "target": nodes.loc[df["target"]],
            "value": df["value"],
        },
    )
)

# Update Layout 
#fig.update_layout(title_text="FOREST FIRES IN PORTUGAL",
#                height = 900,
#                width=1600,
#                font_size=12)

fig.update_layout(plot_bgcolor='black', paper_bgcolor='black',font=dict(size = 10, color = 'white'),)



# START APP -----------------------------------------------------

app = dash.Dash(
    external_stylesheets=[dbc.themes.CYBORG],
    #suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.title = 'VOSTPT - ICNF'

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
                            "borderColor": "#A30000",
                            "opacity": "unset",
                        }
                    ),
                    width={"size": 12},
                ),
                
            ],
            className="g-0",
        ),  # end of first row
        # Second Row
        dbc.Row(
            [  # you have to create a children's array to have more than one column in a row
                dbc.Col(
                    html.H3("FOREST FIRES IN PORTUGAL"),
                    width={"size": 6, "offset": 0},
                ),  # First Column
                dbc.Col(
                    html.H4("Data ICNF", style={"color": "#A30000"}),
                    width={"size": 5, "offset": 0},
                ),  # Second Column
            ],  # Close Children of Second Row
        ),  # End of second row
        # Third Row 
        dbc.Row(
            [
                # Year Dropdown
                dbc.Col(
                    dcc.Dropdown(
                                id="dropdown_year",
                                options=[
                                    {"label": i, "value": i}
                                    for i in df_in.ANO.unique()
                                ],
                                optionHeight=35,  # height/space between dropdown options
                                value=[2013,2022],  # dropdown value selected automatically when page loads
                                disabled=False,  # disable dropdown value selection
                                multi=True,  # allow multiple dropdown values to be selected
                                searchable=True,  # allow user-searching of dropdown values
                                search_value="",  # remembers the value searched in dropdown
                                placeholder="Please select year",  # gray, default text shown when no option is selected
                                clearable=True,  # allow user to removes the selected value
                                style={
                                    "width": "100%"
                                },  # use dictionary to define CSS styles of your dropdown
                                # className='select_box',               #activate separate CSS document in assets folder
                                # persistence=True,                     #remembers dropdown value. Used with persistence_type
                                # persistence_type='memory'             #remembers dropdown value selected until...
                            ), 
                ),
                # District Dropdown
                dbc.Col(
                    dcc.Dropdown(
                                id="dropdown_district",
                                options=[
                                    {"label": i, "value": i}
                                    for i in df_in.DISTRITO.unique()
                                ],
                                optionHeight=35,  # height/space between dropdown options
                                value=['Aveiro','Viseu'],  # dropdown value selected automatically when page loads
                                disabled=False,  # disable dropdown value selection
                                multi=True,  # allow multiple dropdown values to be selected
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




            ],            
        ),
        # Fourth Row
        dbc.Row(
            dbc.Col(dcc.Graph(id="sankey", figure=fig))
            ),
    ],
)  


@app.callback(
    Output(component_id="sankey",component_property="figure"),
    Input(component_id="dropdown_year", component_property="value"),
    Input(component_id="dropdown_district", component_property="value"),
)

def build_graph(dropdown_year, dropdown_district):
    # Data Treatment 

    df_in = pd.read_csv('https://raw.githubusercontent.com/vostpt/ICNF_DATA/main/ICNF_2013_2022_SANKEY.csv') #generated by updater.py 

    # Cleanup where DISTRITO and CONCELHO have the same value 
    df_in["CONCELHO"] = np.where(df_in["DISTRITO"]==df_in["CONCELHO"], df_in["CONCELHO"]+"_concelho", df_in["CONCELHO"])
    # Deal with some duplicates names across source and target
    df_in["CONCELHO"] = df_in["CONCELHO"].str.capitalize()
    # Sort values in dataframe
    df_in = df_in.sort_values(["ANO", "DISTRITO","CONCELHO"])

    # Use isin function to filter dataframe
    # by year from dropdown 
    df_filter_year = df_in[df_in['ANO'].isin(dropdown_year)].reset_index()
    # by district
    df_filter = df_filter_year[df_filter_year['DISTRITO'].isin(dropdown_district)].reset_index()


    # More Data Treatment 

    # Filter by ANO and DISTRITO while summing NCCO. 
    # Also renaming columns for readibility 
    df = df_filter.groupby(["ANO","DISTRITO"], as_index=False)["NCCO"].sum().rename(columns={"ANO":"source","DISTRITO":"target","NCCO":"value"})
    # Change ANO type to string 
    df["source"] = df["source"].astype(int).astype(str)
    # Concatenate previous dataframe with a new dataframe that 
    # groups DISTRITO and CONCELHO. 
    # This can be done enumerous times to create more steps for the Sankey 
    df = pd.concat([df, df_filter.groupby(["DISTRITO","CONCELHO"], as_index=False)["NCCO"].sum().rename(columns={"DISTRITO":"source","CONCELHO":"target", "NCCO":"value"})])


    # Create Nodes
    nodes = np.unique(df[["source","target"]], axis=None)
    nodes = pd.Series(index=nodes, data=range(len(nodes)))


    # define color scale 
    colors = px.colors.sequential.Plasma_r
    # define one random color for every node
    node_colors_mappings = dict([(node,np.random.choice(colors)) for node in nodes])
    node_colors = [node_colors_mappings[node] for node in nodes]
    edge_colors = [node_colors_mappings[node] for node in nodes]

    # Plot Graphs 
    fig = go.Figure(
        go.Sankey(
            node=dict(
              label = nodes.index,
              color =  node_colors,
              ),
            link={
                "source": nodes.loc[df["source"]],
                "target": nodes.loc[df["target"]],
                "value": df["value"],
            },
        )
    )

    # Update Layout 
    fig.update_layout(plot_bgcolor='black', paper_bgcolor='black',font=dict(size = 10, color = 'white'), height=900)
    # Update Orientation 
    # fig.update_traces(orientation="v", selector=dict(type='sankey'))

    return fig 

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)

# END APP 


# END App 