import pandas as pd
import dash
import numpy as np
import plotly.express as px
# from jupyter_dash import JupyterDash
from dash import dcc, html, Input, Output, Dash

import dash_bootstrap_components as dbc  # new import

# uni = pd.read_csv("20230401 - Masi University Main Sheet.csv")
# tl = pd.read_csv("2023 Top Learner  High School - Main -20230120 - NMB High Schools.csv")
children_all = pd.read_csv("Results By Year/20230830.csv").assign(
    full_sessions = lambda x: x["Total Sessions"] > 30
)

# children_all = pd.read_csv("20230712 - Children Results - English.csv")
children = children_all[children_all['Jan - Listen First Sound'].notna() & children_all['June - Listen First Sound'].notna()].copy()

exclude_schools = ['Zukisa', 'Khanyisa', 'Mzingisi', 'Phakamile']
children = children[~children['School'].isin(exclude_schools)].copy()

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
children["Jan - Sounds Total"] =  children["Jan - Listen First Sound"] + children["Jan - Listen Word"]
children["June - Sounds Total"] =  children["June - Listen First Sound"] + children["June - Listen Word"]
children["June - Sounds Total Improvement"] = children["June - Sounds Total"] - children["Jan - Sounds Total"]
children["June - Blends Improvement"] = children["June - Blends"] - children["Jan - Blends"]
children["June - Read Sentences Improvement"] = children["June - Read Sentences"] - children["Jan - Read Sentences"]
children["June - Read Story Improvement"] = children["June - Read Story"] - children["Jan - Read Story"]
children["June - Sight Words Improvement"] = children["June - Sight Words"] - children["Jan - Sight Words"]
children["June - Write Sentence Improvement"] = children["June - Write Sentences"] - children["Jan - Write Sentences"]
children["June - Write CVCs Improvement"] = children["June - Write CVCs"] - children["Jan - Write CVCs"]
children["June - Total Improvement"] = children["June - Total"] - children["Jan - Total"]
# Sounds and Phonics Total is 49
children["Jan - Sounds and Phonics"] = children["Jan - Listen First Sound"] + children["Jan - Listen Word"] + children['Jan - Phonics']
# Reading total is 128
children["Jan - Reading"] = children["Jan - Blends"] + children["Jan - Sight Words"] + children['Jan - Read Sentences'] + children["Jan - Read Story"] + children["Jan - Story Comprehension"]
# Writing total is 87
children["Jan - Writing"] = children['Jan - Written Letters'] + children["Jan - Write CVCs"] + children["Jan - Write Sentences"]
# Sounds and Phonics Total is 49
children["June - Sounds and Phonics"] = children["June - Listen First Sound"] + children["June - Listen Word"] + children['June - Phonics']
# Reading total is 128
children["June - Reading"] = children["June - Blends"] + children["June - Sight Words"] + children['June - Read Sentences'] + children["June - Read Story"] + children["June - Story Comprehension"]
# Writing total is 87
children["June - Writing"] = children['June - Written Letters'] + children["June - Write CVCs"] + children["June - Write Sentences"]

children["June - Sounds and Phonics Improvement"] = children["June - Sounds and Phonics"] - children["Jan - Sounds and Phonics"]
children["June - Reading Improvement"] = children["June - Reading"] - children["Jan - Reading"]
children["June - Writing Improvement"] = children["June - Writing"] - children["Jan - Writing"]

children['Graduate_Status'] = children['June - Total'].apply(lambda x: 'Graduate' if x > 224 else np.nan)

improvement_columns = ["June - Listen First Sound Improvement","June - Listen Word Improvement", "June - Phonics Improvement","June - Blends Improvement", "June - Sight Words Improvement", "June - Read Sentences Improvement", "June - Read Story Improvement", "June - Written Letters Improvement", "June - Write CVCs Improvement", "June - Write Sentence Improvement", "June - Total Improvement" ]
improvement_columns_detailed = ["Full Name", 'School', 'Grade', 'LC Name',"June - Listen First Sound Improvement","June - Phonics Improvement","June - Sight Words Improvement", "June - Read Story Improvement", "June - Written Letters Improvement", "June - Write Sentence Improvement", "June - Total Improvement" ]
primary = children[children['Grade'] != 'PreR']
primary_on = primary[primary['On The Programme'] == 'Yes']
gbo = primary.groupby('School')
gbo_on = primary_on.groupby('School')

GradeR = children[children['Grade'] == 'Grade R']
GradeR_on = GradeR[GradeR['On The Programme'] == 'Yes']
gboR = GradeR.groupby('School')
gboR_on = GradeR_on.groupby('School')

Grade1 = children[children['Grade'] == 'Grade 1']
Grade1_on = Grade1[Grade1['On The Programme'] == 'Yes']
gbo1 = Grade1.groupby('School')
gbo1_on = Grade1_on.groupby('School')

Grade2 = children[children['Grade'] == 'Grade 2']
Grade2_on = Grade2[Grade2['On The Programme'] == 'Yes']
gbo2 = Grade2.groupby('School')
gbo2_on = Grade2_on.groupby('School')

Grade3 = children[children['Grade'] == 'Grade 3']
Grade3_on = Grade3[Grade3['On The Programme'] == 'Yes']
gbo3 = Grade3.groupby('School')
gbo3_on = Grade3_on.groupby('School')


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  # use Bootstrap theme

app.layout = dbc.Container([  # use dbc.Container for main layout
    dbc.Row([  # Bootstrap row
        dbc.Col([  # Bootstrap column
            html.H2("ECD Improvement Stats"),
            dcc.Dropdown(
                id="stat-ecd",
                options=[
                    {"label": option, "value": option} for option in
                    ["June - Phonics Improvement", "June - Sight Words Improvement", "June - Letters Improvement", "June - Total Improvement"]
                ],
                value="June - Total Improvement"
            ),
            dcc.Graph(id="Graph-ecd")
        ], width=12)  # Column width is 12 out of 12 (full width)
    ]),
    dbc.Row([
        dbc.Col([
            html.H2("Grade R & 1 Improvement Stats"),
            dcc.Dropdown(
                id="stat-primary",
                options=[
                    {"label": option, "value": option} for option in
                    ["June - Phonics Improvement", "June - Sight Words Improvement", "June - Blends Improvement", "June - Write CVCs Improvement", "June - Letters Improvement", "June - Read Sentences Improvement", "June - Total Improvement"]
                ],
                value="June - Total Improvement"
            ),
            dcc.Graph(id="Graph-primary")
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.H2("Grade 2 & 3 Improvement Stats"),
            dcc.Dropdown(
                id="stat-adv",
                options=[
                    {"label": option, "value": option} for option in
                    ["June - Read Sentences Improvement", "June - Read Story Improvement", "June - Write Sentence Improvement", "June - Sight Words Improvement", "June - Blends Improvement", "June - Write CVCs Improvement", "June - Letters Improvement", "June - Total Improvement"]
                ],
                value="June - Total Improvement"
            ),
            dcc.Graph(id="Graph-adv")
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.H2("Session Stats"),
            dcc.Dropdown(
                id="grade",
                options=["PreR", "Grade R", "Grade 1", "Grade 2", "Grade 3"],
                value="PreR"
            ),
            dcc.Graph(id="Graph-Sessions")
        ], width=12)
    ])
], fluid=True)  # fluid makes the container take the full width of the viewport

# ... [rest of your callback functions and app server code] ...



@app.callback(
    Output("Graph-ecd", "figure"),
    Input("stat-ecd", "value")
)
def update_graph_ecd(stat):
    # Figuring out who is on the programme for ECD
    on_programme_ecd = children[(children['On The Programme'] == "Yes") & (children['Grade'] == "PreR")]

    # Calculate the average 'Total Improvement' per 'Schools'
    avg_improvement = on_programme_ecd.groupby('School', as_index=False)[stat].mean()
    avg_improvement = avg_improvement.sort_values(by=stat, ascending=False)

    # Create the bar plot
    fig = px.bar(avg_improvement,
                 x="School",
                 y=f"{stat}",
                 title=f"Average Progress of ECD Children by {stat}",
                 color="School")

    # Set x-axis title
    fig.update_xaxes(title_text="School")

    # Set y-axis title
    fig.update_yaxes(title_text=f"{stat}")

    # Update layout properties
    fig.update_layout(autosize=False, width=900, height=600)
    return fig


@app.callback(
    Output("Graph-primary", "figure"),
    Input("stat-primary", "value")
)
def update_graph_primary(stat):

    on_programme_primary = children[(children['On The Programme'] == "Yes") & (children['Grade'].isin(["Grade R", "Grade 1"]))]

    # Calculate the average 'Total Improvement' per 'Schools'
    avg_improvement = on_programme_primary.groupby('School', as_index=False)[stat].mean()
    avg_improvement = avg_improvement.sort_values(by=stat, ascending=False)

    # Create the bar plot
    fig = px.bar(avg_improvement,
                 x="School",
                 y=f"{stat}",
                 title=f"Average Progress of Grade R & 1 Children by {stat}",
                color="School")

    # Set x-axis title
    fig.update_xaxes(title_text="School")

    # Set y-axis title
    fig.update_yaxes(title_text=f"{stat}")

    # Update layout properties
    fig.update_layout(autosize=False, width=900, height=600)
    return fig

@app.callback(
    Output("Graph-adv", "figure"),
    Input("stat-adv", "value")
)
def update_graph_adv(stat):
    # Figuring out who is on the programme for ECD
    on_programme_primary = children[(children['On The Programme'] == "Yes") & (children['Grade'].isin(["Grade 2", "Grade 3"]))]

    # Calculate the average 'Total Improvement' per 'Schools'
    avg_improvement = on_programme_primary.groupby('School', as_index=False)[stat].mean()
    avg_improvement = avg_improvement.sort_values(by=stat, ascending=False)

    # Create the bar plot
    fig = px.bar(avg_improvement,
                 x="School",
                 y=f"{stat}",
                 title=f"Average Progress of Grade 2 & 3 Children by {stat}",
                color="School")

    # Set x-axis title
    fig.update_xaxes(title_text="School")

    # Set y-axis title
    fig.update_yaxes(title_text=f"{stat}")

    # Update layout properties
    fig.update_layout(autosize=False, width=900, height=600)
    return fig


@app.callback(
    Output("Graph-Sessions", "figure"),
    Input("grade", "value")
)
def sessions(grade):
    # Figuring out who is on the programme for ECD
    on_programme = children[(children['On The Programme'] == "Yes") & (children['Grade'] == f"{grade}")]

    # Calculate the average 'Total Improvement' per 'Schools'
    avg_sessions = on_programme.groupby('School', as_index=False)['Total Sessions'].mean()
    avg_sessions = avg_sessions.sort_values(by="Total Sessions", ascending=False)

    # Create the bar plot
    fig = px.bar(avg_sessions,
                 x="School",
                 y="Total Sessions",
                 title=f"Total Sessions for {grade}",
                 color="School")

    # Set x-axis title
    fig.update_xaxes(title_text="School")

    # Set y-axis title
    fig.update_yaxes(title_text="Total Sessions")

    # Update layout properties
    fig.update_layout(autosize=False, width=900, height=600)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port = 8052)
