from flask import Flask
import RPi.GPIO as GPIO
import os
from flask import jsonify, Response, request
from dbconn import LedDatabase
from threading import Timer
import json

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# DB Configuration
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'smartled'
app.config['MYSQL_HOST'] = 'localhost'


ledCounter = 0
ledPinNo = os.getenv('LED_PIN', 40)

class Led(object):
    def __init__(self, pinNo, flaskApp):
        global ledCounter
        self.id = ledCounter
        ledCounter += 1
        self.pinNo = pinNo
        self.value = 0
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pinNo, GPIO.OUT)
        self.led_db = LedDatabase(flaskApp)

    def __del(self):
        self.value = 0
        GPIO.cleanup()

    def getDict(self):
        return { "id": str(self.id), "state": self.getState() }

    def update(self):
        GPIO.output(self.pinNo, self.value)

    def on(self):
        self.value = 1
        self.update()
        self.led_db.switched_on(self.id)
    
    def off(self):
        self.value = 0
        self.update()
        self.led_db.switched_off(self.id)

    def isOn(self):
        return self.value == 1

    def getState(self):
        if self.isOn():
            return "On"

        return "Off"

    def get_stats(self):
        return self.led_db.get_stats_for_led(self.id)

with app.app_context():
    led = Led(ledPinNo, app)

@app.route('/lights', methods=['GET'])
def get_lights():
    return jsonify([str(led.id)])


@app.route('/lights/<id>', methods=['GET', 'PUT'])
def get_or_modify_light(id):
    if not int(id) == led.id:
        return Response("{'error' : 'Not Found'}", status=404, mimetype='application/json')

    if 'GET' == request.method:
        return jsonify(led.getDict())
    else:
        req = request.get_json()
        swOnAfter = -1
        swOffAfter = -1
        if 'switchOnAfter' in req:
            swOnAfter = req['switchOnAfter']
        if 'switchOffAfter' in req:
            swOffAfter = req['switchOffAfter']

        if swOnAfter == 0 and not led.isOn():
            led.on()
        elif swOffAfter == 0 and led.isOn():
            print("Turning off LED")
            led.off()
        elif swOnAfter < 0 and swOffAfter < 0:
            return Response('{ "error": "At least one modification expected" }', status=400, mimetype='application/json')
        else:
            if swOnAfter > 0:
                print("Setting timer to Switch On Lamp after {} seconds".format(swOnAfter))
                Timer(swOnAfter, led.on, ()).start()
            if swOffAfter > 0:
                print("Setting timer to Switch Off Lamp after {} seconds".format(swOffAfter))
                Timer(swOffAfter, led.off, ()).start()

        return Response(str(led.getDict()), status=200, mimetype='application/json')


@app.route('/lights/<id>/stats', methods=['GET'])
def get_stats(id):
    if not int(id) == led.id:
        return Response("{'error' : 'Not Found'}", status=404, mimetype='application/json')

    return Response(json.dumps(led.get_stats()), status=200, mimetype='application/json')

