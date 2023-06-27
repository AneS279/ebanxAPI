from flask import Flask
from flask import request

app = Flask(__name__)

accounts = {}
@app.get("/balance")
def balance():
    account_id = request.args.get('account_id', '')
    if(account_id in accounts):
        return str(accounts[account_id]['amount'])
    else:
        return '0', 404

@app.post("/reset")
def reset():
    accounts = {}
    return "OK", 200

@app.post("/event")
def event():
    body = request.get_json()
    if(body['type'] == 'deposit'):
        if(body['destination'] in accounts):
            accounts[body['destination']]['amount'] += int(body['amount'])
        else:
            accounts[body['destination']] = {'amount': int(body['amount'])}
        return {"destination": {"id": body['destination'], 'balance': accounts[body['destination']]['amount']}}, 201
    elif(body['type'] == 'withdraw'):
        if(body['origin'] in accounts):
            accounts[body['origin']]['amount'] -= int(body['amount'])
            return {"origin": {"id": body['origin'], 'balance': accounts[body['origin']]['amount']}}, 201
        else:
            return '0', 404
    elif(body['type'] == 'transfer'):
        if(body['origin'] in accounts):
            if(body['destination'] in accounts):
                accounts[body['origin']]['amount'] -= int(body['amount'])
                accounts[body['destination']]['amount'] += int(body['amount'])
            else:
                accounts[body['destination']] = {'amount': int(body['amount'])}
                accounts[body['origin']]['amount'] -= int(body['amount'])
            return {"destination": {"id": body['destination'], 'balance': accounts[body['destination']]['amount']},
                    "origin": {"id": body['origin'], 'balance': accounts[body['origin']]['amount']}}, 201
        else:
            return '0', 404