import flask

import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)


_app_route = '/dash-core-components/logout_button'


# Create a login route
@app.server.route('/custom-auth/login', methods=['POST'])
def route_login():
    data = flask.request.form
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        flask.abort(401)

    # actual implementation should verify the password.
    # Recommended to only keep a hash in database and use something like
    # bcrypt to encrypt the password and check the hashed results.

    # Return a redirect with
    rep = flask.redirect(_app_route)

    # Here we just store the given username in a cookie.
    # Actual session cookies should be signed or use a JWT token.
    rep.set_cookie('custom-auth-session', username)
    return rep


# create a logout route
@app.server.route('/custom-auth/logout', methods=['POST'])
def route_logout():
    # Redirect back to the index and remove the session cookie.
    rep = flask.redirect(_app_route)
    rep.set_cookie('custom-auth-session', '', expires=0)
    return rep


# Simple dash component login form.
login_form = html.Div([
    html.Form([
        dcc.Input(placeholder='username', name='username'),
        dcc.Input(placeholder='password', name='password', type='password'),
        html.Button('Login', type='submit')
    ], action='/custom-auth/login', method='post')
])


def dynamic_layout():
    if not flask.has_request_context():
        # Functions layout get validated before the first request.
        return login_form
    session_cookie = flask.request.cookies.get('custom-auth-session')

    if not session_cookie:
        # If there's no cookie we need to login.
        return login_form
    return html.Div([
        html.Div('Hello {}'.format(session_cookie)),
        dcc.LogoutButton(logout_url='/custom-auth/logout')
    ])


app.layout = dynamic_layout

if __name__ == '__main__':
    app.run_server(debug=True)