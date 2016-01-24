import serial
ser = serial.Serial('/dev/ttyAMA0', 38400, timeout=1)
ser.close()
ser.open()
ser.write("light on\n")
try:
    while 1:
        response = ser.readline()
        print response
except KeyboardInterrupt:
    ser.close()
