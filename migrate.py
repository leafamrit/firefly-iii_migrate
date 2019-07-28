#!/usr/bin/env python
from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
from cred import source, sink
import os

# --cred.py
# source = {
#     'client_id': r'<source_client_id>',
#     'client_secret': r'<source_client_secret>',
#     'url': r'<source_url>'
#     }
# sink = {
#     'client_id': r'<sink_client_id>',
#     'client_secret': r'<sink_client_secret>',
#     'url': r'<sink_url>'
#     }
# source['auth_base_url'] = source['url'] + r'/oauth/authorize'
# source['token_url'] = source['url'] + r'/oauth/token'
# sink['auth_base_url'] = sink['url'] + r'/oauth/authorize'
# sink['token_url'] = sink['url'] + r'/oauth/token'

flask = Flask(__name__)

@app.route('/')
def home():
    firefly = OAuth2Session(client_id)
    authorization_url, state = firefly.authorization_url(authorization_base_url)

    session['oauth_state'] = state
    return redirect(authorization_url)
