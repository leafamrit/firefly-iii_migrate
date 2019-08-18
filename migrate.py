#!/usr/bin/env python
from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for, render_template
from flask.json import jsonify
from werkzeug import secure_filename
from cred import src, snk
import json
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

data = {"src": {}, "snk": {}}

@app.route('/')
def index():
    if data:
        return render_template("index.html", session=session, data=json.dumps(data))
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

@app.route('/get_data/<target>/<type>')
def get_data(target, type):
    client = set_target(target)
    if client:
        firefly = OAuth2Session(client["client_id"], token=session[target + '_oauth_token'])
        data[target][type] = firefly.get(client["url"] + '/api/v1/' + type).json()
        return redirect(url_for('.index'))
    else:
        return False

@app.route('/import_accounts')
def import_accounts():
    key_map = {
        "name": ["name", {}],
        "type": ["type", {
            "Default account": "asset",
            "Cash account": "asset",
            "Asset account": "asset",
            "Expense account": "expense",
            "Revenue account": "revenue",
            "Initial balance account": "asset",
            "Beneficiary account": "asset",
            "Import account": "asset",
            "Loan": "liability",
            "Reconciliation account": "liability",
            "Debt": "liability",
            "Mortgage": "liability"
        }],
        "iban": ["iban", {}],
        "bic": ["bic", {}],
        "account_number": ["account_number", {}],
        "opening_balance": ["opening_balance", {}],
        "opening_balance_date": ["opening_balance_date", {}],
        "virtual_balance": ["virtual_balance", {}],
        "currency_id": ["currency_id", {}],
        "currency_code": ["currency_code", {}],
        "active": ["active", {}],
        "include_net_worth": ["include_net_worth", {True: "true", False: "false"}],
        "account_role": ["role", {}],
        "credit_card_type": ["credit_card_type", {}],
        "monthly_payment_date": ["monthly_payment_date", {}],
        "liability_type": ["liability_type", {}],
        "liability_amount": ["liability_amount", {}],
        "liability_start_date": ["liability_start_date", {}],
        "interest": ["interest", {}],
        "interest_period": ["interest_period", {}],
        "notes": ["notes", {}]
    }
    if session and ("src_oauth_token" in session.keys()) and ("snk_oauth_token" in session.keys()):
        firefly = OAuth2Session(snk["client_id"], token=session['snk_oauth_token'])
        if data and ("accounts" in data["src"].keys()):
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            for account in data["src"]["accounts"]["data"]:
                request_body = {}
                for key in key_map.keys():
                    if key_map[key][0] in account["attributes"].keys() and account["attributes"][key_map[key][0]] != None:
                        if len(key_map[key][1]) > 0:
                            request_body[key] = key_map[key][1][account["attributes"][key_map[key][0]]]
                        else:
                            request_body[key] = account["attributes"][key_map[key][0]]

                print(json.dumps(request_body))
                print(firefly.post(snk["url"] + '/api/v1/accounts', data=json.dumps(request_body), headers=headers).content)
            print("all accounts imported")
            return redirect(url_for(".index"))
        else:
            return "bad request", 400
    else:
        return "bad request", 400

@app.route('/upload_records', methods=["POST"])
def upload_records():
    f = request.files['records']
    f.save('./uploads/' + secure_filename(f.filename))
    return "upload successful"

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
