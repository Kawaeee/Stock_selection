import dash
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime
import time

data = pd.read_csv('predicted_data/BAY.BK.csv', parse_dates=['Date'],index_col='Date')

external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/bulma/0.2.1/css/bulma.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

increasing_color = '#98fb98'
decreasing_color = '#ee2400'

col = '#000000'
result_col = ['#006400','#8b0000']

colors = []
for i, _ in enumerate(data.index):
    if i != 0:
        if data['Close'].iloc[i] > data['Close'].iloc[i-1]:
            colors.append(increasing_color)
        else:
            colors.append(decreasing_color)
    else:
        colors.append(decreasing_color)

app.title = 'CABBAGE Stock Prediction System'
app.layout = html.Div([ 
  dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Bank of Ayudhya PCL [BAY.BK]', 'value': 'BAY.BK'},
            {'label': 'Bangkok Bank PCL [BBL.BK]', 'value': 'BBL.BK'},
            {'label': 'CIMB Thai Bank PCL [CIMBT.BK]', 'value': 'CIMBT.BK'},
            {'label': 'Kasikornbank PCL [KBANK.BK]', 'value': 'KBANK.BK'},
            {'label': 'Kiatnakin Bank PCL [KKP.BK]', 'value': 'KKP.BK'},
            {'label': 'Krung Thai Bank PCL [KTB.BK]', 'value': 'KTB.BK'},
            {'label': 'LH Financial Group PCL [LHFG.BK]', 'value': 'LHFG.BK'},
            {'label': 'Siam Commercial Bank PCL [SCB.BK]', 'value': 'SCB.BK'},
            {'label': 'Thanachart Capital PCL [TCAP.BK]', 'value': 'TCAP.BK'},
            {'label': 'TISCO Financial Group PCL [TISCO.BK]', 'value': 'TISCO.BK'},
            {'label': 'TMB Bank PCL [TMB.BK]', 'value': 'TMB.BK'},
        ],
        value='BAY.BK'
    ),
   dcc.DatePickerSingle(
        style={'textAlign': 'center','display': 'flex','align-items': 'center','justify-content': 'center'},
        id='my-date-picker-single',
        #wait for data
        min_date_allowed=datetime(2016, 5, 9),
        max_date_allowed=datetime(2019, 8, 1),
        initial_visible_month=datetime.now().strftime('%Y-%m-%d'),
        date=str(datetime.now().strftime('%Y-%m-%d'))
    ),
    html.Div(id='output-container-date-picker-single',style={'textAlign': 'center','display': 'flex','align-items': 'center','justify-content': 'center'}),
    html.Div(className="row",children=[
        html.Div('Suggestion in next 30 days',id='result_1',style={
         'width': '49%',
            'display': 'inline-block',
            'left':'auto',
            'textAlign': 'center',
            'align-items': 'center',
            'justify-content': 'center',
            'font-size': '125%',
            'font-weight':'bold'}
         ),
        html.Div('Profit gain/loss in next 30 days',id='result_0',style={
            'width': '49%',
            'display': 'inline-block',
            'position':'absolute',
            'right':'auto',
            'textAlign': 'center',
            'align-items': 'center',
            'justify-content': 'center',
            'font-size': '125%',
            'font-weight':'bold'}
            )
    ]),
   html.Div(className="row1",children=[
        html.Div(id='result_2',style={
            'width': '49%',
            'display': 'inline-block',
            'left':'auto',
            'textAlign': 'center',
            'align-items': 'center',
            'justify-content': 'center',
            'font-size': '250%',
            'color':col,
            'font-weight':'bold',
            'text-decoration':'underline'}
            ),
             html.Div(id='result_3',style={
            'width': '49%',
            'display': 'inline-block',
            'position':'absolute',
            'right':'auto',
            'textAlign': 'center',
            'align-items': 'center',
            'justify-content': 'center',
            'font-size': '250%',
            'color':col,
            'font-weight':'bold',
            'text-decoration':'underline'}
            )
   ]),
   #html.H1(id='blank',style={'textAlign': 'center','display': 'flex','align-items': 'center','justify-content': 'center','font-size': '200%'}),
   dcc.Graph(
    figure=go.Figure(
        data=[
            go.Candlestick(
            x=data.index,open=data['Open'], high=data['High'],
            low=data['Low'], close=data['Close'],
            yaxis='y2',
            name='BAY.BK',
            increasing=dict(line=dict(color=increasing_color)),
            decreasing=dict(line=dict(color=decreasing_color)),
            ),
            go.Bar(
                x=data.index, y=data['Volume'],
                marker=dict(color=colors),
                yaxis='y', name='Volume'
            )
        ],
        layout=go.Layout(
            title='Stock Selection System',
            showlegend=True,
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label='reset',
                            step='all'),
                        dict(count=6,
                            label='6m',
                            step='month',
                            stepmode='backward'),
                        dict(count=3,
                            label='3m',
                            step='month',
                            stepmode='backward'),
                        dict(count=1,
                            label='1m',
                            step='month',
                            stepmode='backward'),
                        dict(count=14,
                            label='1wk',
                            step='day',
                            stepmode='backward')
                    ])
            ),
            rangeslider=dict(
            visible = True
            )),
            yaxis= go.layout.YAxis(
                domain = [0.0, 0.4],
                showticklabels = True
            ),
            yaxis2= go.layout.YAxis(
                domain = [0.4, 1.0],
                showticklabels = True
            ),
            legend=go.layout.Legend(
                x=0,
                y=1.0
            ),
            shapes=[dict(
               type = 'rect',
                # x-reference is assigned to the x-values
               xref =  'x',
                # y-reference is assigned to the plot paper [0,1]
               yref = 'paper',
               x0 = '2019-05-27',
               y0 = 0,
               x1 = '2019-07-24',
               y1=1,
               fillcolor= '#add8e6',
               opacity = 0.3,
               line=dict(width = 0)
            )],
            margin=go.layout.Margin(l=40, r=40, t=40, b=40)
        )
    ),
    style={'height': 600},
    id='my-graph'
    ),
    html.Footer('CSC344 Decision Support Systems - CABBAGE group',style={'textAlign': 'center'})
], className="container")



@app.callback(
    dash.dependencies.Output('output-container-date-picker-single', 'children'),
    [dash.dependencies.Input('my-date-picker-single', 'date')])

#TIME
def update_output(date):
    string_prefix = 'You have selected: '
    
    if date is not None:
        date = datetime.strptime(date, '%Y-%m-%d')    
        date_string = date.strftime('%B %d, %Y')

        return string_prefix + date_string

@app.callback(
    [dash.dependencies.Output('result_2', 'children'),dash.dependencies.Output('result_3', 'children')],
    [dash.dependencies.Input('my-date-picker-single', 'date'),Input('my-dropdown', 'value')])

def update_result(date,value):
    result = ["BUY","SELL","HOLD"]
    #next 30 days
    forecast_time = int(30)
    generator = pd.date_range(start=date, periods=forecast_time, freq='B').date
    start = generator[0]
    end = generator[-1]
    
    df = pd.read_csv("predicted_data/"+value+'.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    newdata = df[(df.Date > start) & (df.Date < end)]
    
    #green = 0
    #red = 0
    #len(close_data)

    open_data = list(newdata["Open"])
    close_data = list(newdata["Close"])
    final_change = 0


    final_change = ((close_data[-1]-close_data[0])/close_data[0])*100

    """
    #find percent change
    for i in range(0,len(close_data)): 
      change =  close_data[i] - open_data[i]
      percent_change = (change/open_data[i])*100
      final_change += percent_change
    """

    if(final_change > 0.25):
        return result[0],str("{0:.2f}% : Profit".format(final_change))
    elif(final_change >= -0.25 and final_change <= 0.25):
        return result[2],str("{0:.2f}% : Normal".format(final_change))
    elif(final_change < -0.25):
        return result[1],str("{0:.2f}% : Loss".format(final_change))

    #green > red algorithm that not wok
    """
    for i in range(0,len(close_data)): 
        if close_data[i] > open_data[i]:
            green += 1 
        else:
            red += 1

    if(green>=red):
     col = result_col[0]
     return result[0]
    else:
     col = result_col[1]
     return result[1]
    """


@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value'),dash.dependencies.Input('my-date-picker-single', 'date')])

def update_graph(selected_dropdown_value,date):
    newdata = pd.read_csv("predicted_data/"+selected_dropdown_value+'.csv', parse_dates=['Date'],index_col='Date')
    data = [ dict(
        type = 'candlestick',
        open = newdata.Open,
        high = newdata.High,
        low = newdata.Low,
        close = newdata.Close,
        x = newdata.index,
        yaxis = 'y2',
        name = selected_dropdown_value
        ),
        dict(
        type ='bar',
        x = newdata.index,
        y= newdata['Volume'],
        marker=dict(color=colors),
        yaxis='y',
        name='Volume'
        )
    ]
    layout=go.Layout(
            title='Stock Selection System',
            showlegend=True,
            xaxis=dict(
                range = [date,'2020-01-01'],
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label='reset',
                            step='all'),
                        dict(count=6,
                            label='6m',
                            step='month',
                            stepmode='backward'),
                        dict(count=3,
                            label='3m',
                            step='month',
                            stepmode='backward'),
                        dict(count=1,
                            label='1m',
                            step='month',
                            stepmode='backward'),
                        dict(count=14,
                            label='1wk',
                            step='day',
                            stepmode='backward')
                    ])
            ),
            rangeslider=dict(
            visible = True
            )),
            yaxis= go.layout.YAxis(
                domain = [0.0, 0.4],
                showticklabels = True
            ),
            yaxis2= go.layout.YAxis(
                domain = [0.4, 1.0],
                showticklabels = True
            ),
            legend=go.layout.Legend(
                x=0,
                y=1.0
            ),
            shapes=[dict(
               type = 'rect',
                # x-reference is assigned to the x-values
               xref =  'x',
                # y-reference is assigned to the plot paper [0,1]
               yref = 'paper',
               x0 = '2019-05-27',
               y0 = 0,
               x1 = '2019-07-25',
               y1=1,
               fillcolor= '#add8e6',
               opacity = 0.3,
               line=dict(width = 0)
            )],
            margin=go.layout.Margin(l=40, r=40, t=40, b=40)
        )

    return {'data': data, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)