# Code for Smart LED  

## Setup
SSH to the Raspberry Pi, and navigate to the correct location
If running for the first time, run `pip install -r requirements.txt` from the root folder

## Configuration
To control which pin the LED is connected to, set the environment variable to the correct number with `export LED_PIN=<pin number>`, and then start the server

## Starting the server
Run `./start.sh` from inside the `rest-server` folder
