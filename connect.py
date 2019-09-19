import serial.tools.list_ports
import time
from pyfirmata import Arduino, util

ports = list(serial.tools.list_ports.comports())

if len(ports) == 0:
    raise Exception("No ports found!")

print("\nAvailable USB ports:\n")
print("Port Number\tPort Name")

for idx, p in enumerate(ports):
    print(f"{idx}\t\t({p.device})")

port_num = int(input(f"Please enter the number for the Arduino port [0-{len(ports)-1}]: "))

LED_PIN = 13

print("\nConnecting to the Arduino...")

board = Arduino(ports[port_num].device)

print("Connected!\n")

for n in range(4):
    board.digital[LED_PIN].write(1)
    print(f"Light is: ON ", end="\r")
    
    time.sleep(1)
    
    board.digital[LED_PIN].write(0)
    print("Light is: OFF", end="\r")
    
    time.sleep(1)

print('\nDone!')
