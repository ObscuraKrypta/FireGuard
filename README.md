# FireGuard: Intelligent Fire Prevention System for Eddy Current Separator Conveyor
FireGuard is an intelligent fire prevention system designed to monitor and monitor the temperature of Eddy Current Separator conveyors in real time. These devices, which are usually used in the recycling industry to separate non-ferrous metals such as aluminum and copper from other materials, are subject to fire hazards; Especially when ferromagnetic materials such as iron are mistakenly introduced into the system.
Using an MLX90640 thermal camera mounted on the conveyor belt, the FireGuard project continuously measures and analyzes the temperature of the conveyor belt. If an abnormal temperature (over 40°C) is detected, the system immediately sends alerts to technicians via Telegram messenger. This alert includes a text message along with an image of the conveyor belt with temperature data so that the technician can remotely view the system status and take timely action.
# Prerequisites
Before running this script, ensure you have the following hardware and software:

# Hardware
- Raspberry Pi (with GPIO capabilities)
- MLX90640 Thermal Camera
- Internet connection
- MQ-135 smoke sensor
- Buzzer
- 


## Software

- Python 3.x
- Required Python libraries:
  - opencv-python for image processing
  - numpy for numerical operations
  - RPi.GPIO for controlling GPIO pins on Raspberry Pi
  - Adafruit CircuitPython MLX90640
  - Python Telegram Bot
  - board busio
 
# Note:
- To send alerts, you need to create a bot in Telegram. Get a token for a bot through BotFather on Telegram.
- Chat IDs of users receiving alerts (including yourself) are also required.
Good luck with creating the bot :) 

## Installation
Install the required Python libraries using pip:

```sh
pip install opencv-python numpy RPi.GPIO pygame
pip install adafruit-circuitpython-mlx90640
pip install python-telegram-bot
pip install board busio
```
## How to install and run the project
# 1-Connecting thermal camera MLX90640
Connect the MLX90640 thermal camera to the Raspberry Pi's I2C pins:
- 3.3v -> VCC
- GND  -> GND
- SDA -> Pin 3
- SCL  -> Pin 5

# 2-Buzzer connection:

Connect the pins of the buzzer to a relay so you can control it through the Raspberry Pi.

# 3- Smoke sensor connection (MQ-135):
Connect the smoke sensor pins to the GPIO pins.

## Software installation and configuration
1- Install Python and required libraries
```sh
sudo apt install python3 python3-pip -y
```
2- Install Python libraries:
```sh
pip3 install opencv-python numpy adafruit-circuitpython-mlx90640 python-telegram-bot board busio
```
3- Configure Telegram Bot
- Find BotFather in your Telegram and create a new Bot.
- Please note the API token you received from BotFather and donot forget and share this API token with anybody.

4- Receive the Chat ID
After receiving your Chat ID, replace the information in below...
```sh
bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'
chat_id = 'YOUR_CHAT_ID'
```
5- I2C configuration for MLX90640
- Install Adafruit library for MLX90640
- Checking the I2C connection
```sh
i2cdetect -y 1
```
Note: You should see the I2C address of the camera (usually 0x33).
6- Run the file -> FireGuard_.py
