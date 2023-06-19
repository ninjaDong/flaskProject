import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import pymongo

# 连接MongoDB数据库
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
trade_records = db["trade_records"]

# 从MongoDB读取数据并转化为Pandas DataFrame对象
df = pd.DataFrame(list(trade_records.find()))

# 创建Dash应用程序实例
app = dash.Dash(__name__)

# 应用程序布局
app.layout = html.Div(children=[
    html.H1(children='期货交易监控系统'),

    html.Div(children='''
        交易记录：
    '''),

    # 表格展示交易记录
    html.Table(
        # 表头
        [html.Tr([html.Th(col) for col in df.columns])] +

        # 表格内容
        [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(len(df))]
    ),

    html.Div(children='''
        资金曲线：
    '''),

    # 折线图展示资金曲线
    dcc.Graph(
        id='capital-curve',
        figure={
            'data': [
                {'x': df['date'], 'y': df['capital'], 'type': 'line', 'name': 'Capital Curve'},
            ],
            'layout': {
                'title': 'Capital Curve'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
