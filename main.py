from flask import Flask
from flask import request

app = Flask(__name__)

accounts = {}
@app.get("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.post("/reset")
def reset():
    accounts = {}
    return "OK", 200

@app.post("/event")
def event():
    bodyRequest = request.get_json()
    if(bodyRequest['type'] == 'deposit'):
        if(bodyRequest['destination'] in accounts):
            accounts[bodyRequest['destination']]['amount'] += int(bodyRequest['amount'])
        else:
            accounts[bodyRequest['destination']] = {'amount': int(bodyRequest['amount'])}
        return {"destination": {"id": bodyRequest['destination'], 'balance': accounts[bodyRequest['destination']]['amount']}}, 201
    elif(bodyRequest['type'] == 'withdraw'):
        if(bodyRequest['origin'] in accounts):
            accounts[bodyRequest['origin']]['amount'] -= int(bodyRequest['amount'])
            return {"origin": {"id": bodyRequest['origin'], 'balance': accounts[bodyRequest['origin']]['amount']}}, 201
        else:
            return 404
    elif(bodyRequest['type'] == 'transfer'):
        
#reset - POST