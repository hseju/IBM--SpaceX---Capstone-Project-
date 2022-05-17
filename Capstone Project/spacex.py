from ast import Div
from dash import dash, dcc, html, Input, Output
import plotly.express as px

import pandas as pd

#df = pd.read_csv(r'C:\Everything On This PC\Udacity\IBM Data Science Specialization\Capstone Project/spacex_launch_dash.csv')



# Read the spacex data into pandas dataframe
spacex_df = pd.read_csv(r'C:\Everything On This PC\Udacity\IBM Data Science Specialization\Capstone Project/spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)




# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40,'font-family':'Monospace'
                                               }),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites

                                html.Hr(),

                                html.P('Welcome to SpaceX launch Dashboard. Here you can visualize and find insightful results about launches carried about by SpaceX falcon 9 Rocket.',style={'color': '#000000',
                                               'font-size': 15,'font-family':'verdana'}),
                                html.P('This project is a part of IBM Data Science Specializaton certification.',style={'color': '#000000',
                                               'font-size': 15,'font-family':'verdana'}),
                                html.Br(),

                                html.P('Select the launch site from the dropdown menu:'),
                                
                            
                                #adding dropdown menu
                                dcc.Dropdown(id='site-dropdown',options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                ],
                                value='ALL',
                                placeholder="Select a Launch Site here",
                                searchable=True),

                                html.P('Note: 0 indicates Launch Failure and 1 indicates Launch Success'),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',2500: '2500',5000: '5000',7500: '7500',10000: '10000'},
                                                value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                
                                
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),

                                html.Footer([
                                            
                                            html.Div([
                                                html.P('Copyright @hseju',id='footer' ),
                                                
                                            ])

                                ])

                            ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    
    if entered_site == 'ALL':
        fig = px.pie(spacex_df,names='Launch Site', values='class', 
        title='Total Success launches by site')
        fig.update_layout(transition = {'duration': 1000},paper_bgcolor="#e3d6e8")
        return fig
    else:
        fig = px.pie(filtered_df, 
        names='class', 
        title='Total Success launches for site '+entered_site)
        fig.update_layout(transition = {'duration': 1000},paper_bgcolor="#e3d6e8")
        return fig
    


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output('success-payload-scatter-chart','figure'),
              [Input('site-dropdown','value'),
              Input('payload-slider','value')])
def get_scatter_chart(entered_site, number):
    
    payload_df = spacex_df[spacex_df['Payload Mass (kg)'].between(number[0], number[1])]
    if entered_site == 'ALL':
        
        fig = px.scatter(payload_df, x="Payload Mass (kg)", y="class",color="Booster Version Category", title="Payload Mass vs Launch Success/Failure")
        fig.update_layout(transition = {'duration': 1000},paper_bgcolor="#e3d6e8")
        
        return fig
    else:
        filtered_df = payload_df[payload_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",color="Booster Version Category", title="Payload Mass vs Launch Success/Failure")
        fig.update_layout(transition = {'duration': 1000},paper_bgcolor="#e3d6e8")
        
        return fig
    

# Run the app
if __name__ == '__main__':
    app.run_server()
