import time
import sys
import serial
from eventlet import api

class kitelight:
    m_serialPort = ""
    
    def __init__(self, serial_port):
        self.m_serialPort = serial.Serial(serial_port, 115200)
        return

    def connect(self):
        self.m_serialPort.open()
        return

    def disconnect(self):
        self.m_serialPort.close()

    def setSpeed(self, index, speed):
        command = "{%d,%d}" % (index, speed)
        self.m_serialPort.write(command)
        time.sleep(.001)

    def resetCommunication(self):
        self.setSpeed(0xff, 0xff);
        return 

s = kitelight('/dev/ttyUSB0')

def handle_socket(reader, writer):
    while True:
        # print "connect!"
        # pass through every non-eof line
        x = reader.readline()
        if not x: break
        print x
        s.setSpeed(int(x.split(' ')[0]), int(x.split(' ')[1]))

def main(argv=None):
    if argv is None:
        argv = sys.argv
    s.connect()
    time.sleep(3)
    for i in range(0, 255):
        s.setSpeed(4, i)
        time.sleep(.005)
    for i in range(255, 0, -1):
        s.setSpeed(4, i)
        time.sleep(.005)
    
    server = api.tcp_listener(('localhost', 9000))
    while True:
        try:
            new_sock, address = server.accept()
        except KeyboardInterrupt:
            break
        # handle every new connection with a new coroutine
        api.spawn(handle_socket, new_sock.makefile('r'), new_sock.makefile('w'))
    s.disconnect()
    return 0

if __name__ == "__main__":
    sys.exit(main())




