#!/usr/bin/env python
from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os

app = Flask(__name__)

client_id = r'2'
client_secret = r'PasxQN33izpU8udo7KLL3AmhvxQVnrh3WA2PGb2M'
authorization_base_url = 'http://arkeyve-firefly.herokuapp.com/oauth/authorize'
token_url = r'http://arkeyve-firefly.herokuapp.com/oauth/token'

@app.route('/')
def demo():
    firefly = OAuth2Session(client_id)
    authorization_url, state = firefly.authorization_url(authorization_base_url)

    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/callback', methods=["GET"])
def callback():
    firefly = OAuth2Session(client_id, state=session['oauth_state'])
    token = firefly.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)

    session['oauth_token'] = token

    return redirect(url_for('.profile'))

@app.route('/profile', methods=["GET"])
def profile():
    firefly = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(firefly.get('http://arkeyve-firefly.herokuapp.com/api/v1/transactions').json())

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.secret_key = os.urandom(24)
    app.run(debug=True)
