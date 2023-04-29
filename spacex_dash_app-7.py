# Importing Libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Reading SpaceX Launch Data and putting into Pandas DataFrame
spacex_df = pd.read_csv("spacex_launch_dash.csv")
payload_min = spacex_df['Payload Mass (kg)'].min()
payload_max = spacex_df['Payload Mass (kg)'].max()

# Create Application
app = dash.Dash(__name__)

# Create Layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center','color': '#503D36','font-size': 40}),
                                # TASK 1: Add a Launch Site Drop-down Input Component
                                # The default select value is for ALL site
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                     {'label': 'All Sites', 'value': 'ALL'},
                                                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                     ],
                                             value='ALL',
                                             placeholder="place holder here",
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a callback function to Pie Chart
                                # Using If-Else to display all/select and Classes to display success/fail
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range in kg:"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000,step=1000,
                                                marks={0: '0',
                                                      100: '100'},   
                                                value=[payload_min, payload_max]
                                                ),

                                # TASK 4: Add a callback function to render scatter plot to display relationship between payload vs outcome (class)
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# Callback function to change/specify input variables - Launch Site 
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                    Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='# of success for all launch sites')
        return fig
    else:
# For the case in which an individual launch site is select
        select_df=spacex_df[spacex_df['Launch Site']== entered_site]
        select_df=spacex_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig=px.pie(select_df,values='class count',names='class',title="Total Success Launches for selected")
        return fig

#Callback function to change input variables - Launch Sites & Payload
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
                [Input(component_id='site-dropdown',component_property='value'),
                Input(component_id='payload-slider',component_property='value')])
def scatter_plot(entered_site,payload):
    scatter_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0],payload[1])] 
    if entered_site=='ALL':
        fig=px.scatter(scatter_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Payload mass from all sites')
        return fig
    else:
        fig=px.scatter(scatter_df[scatter_df['Launch Site']==entered_site],x='Payload Mass (kg)',y='class',color='Booster Version Category',title=f"Payload mass for site {entered_site}")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
