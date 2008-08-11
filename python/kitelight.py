import time
import sys
import serial

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
        return
    
    def resetCommunication(self):
        self.setSpeed(0xff, 0xff);
        return 

def main(argv=None):
    if argv is None:
        argv = sys.argv

    return 0

if __name__ == "__main__":
    s = kitelight('/dev/tty.usbserial-000052FD')
    s.connect()
    for i in range(0, 255):
        s.setSpeed(4, i)
        time.sleep(.010)
    s.resetCommunication()
    sys.exit(main())




