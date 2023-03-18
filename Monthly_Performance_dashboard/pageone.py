

import pandas as pd
import numpy as np
import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
from dash.dependencies import Input ,Output
import dash_bootstrap_components as dbc
import plotly_express as px
from plotly.subplots import make_subplots
from dash import dcc, html, callback, Output
from pathlib import Path
#load the data--------------------------------------------------------------------------------------
df=pd.read_excel('data\dataset.xlsx')

#------General Hospital Report ------------------------------------------------------------
#concert the date to datetime format
df['Date']=pd.to_datetime(df['Date'])
#extract the month
df['Month']=df['Date'].dt.month_name()
df['year']=df['Date'].dt.year
#-----------------------------remove the white spaces
df.columns=df.columns.str.replace(" ","")
df=df.rename(columns={'CLINIC':'clinic','DOCTOR':'doctor','REVENUESCATEGORY':'revenue_category','CASH':'cash','CREDIT':'credit',
'TOTALREVENUES':'total_revenues','PATIENTS':'patients'})

app=dash.Dash(external_stylesheets=[dbc.themes.CYBORG],meta_tags=[{'name': 'viewport',
'content': 'width=device-width, initial-scale=1.0'}],suppress_callback_exceptions=True)
server=app.server
app.layout=dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H2('MONTHLY HOSPITAL PERFORMANCE DASHBOARD',className='text-center mb4')
            ,width=12)
    ]),
    dbc.Row(
        html.Marquee("Monthly Hospital Performance Dashboard-Designed by-Mohammed Bahageel-Data Analyst-the Information displayed is stricly confidential"),
        style = {'color':'cyan'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardImg(src='https://media1.giphy.com/media/MgFP7hqxNoDhRCv6Sd/giphy.gif?cid=5e214886366cfe5b9c075895b1569635b4327781c1b7320b&rid=giphy.gif&ct=g',top=True,bottom=False),
                dbc.CardBody([
                    html.H4('Abha Private Hospital',className='card-title'),
                    html.P('Choose The revenue Category:',className='card-text'),
                    dcc.Dropdown(id='selection_op',
                                 multi=False,
                                 options=[{'label':x,'value':x} for x in df['revenue_category'].unique()],
                                 value='CONSULTATION ',
                                 clearable=False ,style={'color': '#000000'})
                ]),
            ])
        ],width=2,xs=12, sm=12, md=12, lg=5, xl=2),
        dbc.Col([
            dcc.Graph(id='revenue',figure={})
        ],width=6,xs=12, sm=12, md=12, lg=6, xl=6),
        html.Br(),
        html.Hr(),
        dbc.Row([dbc.Col([dcc.Graph(id='patients',figure={})],width=6,xs=12, sm=12, md=12, lg=6, xl=6)])
    ])
],fluid=True)
#----------the Callbacks-------------------------------------------------------------------------------------------------------------------------

@app.callback(

    Output('revenue','figure'),

    Input('selection_op','value')

)

def update_graph(selected_category):
    df22=df[(df['year']==2022)&(df['revenue_category']==selected_category)]
    df22.columns=df22.columns.str.replace("  ","")
    df23=df[(df['year']==2023)&(df['revenue_category']==selected_category)]
    dfgrouged22=df22.groupby(['Month','Date'])['total_revenues'].sum().reset_index('Date')
    dfgrouged23=df23.groupby(['Month','Date'])['total_revenues'].sum().reset_index('Date')
    dfgrouged22=dfgrouged22.sort_values('Date')
    dfgrouged23=dfgrouged23.sort_values('Date')
    dfgrouged23['changes']=round(dfgrouged23['total_revenues']/dfgrouged22['total_revenues']-1,2)*100
    color=np.where(dfgrouged23['changes']>0,'green','red')
    fig=make_subplots(rows=2,cols=1,shared_xaxes=True,shared_yaxes=False ,vertical_spacing=0.02,
    y_title='changes in Revenues',
    row_heights=[0.7,0.2] )
    fig.layout.template="plotly_dark"
    fig.add_trace(go.Scatter(x=dfgrouged22.index,y=dfgrouged22['total_revenues'],
                line=dict(color='#00FFFF'),line_shape='spline',fill='tonexty' ,
                fillcolor='rgba(0,255,255,0.4)',name="Revenues in 2022"),
                row=1,col=1,secondary_y=False)
    fig.add_trace(go.Scatter(x=dfgrouged23.index,y=dfgrouged23['total_revenues'],line=dict(color='#66FF33'),line_shape='spline',
                fill='tonexty' ,fillcolor='rgba(102,255,51,0.4)',name="Revenues in 2023"),row=1,col=1,secondary_y=False)
    fig.add_trace(go.Bar( x=dfgrouged23.index,y=dfgrouged23['changes'],marker_color=color,name='change%')
                ,row=2,col=1,secondary_y=False)

    fig.update_layout(title=f'Total Hospital Monthly Revenues of {selected_category} ',xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),

        hovermode='x unified', plot_bgcolor='#000000',paper_bgcolor='#000000' ,showlegend=True,legend=dict(orientation='h',yanchor='bottom',y=1.02, xanchor='right',x=1))

    fig.update_traces(xaxis='x2' )
    return fig

@app.callback(

    Output('patients','figure'),

    Input('selection_op','value')

)
def updated_patients_graph(selected_category):
    df22=df[(df['year']==2022)&(df['revenue_category']==selected_category)]
    df22.columns=df22.columns.str.replace("  ","")
    df23=df[(df['year']==2023)&(df['revenue_category']==selected_category)]
    dfgrougedp22=df22.groupby(['Month','Date'])['patients'].sum().reset_index('Date')
    dfgrougedp23=df23.groupby(['Month','Date'])['patients'].sum().reset_index('Date')
    dfgrougedp22=dfgrougedp22.sort_values('Date')
    dfgrougedp23=dfgrougedp23.sort_values('Date')
    dfgrougedp23['changes_patients']=round(dfgrougedp23['patients']/dfgrougedp22['patients']-1,2)*100
    color1=np.where(dfgrougedp23['changes_patients']>0,'green','red')
    fig1=make_subplots(rows=2,cols=1,shared_xaxes=True,shared_yaxes=False ,vertical_spacing=0.02,
        y_title='Changes in Patients',
        row_heights=[0.7,0.2] )
    fig1.layout.template="plotly_dark"

    fig1.add_trace(go.Scatter(x=dfgrougedp22.index,y=dfgrougedp22['patients'],
    line=dict(color='#00FFFF'),line_shape='spline',fill='tonexty' ,
        fillcolor='rgba(0,255,255,0.4)',name="Patients in 2022"),
        row=1,col=1,secondary_y=False)
    fig1.add_trace(go.Scatter(x=dfgrougedp23.index,y=dfgrougedp23['patients'],
        line=dict(color='#66FF33'),line_shape='spline',
        fill='tonexty' ,fillcolor='rgba(102,255,51,0.4)',
        name="patients in 2023"),row=1,col=1,secondary_y=False)
    fig1.add_trace(go.Bar( x=dfgrougedp23.index,y=dfgrougedp23['changes_patients'],
        marker_color=color1,name='change%'),row=2,col=1,secondary_y=False)
    fig1.update_layout(title=f'Total Hospital Monthly patient in {selected_category} ',xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),
        hovermode='x unified', plot_bgcolor='#000000',paper_bgcolor='#000000' ,showlegend=True,legend=dict(orientation='h',yanchor='bottom',y=1.02,xanchor='right',x=1))
    fig1.update_traces(xaxis='x2' )
    return fig1

        

if __name__ == "__main__":
    app.run_server(debug=True,port=8000)