from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import requests

app = Flask(__name__)

# 样例数据
strategy_data = {
    "name": "均线策略",
    "description": "利用均线交叉信号进行交易的策略",
    "trades": [
        {
            "pair": "BTC/USDT",
            "side": "buy",
            "price": 45000,
            "amount": 0.02,
            "fee": 0.0015
        },
        {
            "pair": "ETH/USDT",
            "side": "sell",
            "price": 3000,
            "amount": 1.5,
            "fee": 0.002
        }
    ],
    "capital_curve": [
        {"date": "2022-01-01", "value": 10000},
        {"date": "2022-01-02", "value": 10250},
        {"date": "2022-01-03", "value": 10100},
        {"date": "2022-01-04", "value": 10400},
        {"date": "2022-01-05", "value": 10500}
    ],
    "history_trades": [
        {
            "pair": "BTC/USDT",
            "side": "buy",
            "price": 42000,
            "amount": 0.01,
            "fee": 0.001
        },
        {
            "pair": "ETH/USDT",
            "side": "sell",
            "price": 3200,
            "amount": 1.8,
            "fee": 0.0025
        }
    ]
}

@app.route('/')
def strategy():
    return render_template('strategy.html')

# 获取策略数据的接口
@app.route('/get_data')
def get_data():
    return jsonify(strategy_data)

# 启动策略的接口
@app.route('/start_strategy', methods=['POST'])
def start_strategy():
    data = request.get_json()
    # 处理启动策略请求
    return jsonify({'status': 'success'})

# 异步获取所有策略数据并在页面上显示
def get_all_strategy_data():
    # 异步请求后端接口，获取策略数据
    data = requests.get('/get_data').json()

    # 更新监控开单情况表格的内容
    trades = data['trades']
    trade_table_content = ''
    for trade in trades:
        trade_table_content += f'<tr><td>{trade["pair"]}</td><td>{trade["side"]}</td><td>{trade["price"]}</td><td>{trade["amount"]}</td><td>{trade["fee"]}</td></tr>'

    # 更新资金曲线图的数据
    capital_curve = data['capital_curve']
    capital_dates = []
    capital_values = []
    for point in capital_curve:
        capital_dates.append(point['date'])
        capital_values.append(point['value'])

    # 更新历史交易记录表格的内容
    history_trades = data['history_trades']
    history_table_content = ''
    for trade in history_trades:
        history_table_content += f'<tr><td>{trade["pair"]}</td><td>{trade["side"]}</td><td>{trade["price"]}</td><td>{trade["amount"]}</td><td>{trade["fee"]}</td></tr>'

    # 向前端发送更新后的数据
    socketio.emit('update_data', {
        'trade_table_content': trade_table_content,
        'capital_dates': capital_dates,
        'capital_values': capital_values,
        'history_table_content': history_table_content
    })


if __name__ == '__main__':
    app.run(debug=True)
