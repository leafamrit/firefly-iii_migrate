#!/usr/bin/env python
from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for, render_template
from flask.json import jsonify
from cred import src, snk
import os

# --cred.py
# src = {
#     'client_id': r'<source_client_id>',
#     'client_secret': r'<source_client_secret>',
#     'redirect_uri': 'http://localhost:5000/callback/src',
#     'url': r'<source_client_url>'
#     }
# snk = {
#     'client_id': r'<sink_client_id>',
#     'client_secret': r'<sink_client_secret>',
#     'redirect_uri': 'http://localhost:5000/callback/snk',
#     'url': r'<sink_client_url>'
#     }
# src['auth_base_url'] = src['url'] + r'/oauth/authorize'
# src['token_url'] = src['url'] + r'/oauth/token'
# snk['auth_base_url'] = snk['url'] + r'/oauth/authorize'
# snk['token_url'] = snk['url'] + r'/oauth/token'

app = Flask(__name__)

def set_target(target):
    if target == "src":
        return src
    elif target == "snk":
        return snk
    else:
        return False

@app.route('/')
def index():
    def get_data(target, type):
        client = set_target(target)
        if client:
            firefly = OAuth2Session(client["client_id"], token=session[target + '_oauth_token'])
            return firefly.get(client["url"] + '/api/v1/' + type).json()
        else:
            return False

    data = None
    if session and ("src_oauth_token" in session.keys()) and ("snk_oauth_token" in session.keys()):
        data = {
            'src': {
                'accounts': get_data('src', 'accounts')
            },
            'snk': {
                'accounts': get_data('snk', 'accounts')
            }
        }

    if data:
        return render_template("index.html", sess=session, data=data)
    else:
        return render_template("index.html", sess=session)

@app.route('/get_connection/<target>')
def get_connection(target):
    client = set_target(target)
    if client:
        firefly = OAuth2Session(client["client_id"], redirect_uri=client['redirect_uri'])
        authorization_url, state = firefly.authorization_url(client["auth_base_url"])

        session[target + '_oauth_state'] = state
        return redirect(authorization_url)
    else:
        return "bad request", 400

@app.route('/callback/<target>', methods=["GET"])
def callback(target):
    client = set_target(target)
    if client:
        firefly = OAuth2Session(client["client_id"], state=session[target + '_oauth_state'], redirect_uri=client['redirect_uri'])
        token = firefly.fetch_token(client["token_url"], client_secret=client["client_secret"], authorization_response=request.url)

        session[target + '_oauth_token'] = token
        return redirect(url_for('.index'))
    else:
        return "bad request", 400

if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.secret_key = os.urandom(24)
    app.run(debug=True)
