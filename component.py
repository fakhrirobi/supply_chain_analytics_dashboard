from dash import html,dcc
import dash_bootstrap_components as dbc 
import dash_mantine_components as dmc 
from datetime import datetime, timedelta, date

date_range = dmc.DateRangePicker(
                id="date_range",
                label="Select Date Range",
                minDate=date(2015, 1, 1),maxDate=date(2018,1,31),
                value=[date(2015, 1, 1), date(2018,1,31)],
                style={"width": 330},
            )


card_style = {'border-style':'solid','width':'250px','border-color':'#d9d7d7'}
card_indicator = dmc.Group([
    dbc.Col(
dbc.Card([dbc.CardHeader('Total Order',style=card_style),
          dbc.CardBody(dcc.Graph(id='total_order'),style=card_style)])),
    dbc.Col(
dbc.Card([dbc.CardHeader('% Perfect Order',style=card_style),
          dbc.CardBody(dcc.Graph(id='perfect_order_pct'),style=card_style)])),
    dbc.Col(
dbc.Card([dbc.CardHeader('Average Shipment Delay',style=card_style),
          dbc.CardBody(dcc.Graph(id='avg_shipment_delay'),style=card_style)])),
],style={'margin-left':'30rem'})

chart2_style = {'width':'500px','border-color':'#d9d7d7'}
chart2 = dmc.Group([
    dbc.Col(
dbc.Card([dbc.CardHeader('Customer Segment Proportion'),
          html.Br(),
          dbc.CardBody(dcc.Graph(id='customer_segment'))]),style=chart2_style),
    dbc.Col(
dbc.Card([dbc.CardHeader('Shipment Delay (Days)'),
          html.Br(),
          dbc.CardBody(dcc.Graph(id='shipment_delay_days'))]),style=chart2_style),
    dbc.Col(
dbc.Card([dbc.CardHeader('Time Series of % On Time'),
          html.Br(),
          dbc.CardBody(dcc.Graph(id='ts_ontime_pct'))]),style=chart2_style),

],style={'margin-left':'5rem','margin-right':'5rem','width':'100%'})

chart3_style = {'width':'750px','border-color':'#d9d7d7'}
chart3 = dmc.Group([
    dbc.Col(
dbc.Card([dbc.CardHeader('% On Time Shipment based on Shipping Mode'),
          html.Br(),
          dbc.CardBody(dcc.Graph(id='shipping_mode'))]),style=chart3_style),
    dbc.Col(
dbc.Card([dbc.CardHeader('% On Time Shipment based on Customer Segment'),
          html.Br(),
          dbc.CardBody(dcc.Graph(id='pct_on_time_customer_segment'))]),style=chart3_style),
    dbc.Col(
dbc.Card([dbc.CardHeader('% On Time Shipment Best on 10 Biggest Total Transaction Shipment Route '),
          html.Br(),
          dbc.CardBody(dcc.Graph(id='biggest_shipment_route'))]),style=chart3_style),


],style={'margin-left':'5rem','margin-right':'5rem','width':'100%'})

