#!/usr/bin/env python

import httplib
import json

from flask import Flask, request, jsonify, make_response

config = {
    'serviceHost': '127.0.0.1:5001',
    'uri': 'feed',
    'petCount': 3,
    'portionSize': 20
}

app = Flask('Feeding service')


@app.route('/', methods=['GET'])
def main():
    return createResponse('Nutrition service is running')


def createResponse(message, status=200):
    return make_response(jsonify({
        'status': 'OK' if status == 200 else 'FAIL',
        'message': message
    }), status)


class FeederClient(object):
    def createRequestBody(self, slot, amount):
        return {
            'slot': slot,
            'amount': amount
        }

    def feedingRequest(self, slotNumber, amount):
        connection = httplib.HTTPConnection(config['serviceHost'])
        connection.request(
            'POST',
            config['uri'],
            json.dumps(self.createRequestBody(slotNumber, amount)),
            {'Content-Type': 'application/json'}
        )

        return connection.getresponse().status == 200


class BlindStrategy(object):
    def feed(self):
        slotDetector = SlotDetector()
        amountCalculator = AmountCalculator()
        feederClient = FeederClient()

        return feederClient.feedingRequest(slotDetector.getSlot(), amountCalculator.calculate())


class SlotDetector():
    def getSlot(self):
        return 1


class AmountCalculator():
    def calculate(self):
        return config['petCount'] * config['portionSize']


class RecognitionClient(object):
    def whoIsHungry(self):
        pass


class PetStrategy(object):
    def feed(self):
        recognitionClient = RecognitionClient()


class FeedingStrategyResolver(object):
    def resolve(self, json):
        if json.get('personally'):
            return PetStrategy()

        return BlindStrategy()


@app.route('/initiate_feeding', methods=['POST'])
def initiate():
    strategyResolver = FeedingStrategyResolver()
    strategy = strategyResolver.resolve(request.json)

    if (strategy.feed()):
        return createResponse('Start feeding')

    return createResponse('No feeding occured')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5002)
