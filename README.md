# Code for Smart LED  

## Setup
SSH to the Raspberry Pi, and navigate to `~/rest-server/iot-smart-led`
If running for the first time, run `pip install -r requirements.txt` from the root folder

## Configuration
To control which pin the LED is connected to, set the environment variable to the correct number with `export LED_PIN=<pin number>`, and then start the server

## Starting the server
Run `./start.sh` from inside the root folder

## Testing the DB Code
Ensure that the DB is setup properly. See dbcommands.txt for reference. <br>
Uncomment the Flask code in DB dbconn.py. <br>

Run the test flask server through the command `FLASK_APP=dbconn.py python -m flask run` <br>
Make the API calls through POSTMAN or Curl: <br>
* curl http://localhost:5000/ - Get LEDs
* curl http://localhost:5000/on/0 - Switch On LED
* curl http://localhost:5000/off/0 - Switch Off LED
* curl http://localhost:5000/stats/0 - Get LED stats
