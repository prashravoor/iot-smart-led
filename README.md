# Smart LED  Implementation
This is an implementation of a Smart LED, which uses a Raspberry Pi3B+ to add "smartness" to the LED.

## Hardware
* Raspberry Pi 3B+
* 1 LED, optional Resistor, connected in series with the LED

## Features
* Remote Switch On / Off LED
* Scheduled Turn On
* Show past usage statistics

## Setup
SSH to the Raspberry Pi, and navigate to `~/rest-server/iot-smart-led`
If running for the first time, run `pip install -r requirements.txt` from the root folder<br>
Install mysql DB by running `sudo apt install mysql` <br>

## Configuration
To control which pin the LED is connected to, set the environment variable to the correct number with `export LED_PIN=<pin number>`, and then start the server. The default is pin 40<br>
Setup the MYSQL DB by running the commands specified in "dbcommands.txt" <br>
The Angular Server needs the IP address of the Pi to run properly. <br>
Modify the IP address to appropriate values in both the `environment.ts` and `environment.prod.ts` files under the `src/environments` folder. <br>

## Starting the server
Run `./start.sh` from inside the "python" folder to start the REST server. It starts on port 5000 <br>
Navigate the the `angular/smart-led` folder, and run `npm start`. The Angular Server is accessible from port 4200 <br>

## Loading the UI
The UI for the application is available by navigating to the `http://<IP addresss>:4200`. <br>

## Testing the DB Code
Ensure that the DB is setup properly. See dbcommands.txt for reference. <br>
Uncomment the Flask code in DB dbconn.py. <br>

Run the test flask server through the command `FLASK_APP=dbconn.py python -m flask run` <br>
Make the API calls through POSTMAN or Curl: <br>
* curl http://localhost:5000/ - Get LEDs
* curl http://localhost:5000/on/0 - Switch On LED
* curl http://localhost:5000/off/0 - Switch Off LED
* curl http://localhost:5000/stats/0 - Get LED stats
