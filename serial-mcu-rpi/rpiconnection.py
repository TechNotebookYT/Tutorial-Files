import os
import sys
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=5)

# listen for the input, exit if nothing received in timeout period
while True:
    line = str(ser.readline())
    if len(line) == 0:
        print("Time out! Exit.\n")
        sys.exit()
    # b'14Hello World\r\n'
    if "esp_start" in line:
        msg_start = line.index('esp_start')
        msg_end = line.index('esp_end')
        msg = line[msg_start+9:msg_end]
        print(msg)
