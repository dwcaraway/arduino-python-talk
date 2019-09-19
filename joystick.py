import serial.tools.list_ports
from pyfirmata import Arduino, util
import time

# Constants
SW_PIN = 2  # Switch digital output
X_PIN = 0  # X analog output
Y_PIN = 1  # X analog output

ports = list(serial.tools.list_ports.comports())

if len(ports) == 0:
    raise Exception("No ports found!")

print("\nAvailable USB ports:\n")
print("Port Number\tPort Name")

for idx, p in enumerate(ports):
    print(f"{idx}\t\t({p.device})")

port_num = int(input(f"Please enter the number for the Arduino port \
        [0-{len(ports)-1}]: "))

print("\nConnecting to the Arduino...", end='')
board = Arduino(ports[port_num].device)
print("connected!\n")

# Setup
it = util.Iterator(board)
it.start()

board.digital[SW_PIN].write(1)

switch_in = board.get_pin(f'd:{SW_PIN}:i')
x_axis_in = board.get_pin(f'a:{X_PIN}:i')
y_axis_in = board.get_pin(f'a:{Y_PIN}:i')

x_axis_in.enable_reporting()
y_axis_in.enable_reporting()
switch_in.enable_reporting()


while True:
    print(f"X-axis: {x_axis_in.read()}\tY-axis: {y_axis_in.read()}\t\
            Switch: {switch_in.read()}", end='\r')

    time.sleep(0.2)
    # clear the line
    print(80*" ", end='\r')

print('\nDone!')
