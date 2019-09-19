import serial.tools.list_ports
import time
from pyfirmata import Arduino, util

LED_PIN_NUM = 13
ON = 1
OFF = 0

ports = list(serial.tools.list_ports.comports())

if len(ports) == 0:
    raise Exception("No ports found!")

print("\nAvailable USB ports:\n")
print("Port Number\tPort Name")

for idx, p in enumerate(ports):
    print(f"{idx}\t\t({p.device})")

port_num = int(input(f"Please enter the number for the Arduino port [0-{len(ports)-1}]: "))


print("\nConnecting to the Arduino...", end='')
board = Arduino(ports[port_num].device)
print("connected!\n")

light = board.get_pin(f'd:{LED_PIN_NUM}:o')

for n in range(4):
    light.write(ON)
    print(f"Light is: ON ", end="\r")
    
    time.sleep(1)
    
    light.write(OFF)
    print("Light is: OFF", end="\r")
    
    time.sleep(1)

print('\nDone!')
