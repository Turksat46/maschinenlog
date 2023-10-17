import serial

s = serial.Serial()

# Kommunikationsparameter
s.port = '/dev/ttyUSB0'
s.baudrate = 9600
s.bytesize = 8
s.stopbits = serial.STOPBITS_ONE
s.parity = serial.PARITY_NONE
s.rts = True
s.dtr = True

s.timeout = None

print(s.timeout)
print(s.parity)

# Oeffne Kommunikation 
s.open()

# gib den Namen des Ports aus 
print(s.name)

# checkt ob Kommunikation offen ist 
print(s.is_open) 

test = []

if(s.isOpen()):
    xy = ("SET\n\r").encode('utf-8')
    s.write(xy)
    s.write(("123\n\r").encode('utf-8'))
    while(1):
        serial_line = s.readline().decode("utf-8")
        print(serial_line)
        test.append(serial_line)
  
    file = open("CAB690.txt", "w")
    file.write(str(test))
    file.close()
    s.close()
else:
    print("Cannot open serial port")