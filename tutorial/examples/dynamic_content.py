import dash
from dash.dependencies import Event, Output
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.Button('Click to load children', id='display-children-button'),
    html.Div('-', id='display-children')
])


# When you click the button, this content gets loaded
@app.callback(
    Output('display-children', 'children'),
    events=[Event('display-children-button', 'click')])
def render():
    return html.Div([
        html.H3('Hello Dash')
    ])


if __name__ == '__main__':
    app.run_server(debug=True)
