import serial.tools.list_ports
ports = list(serial.tools.list_ports.comports())

print("Available USB devices:")

for idx, p in enumerate(ports):
    print(idx, p.device)

port_num = int(input("Please enter a device number to connect to: "))

LED_PIN = 13

import time
from pyfirmata import Arduino, util
board = Arduino(ports[port_num].device)

for n in range(10):
    board.digital[LED_PIN].write(1)
    
    time.sleep(1)
    
    board.digital[LED_PIN].write(0)
    
    time.sleep(1)
