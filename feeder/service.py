#!/usr/bin/env python

from flask import Flask, request, jsonify, make_response

app = Flask('Feeding service')


@app.route('/', methods=['GET'])
def main():
    return make_response(jsonify({'status': 'ok', 'message': 'Feeding service is running'}), 200)


@app.route('/feed', methods=['POST'])
def feed():
    params = request.json

    feeder = FeederClient()

    result = feeder.feed(params.get('slot'), params.get('amount'))

    return make_response(jsonify(result), 200)


class FeederClient:
    def __init__(self):
        pass

    def feed(self, slot, amount):
        return 'From slot ' + str(slot) + ' dropped ' + str(amount) + ' portions of food'


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001)
