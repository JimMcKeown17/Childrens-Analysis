import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
G3_colour = "#6DA9E4"
G2_colour = "#F7D060"
G1_colour = "#917FB3"
GR_colour = "#98D8AA"
ECD_colour = "#FF6D60"

all_children = pd.read_csv("20230623 - Children Results.csv")
children = all_children[all_children['Jan - Listen First Sound'].notna() & all_children['June - Listen First Sound'].notna()].copy()

# # create new column 'Jan-Jun Assessed' where 'Jan - Total' and 'June - Total' are not blank
# children['Jan-Jun Assessed'] = np.where(children['Jan - Total'].notnull() & children['June - Total'].notnull(), 'Assessed', '')

children['Jan - Total'] = children[['Jan - Listen First Sound', 'Jan - Listen Word','Jan - Phonics', 'Jan - Blends', 'Jan - Sight Words',
                                  'Jan - Read Sentences', 'Jan - Read Story', 'Jan - Story Comprehension',
                                  'Jan - Written Letters', 'Jan - Write Name', 'Jan - Write CVCs',
                                  'Jan - Write Sentences']].sum(axis=1,min_count=1)
children['June - Total'] = children[['June - Listen First Sound',
       'June - Listen Word','June - Phonics', 'June - Blends', 'June - Sight Words',
                                  'June - Read Sentences', 'June - Read Story', 'June - Story Comprehension',
                                  'June - Written Letters', 'June - Write Name', 'June - Write CVCs',
                                  'June - Write Sentences']].sum(axis=1,min_count=1)
children['June - Listen First Sound Improvement'] = children['June - Listen First Sound'] - children['Jan - Listen First Sound']
children['June - Listen Word Improvement'] = children['June - Listen Word'] - children['Jan - Listen Word']
children['June - Phonics Improvement'] = children['June - Phonics'] - children['Jan - Phonics']
children['June - Written Letters Improvement'] = children['June - Written Letters'] - children['Jan - Written Letters']

children['June - Total Improvement'] = children['June - Total'] - children['Jan - Total']
children['June - Level Improvement'] = children['May Level'] - children['March Level']

ecd = children[children['Grade'] == 'PreR']
ecd_on = ecd[ecd['On The Programme'] == 'Yes']
ecd_qualify = ecd[(ecd['On The Programme'] == 'Yes') & (ecd['Total Sessions'] > 10)]
gbo_ecd = ecd.groupby('Schools')
gbo_ecd_on = ecd_on.groupby('Schools')
gbo_ecd_qualify = ecd_qualify.groupby('Schools')
df = ecd.copy()



# Create a Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    dcc.Dropdown(
        id='school-dropdown',
        options=[{'label': i, 'value': i} for i in ecd['Schools'].unique()],
        value='School1'
    ),
    dcc.Graph(id='scatter-plot')
])

# Define callback
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('school-dropdown', 'value')]
)
def update_graph(selected_school):
    filtered_df = ecd[ecd.Schools == selected_school]
    fig = px.scatter(filtered_df, x='Total Sessions', y='June - Total Improvement', color='LC Name')
    return fig

# Run app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
