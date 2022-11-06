from distutils.log import debug
from dash import Dash, dcc, Input, Output, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

github_root = 'https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/'
github_epidemic = 'epidemic/'
github_mysejahtera = 'mysejahtera/'
github_static = 'static/'
github_vaccination = 'vaccination/'

app = Dash(
    __name__,
    external_stylesheets=[
        'https://cdnjs.cloudflare.com/ajax/libs/meyer-reset/2.0/reset.min.css',
        'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
        'https://fonts.googleapis.com/css2?family=Oswald:wght@200;300;400;500;600;700&display=swap',
    ])

HeaderHtml = html.Div([
    html.Span('COVID-19'),
    html.H2('The latest data on the pandemic in Malaysia'),
    html.P("Building on the Ministry of Health's previous COVIDNOW dashboard, "
        +"this page provides a summarised view of the pandemic in Malaysia, "
        +"allowing you to track its evolution on a daily basis."),
    dcc.Dropdown(
        id='select_age',
        options=[
            {'label': 'Malaysia', 'value': 'Malaysia'},
            {'label': 'Johor', 'value': 'Johor'},
            {'label': 'Kedah', 'value': 'Kedah'},
            {'label': 'Kelantan', 'value': 'Kelantan'},
            {'label': 'Melaka', 'value': 'Melaka'},
            {'label': 'Negeri Sembilan', 'value': 'Negeri Sembilan'},
            {'label': 'Pahang', 'value': 'Pahang'},
            {'label': 'Perak', 'value': 'Perak'},
            {'label': 'Perlis', 'value': 'Perlis'},
            {'label': 'Pulau Pinang', 'value': 'Pulau Pinang'},
            {'label': 'Sabah', 'value': 'Sabah'},
            {'label': 'Sarawak', 'value': 'Sarawak'},
            {'label': 'Selangor', 'value': 'Selangor'},
            {'label': 'Terengganu', 'value': 'Terengganu'},
            {'label': 'W.P. Kuala Lumpur', 'value': 'W.P. Kuala Lumpur'},
            {'label': 'W.P. Labuan', 'value': 'W.P. Labuan'},
            {'label': 'W.P. Putrajaya', 'value': 'W.P. Putrajaya'},
        ],
        value='Malaysia',
    ),
], className='container-header px-4 py-4')

FacilityHtml = html.Div([
    html.Div([
        html.H4('Healthcare facility utilization', className='SectionTitle'),
        html.Span(id='Facility_DataAs', children=[], className='SectionDate'),
        html.P(id='Facility_State', children=[], className='SectionState'),
    ]),
    html.Div([
        html.Div([
            dcc.Graph(id='Facility_Vent-graph', figure={}, className='Facility-graph'),
            dcc.Graph(id='Facility_ICU-graph', figure={}, className='Facility-graph'),
            dcc.Graph(id='Facility_Beds-graph', figure={}, className='Facility-graph'),
        ], className='FacilityGraph'),
    ]),
], className='px-4 py-4')

PopulationHtml = html.Div([
    html.H1(id='population-title', children=[]),
    dcc.Graph(id='population-graph', figure={})
], className='px-4 py-4')

app.layout = html.Div([
    HeaderHtml,
    FacilityHtml,

    # Soon
    # PopulationHtml
])

@app.callback(
    [
        Output(component_id='Facility_DataAs', component_property='children'),
        Output(component_id='Facility_State', component_property='children'),
        Output(component_id='Facility_Vent-graph', component_property='figure'),
        Output(component_id='Facility_ICU-graph', component_property='figure'),
        Output(component_id='Facility_Beds-graph', component_property='figure'),
    ], 
    [ Input(component_id='select_age', component_property='value') ]
)

def update_population(option):
    if(type(option) == 'str'):
        print('State select: ' +option)

    # Healthcare facility utilisation
    ## Get Hospital bed percentage
    hosp = pd.read_csv(github_root + 'epidemic/hospital.csv')
    hosp = pd.DataFrame( 
        hosp,
        columns = [
            'date',
            'state',
            'beds',
            'beds_covid',
            'beds_noncrit',
            'admitted_pui',
            'admitted_covid',
            'admitted_total',
            'discharged_pui',
            'discharged_covid',
            'discharged_total',
            'hosp_covid',
            'hosp_pui',
            'hosp_noncovid'
        ]
    )
    hosp_date = hosp.tail(1)['date']
    hosp_date = str(hosp_date).split('    ')[1]
    hosp_date = hosp_date.split(' ')[0]
    hosp_date = hosp_date.split('\n')[0]
    hosp_filter = hosp[hosp['date'] == hosp_date]
    
    facility_date = 'Data as of {}'.format(hosp_date)
    state = 'Data for {}'.format(option)
    if(option == 'Malaysia'):
        sum_hosp_covid = sum(hosp_filter['hosp_covid'])
        sum_hosp_noncovid = sum(hosp_filter['hosp_noncovid'])
        sum_hosp_pui = sum(hosp_filter['hosp_pui'])
        sum_beds_noncrit = sum(hosp_filter['beds_noncrit'])

        hosp_bed_percent = ((sum_hosp_covid + sum_hosp_noncovid + sum_hosp_pui) / sum_beds_noncrit) * 100

        labels = ['In Used',' Available']
        values = [hosp_bed_percent, 100-hosp_bed_percent]
        hosp_bed_fig = go.Figure(data=[go.Pie(labels=labels, values=values, title='Hospital Beds', hole=0.8, marker_colors=['green', 'lightgrey'])])
    else:
        hosp_state = hosp_filter[hosp_filter['state'] == option]

        sum_hosp_covid = sum(hosp_state['hosp_covid'])
        sum_hosp_noncovid = sum(hosp_state['hosp_noncovid'])
        sum_hosp_pui = sum(hosp_state['hosp_pui'])
        sum_beds_noncrit = sum(hosp_state['beds_noncrit'])

        hosp_bed_percent = ((sum_hosp_covid + sum_hosp_noncovid + sum_hosp_pui) / sum_beds_noncrit) * 100
        
        labels = ['In Used',' Available']
        values = [hosp_bed_percent, 100-hosp_bed_percent]
        hosp_bed_fig = go.Figure(data=[go.Pie(labels=labels, values=values, title='Hospital Beds', hole=0.8, marker_colors=['green', 'lightgrey'])])

    ## End Hospital bed percentage

    ## Get ventilator & percentage
    icu = pd.read_csv(github_root + 'epidemic/icu.csv')
    icu = pd.DataFrame( 
        icu,
        columns = [
            'date',
            'state',
            'beds_icu',
            'beds_icu_rep',
            'beds_icu_total',
            'beds_icu_covid',
            'vent',
            'vent_port',
            'icu_covid',
            'icu_pui',
            'icu_noncovid',
            'vent_covid',
            'vent_pui',
            'vent_noncovid',
            'vent_used',
            'vent_port_used'
        ]
    )
    icu_date = icu.tail(1)['date']
    icu_date = str(icu_date).split('    ')[1]
    icu_date = icu_date.split(' ')[0]
    icu_date = icu_date.split('\n')[0]
    icu_filter = icu[icu['date'] == icu_date]
    
    facility_date = 'Data as of {}'.format(icu_date)
    state = 'Data for {}'.format(option)
    if(option == 'Malaysia'):
        sum_vent_used = sum(icu_filter['vent_used'])
        sum_vent_port_used = sum(icu_filter['vent_port_used'])
        sum_vent = sum(icu_filter['vent'])
        sum_vent_port = sum(icu_filter['vent_port'])
        icu_vent_percent = ((sum_vent_used + sum_vent_port_used) / (sum_vent +sum_vent_port)) * 100
        
        labels = ['In Used',' Available']
        values = [icu_vent_percent, 100-icu_vent_percent]
        ventilator_fig = go.Figure(data=[go.Pie(labels=labels, values=values, title='Ventilator', hole=0.8, marker_colors=['green', 'lightgrey'])])

        sum_icu_covid = sum(icu_filter['icu_covid'])
        sum_icu_pui = sum(icu_filter['icu_pui'])
        sum_icu_noncovid = sum(icu_filter['icu_noncovid'])
        sum_beds_icu_total = sum(icu_filter['beds_icu_total'])
        icu_beds_percent = ((sum_icu_covid + sum_icu_pui + sum_icu_noncovid) / sum_beds_icu_total) * 100
        
        labels = ['In Used',' Available']
        values = [icu_beds_percent, 100-icu_beds_percent]
        icu_beds_fig = go.Figure(data=[go.Pie(labels=labels, values=values, title='ICU Beds', hole=0.8, marker_colors=['green', 'lightgrey'])])
    else:
        icu_state = icu_filter[icu_filter['state'] == option]

        sum_vent_used = sum(icu_state['vent_used'])
        sum_vent_port_used = sum(icu_state['vent_port_used'])
        sum_vent = sum(icu_state['vent'])
        sum_vent_port = sum(icu_state['vent_port'])
        icu_vent_percent = ((sum_vent_used + sum_vent_port_used) / (sum_vent +sum_vent_port)) * 100

        labels = ['In Used',' Available']
        values = [icu_vent_percent, 100-icu_vent_percent]
        ventilator_fig = go.Figure(data=[go.Pie(labels=labels, values=values, title='Ventilator', hole=0.8, marker_colors=['green', 'lightgrey'])])
        
        sum_icu_covid = sum(icu_state['icu_covid'])
        sum_icu_pui = sum(icu_state['icu_pui'])
        sum_icu_noncovid = sum(icu_state['icu_noncovid'])
        sum_beds_icu_total = sum(icu_state['beds_icu_total'])
        icu_beds_percent = ((sum_icu_covid + sum_icu_pui + sum_icu_noncovid) / sum_beds_icu_total) * 100
        
        labels = ['In Used',' Available']
        values = [icu_beds_percent, 100-icu_beds_percent]
        icu_beds_fig = go.Figure(data=[go.Pie(labels=labels, values=values, title='ICU Beds', hole=0.8, marker_colors=['green', 'lightgrey'])])

    ## End ventilator & percentage
    # End Healthcare facility utilisation

    return facility_date, state, ventilator_fig, icu_beds_fig, hosp_bed_fig

if __name__ == "__main__":
    app.run_server(debug=True)