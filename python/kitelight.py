import time
import sys
import serial
from eventlet import api

class kitelight:
    m_serialPort = ""
    
    def __init__(self, serial_port):
        self.m_serialPort = serial.Serial(serial_port, 9600)
        return

    def connect(self):
        self.m_serialPort.open()
        return

    def disconnect(self):
        self.m_serialPort.close()

    def setSpeed(self, index, speed):
        command = ''.join([chr(index), chr(speed), chr(0)])
        self.m_serialPort.write(command)
        time.sleep(.001)
    def resetCommunication(self):
        self.setSpeed(0xff, 0xff);
        return 

s = kitelight('/dev/tty.usbserial-A70062Nn')

def handle_socket(reader, writer):
    while True:
        print "connect!"
        # pass through every non-eof line
        x = reader.readline()
        if not x: break
        print x
        s.setSpeed(int(x.split(' ')[0]), int(x.split(' ')[1]))

def main(argv=None):
    if argv is None:
        argv = sys.argv
#    s.resetCommunication()
#    for i in range(0, 255):
#        s.setSpeed(4, i)
#        time.sleep(.10)
#    s.resetCommunication()

    s.connect()
    time.sleep(3)
    server = api.tcp_listener(('192.168.123.20', 9000))
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




