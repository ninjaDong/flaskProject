import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2('登录'),
    html.Label('用户名'),
    dcc.Input(
        id='username-input',
        type='text',
        placeholder='请输入用户名'
    ),
    html.Label('密码'),
    dcc.Input(
        id='password-input',
        type='password',
        placeholder='请输入密码'
    ),
    html.Button('登录', id='login-button', n_clicks=0),
    html.Div(id='login-status')
])

@app.callback(
    dash.dependencies.Output('login-status', 'children'),
    [dash.dependencies.Input('login-button', 'n_clicks')],
    [dash.dependencies.State('username-input', 'value'),
     dash.dependencies.State('password-input', 'value')])
def authenticate_user(n_clicks, username, password):
    if n_clicks > 0:
        # 在这里进行用户认证逻辑，如果用户名和密码正确，则返回成功信息，否则返回失败信息。
        if username == "ninja" and password == "lznbjs":
            return html.Div('登录成功！')
        else:
            return html.Div('用户名或密码错误，请重新输入。')

if __name__ == '__main__':
    app.run_server(debug=True)
