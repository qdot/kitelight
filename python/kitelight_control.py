import time
import socket
import sys

def main(argv=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( ('192.168.123.20', 9000) )
#    for i in range(0, 255):
    sock.send(sys.argv[1] + " " + sys.argv[2] + "\n")
    #    sock.send("%s %s \r\n" % (sys.argv[1], str(i)))
#        time.sleep(.1)
    sock.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())




