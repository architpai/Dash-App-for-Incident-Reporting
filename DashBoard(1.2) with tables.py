# Imports
from datetime import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# Linking reference to external stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Global scope declarations and variables:
df = pd.read_excel('updated_data.xlsx')
p_value_style = {
    'text-align': 'center',
    'color : '  # 2a3f5f',
    'font-size': '35px',
    'color': '#2a3f5f',
    'font-size': '35px'
}
indicator_style = {
    'margin-left': '0',
    'border': '1px solid #C8D4E3',
    'border-radius': '3px',
    'background-color': 'white',
    'height': '100px',
    'vertical-align': 'middle',
    'float': 'left',
    'box - sizing': 'border - box',
    'display': 'block',
    'margin': '2.5px'
}
p_text_style = {
    'text-align': 'center',
    'float': 'left',
    'font-size': '15px',
    'width': '100 %',
    'margin - left': '0',
    'display': 'block',
    'margin-block-start': '1em',
    'margin-block-end': '1em',
    'margin-inline-start': '0px',
    'margin-inline-end': '0px',
    'padding': '10px',
    'padding-bottom': '0px',
    'padding-top': '2px',
    }


def generate_fleet_pie_chart(data):
    count_of_fleet = []
    fleet_list = data['Fleet'].values.tolist()
    fleet_list = list(dict.fromkeys(fleet_list))
    fleet_list.sort()
    for fleet in fleet_list:
        temp_count = data[data.Fleet == fleet].shape[0]
        count_of_fleet.append(temp_count)
    return dcc.Graph(id='fleet-pie-chart',
                     figure={
                         'data': [
                             go.Pie(labels=fleet_list, values=count_of_fleet, hoverinfo='percent',
                                    textinfo='label+value',
                                    )],
                         'layout': {
                             'title': 'Distribution of Incidents based on Fleet'
                         }
                     }, style={'width': '100%', 'height': '49%', 'float': 'left', 'display': 'block'})


def generate_priority_pie(data):
    count_of_priority = []
    priority_list = data['Priority_Level'].values.tolist()
    priority_list = list(dict.fromkeys(priority_list))
    priority_list.sort()

    for prior in priority_list:
        temp_count = df[df.Priority_Level == prior].shape[0]
        count_of_priority.append(temp_count)
    for i in range(len(priority_list)):
        priority_list[i] = 'Priority Level {}'.format(priority_list[i])
    return dcc.Graph(id='priority-pie-chart',
                     figure={
                         'data': [
                             go.Pie(labels=priority_list, values=count_of_priority, hoverinfo='percent',
                                    textinfo='label+value')],
                         'layout': {'title': 'Distribution of incidents based on Priority Level'}
                     }, style={'width': '100%', 'height': '49%', 'float': 'right', 'display': 'block'})


# App Initialization
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(id='main-container', children=[
    html.Div(id='header-container', children=[
        html.H1('Incident Report', style={'float': 'Left', 'color': '#EAEAEA'}),
        html.Div(id='Button-div', children=[
            html.Button('Export to pdf', id='export-pdf')
        ], style={'display': 'inline', 'float': 'right', 'margin': '10px'})
    ], style={'padding': '20px', 'background': '#231f20', 'height': '60px', }),
    html.Div([
        html.H1(dt.now().strftime('%B %d, %Y.'), style={'display': 'inline', 'margin': '10px'}),
    ]),
    html.Div(id='meta-data-row', children=[
        html.Div(id='column-indicator1', children=[
            html.P('Total Number of Incidents:', style=p_text_style, id='p_text_1'),
            html.P(style=p_value_style, id='p_value_1')
        ], style=indicator_style),
        html.Div(id='column-indicator2', children=[
            html.P('Total Number Incidents with Priority Level 3:', style=p_text_style, id='p_text_2'),
            html.P(style=p_value_style, id='p_value_2')
        ], style=indicator_style),
        html.Div(id='column-indicator3', children=[
            html.P('Total Number of Injuries:', style=p_text_style, id='p_text_3'),
            html.P(style=p_value_style, id='p_value_3')
        ], style=indicator_style),
        html.Div(id='column-indicator4', children=[
            html.P('Classification with Most Incidents:', style=p_text_style, id='p_text_4'),
            html.P(style=p_value_style, id='p_value_4')
        ], style=indicator_style),
    ]),
    html.Div(id='filters-div', children=[
        html.Div(id='Primary-filter-Div', children=[
            dcc.DatePickerRange(
                id='date-range-picker',
                start_date=dt(2019, 1, 1),
                end_date=dt(2019, 5, 2),
                style={'float': 'left', 'margin': '5px', 'display': 'block'}
            ),
            dcc.Graph(id='issue-time-series', style={'float': 'left', 'display': 'block'}),
            html.Div(id='fleet-checklist', children=[html.H4('Fleet Selection'), dcc.Checklist(
                id='fleet-check',
                options=[
                    {'label': 'Fleet 1', 'value': 'Fleet 1'},
                    {'label': 'Fleet 2', 'value': 'Fleet 2'},
                    {'label': 'Fleet 3', 'value': 'Fleet 3'},
                    {'label': 'Fleet 4', 'value': 'Fleet 4'},
                    {'label': 'Fleet 5', 'value': 'Fleet 5'},
                ],
                value=['Fleet 1', 'Fleet 2', 'Fleet 3', 'Fleet 4', 'Fleet 5'],
                style={}
            )], style={'display': 'block', 'margin-top': '55px', 'margin-left': '50px'}),
            html.Div(id='priority-level-checklist', children=[html.H4('Priority Level Selection'), dcc.Checklist(
                id='priority-check',
                options=[
                    {'label': 'Priority Level 1', 'value': '1'},
                    {'label': 'Priority Level 2', 'value': '2'},
                    {'label': 'Priority Level 3', 'value': '3'},
                ],
                value=['1', '2', '3'],
                style={}
            )], style={'display': 'block', 'margin-bottom': '55px', 'margin-left': '50px'})
        ], style={'width': '49%', 'float': 'left', 'display': 'inline'}),
        html.Div(id='pie-chart-filter-div', children=[
            generate_fleet_pie_chart(df),
            generate_priority_pie(df)
        ], style={'width': '49%', 'float': 'right', 'display': 'inline'}),
    ], style={'display': 'inline'}),
    html.Div(id='Report-body-classification', children=[
        html.H1('Report Based on Classification of Failure'),
        dcc.Graph(id='dist-classification', style={'width': '50%', 'float': 'left'}),
        dcc.Graph(id='classification-equip', style={'width': '50%', 'height': '50%', 'float': 'right'}),
        dcc.Graph(id='classification-subequip', style={'width': '50%', 'height': '50%', 'float': 'right'}),
        html.Div(id='classi-stats', style={'width': '49%', 'float': 'left', 'margin-top': '100px'})
    ], style={'margin-top': '100px'}),
    html.Div(id='Report-body-TypeOfFailure', children=[
        html.H1('Report Based on Type of Failure'),
        dcc.Graph(id='dist-TOF', style={'width': '50%', 'float': 'left'}),
        dcc.Graph(id='TOF-equip', style={'width': '50%', 'height': '50%', 'float': 'right'}),
        html.Div(id='TOF-stats', style={'width': '49%', 'float': 'left', 'display': 'inline', 'height': '270px',
                                        'margin-top': '100px'}),
        dcc.Graph(id='TOF-subequip', style={'width': '50%', 'height': '50%', 'float': 'right', 'display': 'inline'}),

    ], style={'margin-top': '150px'}),
], style={'margin': '5%', 'margin-top': '1%'})  # End of Main Div


@app.callback(Output('issue-time-series', 'figure'),
              [Input('date-range-picker', 'start_date'),
               Input('date-range-picker', 'end_date')])
def update_issue_time_series(start_date, end_date):
    mask = (df['Report_Date'] >= start_date) & (df['Report_Date'] <= end_date)
    data = df.loc[mask]
    issue_count = []
    report_date = []
    dates = data.Report_Date.unique()
    for date in dates:
        ts = pd.to_datetime(str(date))
        d = ts.strftime('%d/%b')
        report_date.append(d)
        issue_count.append(data.loc[data['Report_Date'] == date, 'Issue'].count())
    return {
        'data': [
            go.Bar(
                x=report_date,
                y=issue_count,
                marker={"color": "#ed2939", "opacity": 0.9}
            )
        ],
        'layout': {
            'title': 'Timeline of Reported Incidents'
        }}


@app.callback(Output('fleet-pie-chart', 'figure'),
              [Input('date-range-picker', 'start_date'),
               Input('date-range-picker', 'end_date')])
def update_fleet_pie(start_date, end_date):
    mask = (df['Report_Date'] >= start_date) & (df['Report_Date'] <= end_date)
    data = df.loc[mask]
    count_of_fleet = []
    fleet_list = data['Fleet'].values.tolist()
    fleet_list = list(dict.fromkeys(fleet_list))
    fleet_list.sort()
    for fleet in fleet_list:
        temp_count = data[data.Fleet == fleet].shape[0]
        count_of_fleet.append(temp_count)
    return {
        'data': [
            go.Pie(labels=fleet_list, values=count_of_fleet, hoverinfo='percent',
                   textinfo='label+value',
                   )],
        'layout': {
            'title': 'Distribution of Incidents based on Fleet'
        }
    }


@app.callback(Output('priority-pie-chart', 'figure'),
              [Input('date-range-picker', 'start_date'),
               Input('date-range-picker', 'end_date')])
def update_priority_pie_chart(start_date, end_date):
    mask = (df['Report_Date'] >= start_date) & (df['Report_Date'] <= end_date)
    data = df.loc[mask]
    count_of_priority = []
    priority_list = data['Priority_Level'].values.tolist()
    priority_list = list(dict.fromkeys(priority_list))
    priority_list.sort()
    for prior in priority_list:
        temp_count = data[data.Priority_Level == prior].shape[0]
        count_of_priority.append(temp_count)
    for i in range(len(priority_list)):
        priority_list[i] = 'Priority Level {}'.format(priority_list[i])
    return {
        'data': [
            go.Pie(labels=priority_list, values=count_of_priority, hoverinfo='percent', textinfo='label+value')],
        'layout': {'title': 'Distribution of incidents based on Priority Level'}
    }


@app.callback(Output('dist-classification', 'figure'),
              [Input('date-range-picker', 'start_date'),
               Input('date-range-picker', 'end_date'),
               Input('fleet-check', 'value'),
               Input('priority-check', 'value')])
def update_classification_distribution(start_date, end_date, fleet_select, priority_select):
    mask = (df['Report_Date'] >= start_date) & (df['Report_Date'] <= end_date)
    data = df.loc[mask]
    temp = data[data['Fleet'].isin(fleet_select)]
    data = temp[temp['Priority_Level'].isin(priority_select)]
    classification = data['Classification'].unique()
    count_of_classification = []
    for classi in classification:
        temp_count = data.Issue[data['Classification'] == classi].shape[0]
        count_of_classification.append(temp_count)
    return {
        'data': [
            go.Bar(
                x=classification,
                y=count_of_classification,
                marker={"color": "#ed2939", "opacity": 0.9}
            )
        ],
        'layout': {'title': 'Distribution of Classification of failure'}
    }


@app.callback(Output('dist-TOF', 'figure'),
              [Input('date-range-picker', 'start_date'),
               Input('date-range-picker', 'end_date'),
               Input('fleet-check', 'value'),
               Input('priority-check', 'value')])
def update_tof_distribution(start_date, end_date, fleet_select, priority_select):
    mask = (df['Report_Date'] >= start_date) & (df['Report_Date'] <= end_date)
    data = df.loc[mask]
    temp = data[data['Fleet'].isin(fleet_select)]
    data = temp[temp['Priority_Level'].isin(priority_select)]
    tof = data['Type_of_Failure'].unique()
    count_of_tof = []
    for fail in tof:
        temp_count = data.Issue[data['Type_of_Failure'] == fail].shape[0]
        count_of_tof.append(temp_count)
    return {
        'data': [
            go.Bar(
                x=tof,
                y=count_of_tof,
                marker={"color": "#ed2939", "opacity": 0.9}
            )
        ],
        'layout': {'title': 'Distribution of Type of failure'}
    }


@app.callback(Output('classification-equip', 'figure'),
              [Input('date-range-picker', 'start_date'),
               Input('date-range-picker', 'end_date'),
               Input('fleet-check', 'value'),
               Input('priority-check', 'value'),
               Input('dist-classification', 'clickData')])
def update_classi_equipment(start_date, end_date, fleet_select, priority_select, clickdata):
    mask = (df['Report_Date'] >= start_date) & (df['Report_Date'] <= end_date)
    data = df.loc[mask]
    temp = data[data['Fleet'].isin(fleet_select)]
    data = temp[temp['Priority_Level'].isin(priority_select)]
    if clickdata is None:
        equip_list = data.Equipment_Failed.unique()
        count_of_equip = []
        for equip in equip_list:
            temp_count = data[data['Equipment_Failed'] == equip].shape[0]
            count_of_equip.append(temp_count)
    else:
        criteria = clickdata['points'][0]['x']
        data = data[data['Classification'] == criteria]
        equip_list = data.Equipment_Failed.unique()
        count_of_equip = []
        for equip in equip_list:
            temp_count = data[data['Equipment_Failed'] == equip].shape[0]
            count_of_equip.append(temp_count)
    return {
        'data': [
            go.Bar(
                x=equip_list,
                y=count_of_equip,
                marker={"color": "#ed2939", "opacity": 0.9}
            )
        ],
        'layout': {'title': 'Distribution of Failed Equipment'}
    }


@app.callback(Output('classification-subequip', 'figure'),
              [Input('date-range-picker', 'start_date'),
               Input('date-range-picker', 'end_date'),
               Input('fleet-check', 'value'),
               Input('priority-check', 'value'),
               Input('dist-classification', 'clickData')])
def update_classi_subequipment(start_date, end_date, fleet_select, priority_select, clickdata):
    mask = (df['Report_Date'] >= start_date) & (df['Report_Date'] <= end_date)
    data = df.loc[mask]
    temp = data[data['Fleet'].isin(fleet_select)]
    data = temp[temp['Priority_Level'].isin(priority_select)]
    if clickdata is None:
        subequip_list = data.SubEquipment_Failed.unique()
        index = np.argwhere(subequip_list == 'NA')
        subequip_list = np.delete(subequip_list, index)
        count_of_subequip = []
        for equip in subequip_list:
            temp_count = data[data['SubEquipment_Failed'] == equip].shape[0]
            count_of_subequip.append(temp_count)
    else:
        criteria = clickdata['points'][0]['x']
        data = data[data['Classification'] == criteria]
        subequip_list = data.SubEquipment_Failed.unique()
        index = np.argwhere(subequip_list == 'NA')
        subequip_list = np.delete(subequip_list, index)
        count_of_subequip = []
        for equip in subequip_list:
            temp_count = data[data['SubEquipment_Failed'] == equip].shape[0]
            count_of_subequip.append(temp_count)
    return {
        'data': [
            go.Bar(
                x=subequip_list,
                y=count_of_subequip,
                marker={"color": "#ed2939", "opacity": 0.9}
            )
        ],
        'layout': {'title': 'Distribution of Failed Sub-Equipment'}
    }


@app.callback(Output('TOF-equip', 'figure'),
              [Input('date-range-picker', 'start_date'),
               Input('date-range-picker', 'end_date'),
               Input('fleet-check', 'value'),
               Input('priority-check', 'value'),
               Input('dist-TOF', 'clickData')])
def update_tof_equipment(start_date, end_date, fleet_select, priority_select, clickdata):
    mask = (df['Report_Date'] >= start_date) & (df['Report_Date'] <= end_date)
    data = df.loc[mask]
    temp = data[data['Fleet'].isin(fleet_select)]
    data = temp[temp['Priority_Level'].isin(priority_select)]
    if clickdata is None:
        equip_list = data.Equipment_Failed.unique()
        count_of_equip = []
        for equip in equip_list:
            temp_count = data[data['Equipment_Failed'] == equip].shape[0]
            count_of_equip.append(temp_count)
    else:
        criteria = clickdata['points'][0]['x']
        data = data[data['Type_of_Failure'] == criteria]
        equip_list = data.Equipment_Failed.unique()
        count_of_equip = []
        for equip in equip_list:
            temp_count = data[data['Equipment_Failed'] == equip].shape[0]
            count_of_equip.append(temp_count)
    return {
        'data': [
            go.Bar(
                x=equip_list,
                y=count_of_equip,
                marker={"color": "#ed2939", "opacity": 0.9}
            )
        ],
        'layout': {'title': 'Distribution of Failed Equipment'}
    }


@app.callback(Output('TOF-subequip', 'figure'),
              [Input('date-range-picker', 'start_date'),
               Input('date-range-picker', 'end_date'),
               Input('fleet-check', 'value'),
               Input('priority-check', 'value'),
               Input('dist-TOF', 'clickData')])
def update_tof_subequip(start_date, end_date, fleet_select, priority_select, clickdata):
    mask = (df['Report_Date'] >= start_date) & (df['Report_Date'] <= end_date)
    data = df.loc[mask]
    temp = data[data['Fleet'].isin(fleet_select)]
    data = temp[temp['Priority_Level'].isin(priority_select)]
    if clickdata is None:
        subequip_list = data.SubEquipment_Failed.unique()
        index = np.argwhere(subequip_list == 'NA')
        subequip_list = np.delete(subequip_list, index)
        count_of_subequip = []
        for equip in subequip_list:
            temp_count = data[data['SubEquipment_Failed'] == equip].shape[0]
            count_of_subequip.append(temp_count)
    else:
        criteria = clickdata['points'][0]['x']
        data = data[data['Type_of_Failure'] == criteria]
        subequip_list = data.SubEquipment_Failed.unique()
        index = np.argwhere(subequip_list == 'NA')
        subequip_list = np.delete(subequip_list, index)
        count_of_subequip = []
        for equip in subequip_list:
            temp_count = data[data['SubEquipment_Failed'] == equip].shape[0]
            count_of_subequip.append(temp_count)
    return {
        'data': [
            go.Bar(
                x=subequip_list,
                y=count_of_subequip,
                marker={"color": "#ed2939", "opacity": 0.9}
            )
        ],
        'layout': {'title': 'Distribution of Failed Sub-Equipment'}
    }


@app.callback(Output('classi-stats', 'children'),
              [Input('date-range-picker', 'start_date'),
               Input('date-range-picker', 'end_date'),
               Input('fleet-check', 'value'),
               Input('priority-check', 'value'),
               Input('classification-equip', 'clickData'),
               Input('dist-classification', 'clickData')])
def update_table(start_date, end_date, fleet_select, priority_select, click_data_1, click_data_2):
    mask = (df['Report_Date'] >= start_date) & (df['Report_Date'] <= end_date)
    data = df.loc[mask]
    temp = data[data['Fleet'].isin(fleet_select)]
    data = temp[temp['Priority_Level'].isin(priority_select)]
    df_modified = data.drop(
        ['Sr No.', 'Fleet', 'Vessel_Type', 'Priority_Level', 'Make/Model', 'Expected_Close_Out', 'Description',
         'Type_of_Failure', 'Report_Date'], axis=1)
    if click_data_1 is not None:
        criteria = click_data_1['points'][0]['x']
        df_modified = df_modified[df_modified['Equipment_Failed'] == criteria]
    if click_data_2 is not None:
        classi = click_data_2['points'][0]['x']
        df_modified = df_modified[df_modified['Classification'] == classi]
    return dash_table.DataTable(
        style_data={'whiteSpace': 'normal'},
        style_table={'overflowY': 'scroll', 'width': '620px', 'height': '270px'},
        data=df_modified.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df_modified.columns]
    )


@app.callback(Output('TOF-stats', 'children'),
              [Input('date-range-picker', 'start_date'),
               Input('date-range-picker', 'end_date'),
               Input('fleet-check', 'value'),
               Input('priority-check', 'value'),
               Input('TOF-equip', 'clickData'),
               Input('dist-TOF', 'clickData')])
def update_table(start_date, end_date, fleet_select, priority_select, click_data_1, click_data_2):
    mask = (df['Report_Date'] >= start_date) & (df['Report_Date'] <= end_date)
    data = df.loc[mask]
    temp = data[data['Fleet'].isin(fleet_select)]
    data = temp[temp['Priority_Level'].isin(priority_select)]
    df_modified = data.drop(
        ['Sr No.', 'Fleet', 'Vessel_Type', 'Priority_Level', 'Make/Model', 'Expected_Close_Out', 'Description',
         'Classification', 'Report_Date'], axis=1)
    if click_data_1 is not None:
        criteria = click_data_1['points'][0]['x']
        df_modified = df_modified[df_modified['Equipment_Failed'] == criteria]
    if click_data_2 is not None:
        tof = click_data_2['points'][0]['x']
        df_modified = df_modified[df_modified['Type_of_Failure'] == tof]
    return dash_table.DataTable(
        style_data={'whiteSpace': 'normal'},
        style_table={'overflowY': 'scroll', 'width': '620px', 'height': '270px', 'z-index': '5'},
        data=df_modified.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df_modified.columns]
    )


@app.callback(Output('p_value_1', 'children'),
              [Input('date-range-picker', 'start_date'),
               Input('date-range-picker', 'end_date')])
def update_p(start_date, end_date):
    mask = (df['Report_Date'] >= start_date) & (df['Report_Date'] <= end_date)
    data = df.loc[mask]
    return '{}'.format(data.Issue.count())


@app.callback(Output('p_value_2', 'children'),
              [Input('date-range-picker', 'start_date'),
               Input('date-range-picker', 'end_date')])
def update_p(start_date, end_date):
    mask = (df['Report_Date'] >= start_date) & (df['Report_Date'] <= end_date)
    data = df.loc[mask]
    return '{}'.format(data[data['Priority_Level'] == 3].Issue.count())


@app.callback(Output('p_value_3', 'children'),
              [Input('date-range-picker', 'start_date'),
               Input('date-range-picker', 'end_date')])
def update_p(start_date, end_date):
    mask = (df['Report_Date'] >= start_date) & (df['Report_Date'] <= end_date)
    data = df.loc[mask]
    return '{}'.format(data[data['Classification'] == 'Injury'].Issue.count())


@app.callback(Output('p_value_4', 'children'),
              [Input('date-range-picker', 'start_date'),
               Input('date-range-picker', 'end_date')])
def update_p(start_date, end_date):
    mask = (df['Report_Date'] >= start_date) & (df['Report_Date'] <= end_date)
    data = df.loc[mask]
    return '{}'.format(data.Classification.value_counts().idxmax())


# App Driver
if __name__ == '__main__':
    app.run_server(debug=True)
