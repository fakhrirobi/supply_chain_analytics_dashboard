import dash 
from dash_extensions.enrich import ServersideOutput,ServersideOutputTransform,DashProxy
from dash import callback,Input,Output,html,dcc
import dash_bootstrap_components as dbc 
import dash_mantine_components as dmc 
from component import card_indicator,date_range,chart2,chart3
import pandas as pd 
import numpy as np 
import plotly.express as px 
import plotly.graph_objects as go 
from datetime import datetime, timedelta, date

external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Work+Sans:wght@500&display=swap",
    "https://tailwindcss.com/",
    "https://cdn.sheetjs.com/xlsx-latest/package/dist/xlsx.full.min.js",
    {"src": "https://cdn.tailwindcss.com"},
    dbc.themes.BOOTSTRAP,
]
app = DashProxy(__name__,external_stylesheets=external_stylesheets,transforms=[ServersideOutputTransform()]) 




#layout 


app.layout = html.Div(children=[
    dcc.Store(id='store_shipping_df'),
    dbc.Row(id='dummy_input'),
    dbc.Row(children=date_range,style={'margin-left':'45rem'}),
    html.Br(),
    dbc.Row(card_indicator),
    html.Br(),
    html.Br(),
    dbc.Row(chart2),
    html.Br(),
    html.Br(),
    dbc.Row(chart3)
])

def create_crosstab(data,index) : 
    var = pd.crosstab(data[index], data['ontime_delivery']).reset_index()
    var['total'] = var['delayed'] + var['ontime']
    var['delayed']/=var['total']
    var['ontime']/=var['total']
    var['delayed']= np.round(var['delayed']*100,2)
    var['ontime']= np.round(var['ontime']*100,2)
    return var


@app.callback(ServersideOutput("store_shipping_df", "data"),
              Input('dummy_input','children'),memoize=True,prevent_initial_call=False)
def render_data(dummy) :
    data  = pd.read_csv('shipping.csv')
    data['order_date'] = pd.to_datetime(data['order_date'])
    return data
    



@app.callback([Output('total_order','figure'),
               Output('perfect_order_pct','figure'),
               Output('avg_shipment_delay','figure')],
              [Input('date_range','value'),Input("store_shipping_df", "data")]
              
               )
def generate_indicator(date_range,data) : 
    data= data[(data['order_date'] >= date_range[0]) & (data['order_date'] <= date_range[1])]
    total_order = go.Figure()
    total_order.add_trace(go.Indicator(
        mode = "number",
        number = {'font':{'size':40}},
        value = data['order_date'].count()))
    
    c = data.groupby('ontime_delivery').agg({'order_date':'count'}).reset_index()
    total = c['order_date'].sum()
    c['order_date']/=total
    c['order_date']= np.round(c['order_date']*100,2)
    perfect_order_val = c.loc[c['ontime_delivery']=='ontime','order_date'].values.tolist()[0]
    perfect_order_pct = go.Figure()
    perfect_order_pct.add_trace(go.Indicator(
        number = {'suffix': "%",'font':{'size':40}},
        mode = "number",
        value = perfect_order_val))
    avg_shipment_delay_value = data.loc[data['shipment_delay']>0,'shipment_delay'].mean()
    avg_shipment_delay = go.Figure()
    avg_shipment_delay.add_trace(go.Indicator(
        number = {'suffix': " Days",'font':{'size':40}},
        mode = "number",
        value = avg_shipment_delay_value))
    total_order.update_layout(width=200,height=100)
    avg_shipment_delay.update_layout(width=200,height=100)
    perfect_order_pct.update_layout(width=200,height=100)
    return total_order,perfect_order_pct,avg_shipment_delay

@app.callback(Output('customer_segment','figure'),
              [Input('date_range','value'),Input("store_shipping_df", "data")]
              
               )
def render_customer_segment(date_range,data) : 
    data= data[(data['order_date'] >= date_range[0]) & (data['order_date'] <= date_range[1])]
    groupby_customer_segment = data.groupby('customer_segment').agg({'order_date':'count'}).reset_index()
    fig = px.pie(groupby_customer_segment, values='order_date', names='customer_segment', template='xgridoff', color_discrete_sequence=px.colors.qualitative.Prism)
    fig.update_layout(title=f'Transaction from {date_range[0]} to {date_range[1]}')
    return fig

@app.callback(Output('shipping_mode','figure'),
              [Input('date_range','value'),Input("store_shipping_df", "data")]
              
               )
def render_ontime_pct_shipping_mode(date_range,data) : 
    data= data[(data['order_date'] >= date_range[0]) & (data['order_date'] <= date_range[1])]
    var = create_crosstab(data=data,index='shipping_mode')
    fig = px.bar(var, x='shipping_mode', y='ontime', color='shipping_mode', color_discrete_sequence=px.colors.qualitative.Prism, 
             template='xgridoff',text_auto=True)
    fig.update_layout(title=f'Transaction from {date_range[0]} to {date_range[1]}')
    return fig 

@app.callback(Output('pct_on_time_customer_segment','figure'),
              [Input('date_range','value'),Input("store_shipping_df", "data")]
              
               )
def render_ontime_pct_customer_segment(date_range,data) : 
    data= data[(data['order_date'] >= date_range[0]) & (data['order_date'] <= date_range[1])]
    var = create_crosstab(data=data,index='customer_segment')
    fig = px.bar(var, x='customer_segment', y='ontime', color='customer_segment', color_discrete_sequence=px.colors.qualitative.Prism, 
                template='xgridoff',text_auto=True)
    fig.update_layout(title=f'Transaction from {date_range[0]} to {date_range[1]}')
    return fig 

@app.callback(Output('shipment_delay_days','figure'),
              [Input('date_range','value'),Input("store_shipping_df", "data")]
              
               )
def render_shipment_delay(date_range,data) : 
    data= data[(data['order_date'] >= date_range[0]) & (data['order_date'] <= date_range[1])]
    groupby_shipping_delay = data.groupby('shipment_delay').agg({'order_date':'count'})
    groupby_shipping_delay = data.groupby('shipment_delay').agg({'order_date':'count'})
    groupby_shipping_delay = groupby_shipping_delay.reset_index()
    groupby_shipping_delay = groupby_shipping_delay.loc[groupby_shipping_delay['shipment_delay']>=0]
    groupby_shipping_delay['shipment_delay'] =groupby_shipping_delay['shipment_delay'].astype('category')
    fig = px.bar(groupby_shipping_delay, x='shipment_delay', y='order_date', color='shipment_delay', color_discrete_sequence=px.colors.qualitative.Prism, 
             template='xgridoff',text_auto=True)
    fig.update_yaxes(title='count')
    fig.update_xaxes(title='shipment_delay')
    fig.update_layout(title=f'Transaction from {date_range[0]} to {date_range[1]}')
    return fig 

@app.callback(Output('ts_ontime_pct','figure'),
              [Input('date_range','value'),Input("store_shipping_df", "data")]
              
               )
def render_shipment_delay(date_range,data) : 
    print('date_range',date_range)
    
    data= data[(data['order_date'] >= date_range[0]) & (data['order_date'] <= date_range[1])]
    # data['order_date_year'] = data['order_date'].dt.year
    # data['order_date_month_number'] = data['order_date'].dt.month
    # data = data.sort_values(['order_date_month_number','order_date_year'])
    data['year_month'] = data['order_date'].dt.strftime('%Y-%m')
    ts = create_crosstab(data=data,index='year_month')
    fig = px.line(ts.sort_values(by=['year_month'], ascending=[True]), x='year_month', y='ontime', template='xgridoff', color_discrete_sequence=px.colors.qualitative.Prism)
    fig.update_layout(title=f'Transaction from {date_range[0]} to {date_range[1]}')
    return fig 

@app.callback(Output('biggest_shipment_route','figure'),
              [Input('date_range','value'),Input("store_shipping_df", "data")]
              
               )
def render_top_10_order_route_pct(date_range,data) : 
    data= data[(data['order_date'] >= date_range[0]) & (data['order_date'] <= date_range[1])]
    data['source_destination_country'] = data['customer_country'] +' to '+ data['order_country']
    source_destination_country_ontime = create_crosstab(data=data,
                                                        index='source_destination_country')
    source_destination_country_ontime_top_10 = source_destination_country_ontime.sort_values('total',ascending=False)\
    .nlargest(10,columns='total')
    fig = px.bar(source_destination_country_ontime_top_10, x='source_destination_country', y='ontime', color='source_destination_country', color_discrete_sequence=px.colors.qualitative.Prism, 
                template='xgridoff',text_auto=True)
    fig.update_yaxes(title='%Ontime')
    fig.update_xaxes(title='Route')
    fig.update_layout(title=f'Transaction from {date_range[0]} to {date_range[1]}')
    return fig

if __name__ == '__main__' : 
        app.run(
        debug=True,
        #port=5000,#host="0.0.0.0",
        dev_tools_hot_reload=True,
    )

