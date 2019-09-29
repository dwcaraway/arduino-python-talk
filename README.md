# arduino-python-talk
GMVCSC talk to middle and high school students on connecting arduino to python.

To have a high baud rate with our arduino, we'll use [pymata-express](https://github.com/MrYsLab/pymata-express).

To get started, you'll need to install [FirmataExpress](https://github.com/MrYsLab/FirmataExpress) on your arduino. Installation instructions [here](https://mryslab.github.io/pymata-express/firmata_express/)

Files
* joystick.py - the joystick control example, outputs values
* game.py - a simple app to show joystick control

Keys:
use directional arrows to move the ball
use `spacebar` to toggle leaving a trail after the ball. hold down `spacebar` to draw stripped lines.
use the `r` key to reset the screen.

To quit, simply close the window.

Joystick:
up/down/left/right moves the ball. Click the joystick to change to a random color, click again to revert to the default color.
