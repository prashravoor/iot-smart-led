from flask import Flask
import RPi.GPIO as GPIO
import os
from flask import jsonify, Response, request

app = Flask(__name__)

ledCounter = 0
ledPinNo = os.getenv('LED_PIN', 40)

class Led(object):
    def __init__(self, pinNo):
        global ledCounter
        self.id = ledCounter
        ledCounter += 1
        self.pinNo = pinNo
        self.value = 0
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pinNo, GPIO.OUT)

    def __del(self):
        self.value = 0
        GPIO.cleanup()

    def getDict(self):
        return { "id": self.id, "state": self.getState() }

    def update(self):
        GPIO.output(self.pinNo, self.value)

    def on(self):
        self.value = 1
        self.update()
    
    def off(self):
        self.value = 0
        self.update()

    def isOn(self):
        return self.value == 1

    def getState(self):
        if self.isOn():
            return "On"

        return "Off"

led = Led(ledPinNo)

@app.route('/lights', methods=['GET'])
def get_lights():
    return jsonify(led.getDict())


@app.route('/lights/<id>', methods=['GET', 'PUT'])
def get_or_modify_light(id):
    if not int(id) == led.id:
        return Response("{'error' : 'Not Found'}", status=404, mimetype='application/json')

    if 'GET' == request.method:
        return jsonify(led.getDict())
    else:
        # Toggle LED
        if led.isOn():
            led.off()
        else:
            led.on()
        return Response(str(led.getDict()), status=200, mimetype='application/json')



