import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
import cufflinks as cf

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
server = app.server

df_glri = pd.read_csv('glri.csv')
df_glri['GLRI Amount'] = df_glri['GLRI Amount'].str.strip()
df_glri['Funding'] = df_glri['GLRI Amount'].str.strip().str.strip('$').str.replace(",","").astype(int)

YEARS = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

app.title = 'GLRI Federal Funding 2010-2019'
app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.Img(id="logo", src=app.get_asset_url("glri.png")),
                html.H4(children="Great Lakes Restoration Initiative: US Federal Funding for Great Lakes Projects"),
                html.P(
                    id="description",
                    children="Explore the projects of the Great Lakes Restoration Initiative from 2010-2019 by location, focus areas, and funding agencies",
                ),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="slider-container",
                            children=[
                                html.P(
                                    id="slider-text",
                                    children="Use the slider to filter the data by funding year:",
                                ),
                                dcc.Slider(
                                    id="years-slider",
                                    min=min(YEARS),
                                    max=max(YEARS),
                                    value=min(YEARS),
                                    marks={
                                        str(year): {
                                            "label": str(year),
                                            "style": {"color": "#7fafdf"},
                                        }
                                        for year in YEARS
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="map-container",
                            children=[
                                html.P(
                                    "Projects funded under the Great Lakes Restoration Initative in {0}".format(
                                        min(YEARS)
                                    ),
                                    id="map-title",
                                ),
                                dcc.Graph(
                                    id="project-map",
                                    figure=dict(
                                        data=[
                                            dict(
                                                lat=df_glri['Latitude'],
                                                lon=df_glri["Longitude"],
                                                text=df_glri['Funder']+' '+df_glri['Project Type']+': '+df_glri['GLRI Amount']+'<br>'+df_glri["Project Title"],
                                                type="scattermapbox",
                                            )
                                        ],
                                        layout=dict(
                                            mapbox=dict(
                                                layers=[],
                                                accesstoken=mapbox_access_token,
                                                style=mapbox_style,
                                                center=dict(
                                                    lat=43.736238, lon=-84.660662
                                                ),
                                                pitch=0,
                                                zoom=4.5,
                                            ),
                                            autosize=True,
                                        ),
                                    ),
                                ),
                                html.P("To filter the data to a specific region, click and draw on the map. To clear your selection, double-click the map.", id="description2"),
                                html.P("Not all coordinates reflect the location of work. Some reflect approximations, while others represent research centers where funding was allocated. Still others may represent data entry errors. If you would like to suggest a correction, please contact the GLRI at www.glri.us. This is not an official presentation of the Great Lakes Restoration Initiative or the US Government.", id="description3"),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    id="graph-container",
                    children=[
                        html.P(id="chart-selector", children="Select a GLRI topic area:"),
                        dcc.Dropdown(
                            options=[
                                {
                                    "label": "All Focus Areas",
                                    "value": "",
                                },
                                {
                                    "label": "Toxic Substances and Areas of Concern",
                                    "value": "1 - Toxic Substances and Areas of Concern",
                                },
                                {
                                    "label": "Invasive Species",
                                    "value": "2 - Invasive Species",
                                },
                                {
                                    "label": "Nonpoint Source Pollution Impacts on Nearshore Health",
                                    "value": "3 - Nonpoint Source Pollution Impacts on Nearshore Health",
                                },
                                {
                                    "label": "Habitats and Species",
                                    "value": "4 - Habitats and Species",
                                },
                                {
                                    "label": "Foundations for Future Restoration Actions",
                                    "value": "5 - Foundations for Future Restoration Actions",
                                },
                                {
                                    "label": "Multiple Focus Areas",
                                    "value": "6 - Multiple Focus Areas",
                                },

                            ],
                            value="",
                            id="chart-dropdown",
                        ),
                        html.P(id="chart-selector2", children="Select a federal funding agency:"),
                        dcc.Dropdown(
                            options=[
                                {
                                    "label": "All Agencies",
                                    "value": "",
                                },
                                {
                                    "label": "Animal and Plant Health Inspection Service",
                                    "value": "APHIS",
                                },
                                {
                                    "label": "Agency for Toxic Substances and Disease Registry",
                                    "value": "ATSDR",
                                },
                                {
                                    "label": "Bureau of Indian Affairs",
                                    "value": "BIA",
                                },
                                {
                                    "label": "Centers for Disease Control and Prevention",
                                    "value": "CDC",
                                },
                                {
                                    "label": "Environmental Protection Agency",
                                    "value": "EPA",
                                },
                                {
                                    "label": "Federal Highway Administration",
                                    "value": "FHWA",
                                },
                                {
                                    "label": "United States Forest Service",
                                    "value": "FS",
                                },
                                {
                                    "label": "United States Fish and Wildlife Service",
                                    "value": "FWS",
                                },
                                {
                                    "label": "United States Maritime Administrations",
                                    "value": "MARAD",
                                },
                                {
                                    "label": "National Oceanic and Atmospheric Administration",
                                    "value": "NOAA",
                                },
                                {
                                    "label": "National Parks Service",
                                    "value": "NPS",
                                },
                                {
                                    "label": "Natural Resources Conservation Service",
                                    "value": "NRCS",
                                },
                                {
                                    "label": "United States Army Corps of Engineers",
                                    "value": "USACE",
                                },
                                {
                                    "label": "United States Coast Guard",
                                    "value": "USCG",
                                },
                                {
                                    "label": "United States Geological Survey",
                                    "value": "USGS",
                                },
                            ],
                            value="",
                            id="chart-dropdown2",
                        ),
                        dcc.Graph(
                            id="selected-data",
                            figure=dict(
                                data=[dict(x=0, y=0)],
                                layout=dict(
                                    paper_bgcolor="#F4F4F8",
                                    plot_bgcolor="#F4F4F8",
                                    autofill=True,
                                    margin=dict(t=75, r=50, b=50, l=50),
                                ),
                            ),
                        ),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("project-map", "figure"),
    [Input("years-slider", "value"),
    Input("chart-dropdown", "value"),
    Input("chart-dropdown2", "value")],
    [State("project-map", "figure")],
)
def display_map(year, chart_dropdown, chart_dropdown2, figure):
    dff = df_glri[df_glri['Year'] == year]
    if chart_dropdown == '':
        dff = dff
    elif chart_dropdown != '':
        dff = dff[dff['Focus Area'] == chart_dropdown]
    if chart_dropdown2 == '':
        dff = dff
    elif chart_dropdown2 != '':
        dff = dff[dff['Funder'] == chart_dropdown2]
    data = [
        dict(
            lat=dff["Latitude"],
            lon=dff["Longitude"],
            text=dff['Funder']+' '+dff['Project Type']+': '+dff['GLRI Amount']+'<br>'+dff["Project Title"],
            type="scattermapbox",
            hoverinfo="text",
            marker=dict(size=5, color="#2D89C8", opacity=1),
        )
    ]
    
    if "layout" in figure:
        lat = figure["layout"]["mapbox"]["center"]["lat"]
        lon = figure["layout"]["mapbox"]["center"]["lon"]
        zoom = figure["layout"]["mapbox"]["zoom"]
    else:
        lat = (43.736238,)
        lon = (-84.660662,)
        zoom = 4.5

    layout = dict(
        mapbox=dict(
            layers=[],
            accesstoken=mapbox_access_token,
            style=mapbox_style,
            center=dict(lat=lat, lon=lon),
            zoom=zoom,
        ),
        hovermode="closest",
        margin=dict(r=0, l=0, t=0, b=0),
        dragmode="lasso",
    )

    fig = dict(data=data, layout=layout)
    return fig


@app.callback(Output("map-title", "children"), [Input("years-slider", "value")])
def update_map_title(year):
    return "Federal project funding distributed under the Great Lakes Restoration Initative in {0}".format(
        year
    )

@app.callback(
    Output("selected-data", "figure"),
    [
        Input("project-map", "selectedData"),
        Input("chart-dropdown", "value"),
        Input("chart-dropdown2", "value"),
        Input("years-slider", "value"),
    ],
)
def display_selected_data(selectedData, chart_dropdown, chart_dropdown2, year):
    dff = df_glri[df_glri['Year'] == year]
    if chart_dropdown == '':
        dff = df_glri
    elif chart_dropdown != '':
        dff = dff[dff['Focus Area'] == chart_dropdown]
    if chart_dropdown2 == '':
        dff = dff
    elif chart_dropdown2 != '':
        dff = dff[dff['Funder'] == chart_dropdown2]
    
    if selectedData is None:
        dff = dff[dff['Year'] <= year]
        dff = dff[['Year', 'Funding']]
        dff = dff.groupby('Year')['Funding'].agg('sum').reset_index()
        fig = dff.iplot(
            kind="bar", x='Year', y='Funding', title="Project Funding through "+str(year), asFigure=True
        )
        fig_layout = fig["layout"]
        fig_data = fig["data"]
        fig_data[0]["marker"]["color"] = "#1f5e8a"
        fig_data[0]["marker"]["opacity"] = 1
        fig_data[0]["marker"]["line"]['color'] = "#1f5e8a"
        fig_data[0]["textposition"] = "outside"
        fig_layout["paper_bgcolor"] = "#1f2630"
        fig_layout["plot_bgcolor"] = "#1f2630"
        fig_layout["font"]["color"] = "#2D89C8"
        fig_layout["title"]["font"]["color"] = "#2D89C8"
        fig_layout["xaxis"]["tickfont"]["color"] = "#2D89C8"
        fig_layout["xaxis"]["nticks"] = int(dff['Year'].count())
        fig_layout["yaxis"]["tickfont"]["color"] = "#2D89C8"
        fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
        fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
        fig_layout["margin"]["t"] = 75
        fig_layout["margin"]["r"] = 50
        fig_layout["margin"]["b"] = 50
        fig_layout["margin"]["l"] = 50
        
        return fig
    
    else:
        latlong = []
        for x in selectedData['points'][:]:
            latlong.append(x['lat']+x['lon'])
        dff = dff[dff['Year'] == year]
        dff['LatLong'] = dff['Latitude']+dff['Longitude']
        dff = dff[dff['LatLong'].isin(latlong)]
        dff = dff[['Year', 'Funding']]
        dff = dff.groupby('Year')['Funding'].agg('sum').reset_index()
        fig = dff.iplot(
            kind="bar", x='Year', y='Funding', title="Selected Regional Projects By Agency and Topic Area in "+str(year), asFigure=True
        )
        fig_layout = fig["layout"]
        fig_data = fig["data"]
        fig_data[0]["marker"]["color"] = "#1f5e8a"
        fig_data[0]["marker"]["opacity"] = 1
        fig_data[0]["marker"]["line"]['color'] = "#1f5e8a"
        fig_data[0]["textposition"] = "outside"
        fig_layout["paper_bgcolor"] = "#1f2630"
        fig_layout["plot_bgcolor"] = "#1f2630"
        fig_layout["font"]["color"] = "#2D89C8"
        fig_layout["title"]["font"]["color"] = "#2D89C8"
        fig_layout["xaxis"]["tickfont"]["color"] = "#2D89C8"
        fig_layout["xaxis"]["nticks"] = int(dff['Year'].count())
        fig_layout["yaxis"]["tickfont"]["color"] = "#2D89C8"
        fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
        fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
        fig_layout["margin"]["t"] = 75
        fig_layout["margin"]["r"] = 50
        fig_layout["margin"]["b"] = 50
        fig_layout["margin"]["l"] = 50
        
        return fig


if __name__ == "__main__":
    app.run_server(debug=True)