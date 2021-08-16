
#!/home/pi/Python-Dev/env/bin/python3
import os
import subprocess
import time
from datetime import datetime
import serial
from pathlib import Path
from codecs import encode


def activateUart(filename):
    ser = serial.Serial()
    ser.port = '/dev/ttyUSB0'
    ser.baudrate = 19200
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.bytesize = serial.EIGHTBITS
    ser.timeout = 1
    ser.exclusive = True
    ser.close()

    try:
        ser.open()
    except Exception as e:
        with (open(filename, "a")) as fw1:
            fw1.write(str(e) + '<\n')
            fw1.close()
        print("Error: Serial Open " + str(e))
        return()

    ser.reset_input_buffer()

    while True:
        rx_data = ser.readline()

        utf8_data = rx_data.decode('utf8', 'ignore')
        #hex_data = rx_data.hex()

        if(len(utf8_data) > 1):
            with (open(filename, "a")) as fw2:
                currentTime = datetime.today()
                # fw2.write(currentTime.strftime(
                #    '%H:%M:%S') + '>' + hex_data + '<\n')
                fw2.write(currentTime.strftime(
                    '%H:%M:%S') + '>' + utf8_data + '<\n')
                fw2.close()
            print(utf8_data + '<')


def openFile():
    # define file path/name.txt
    filePath = Path('/home/pi/Desktop/Z80Uart.txt')
    # If file does not exits, create it
    filePath.touch(exist_ok=True)

    with (open(filePath, "a")) as fw0:
        fw0.write('----------------------------------')
        fw0.write(datetime.today().strftime('%Y-%m-%d' + "," '%H:%M:%S'))
        fw0.write('----------------------------------'+'\n')
        fw0.close()
    print('Script Started: ' + datetime.today().strftime('%Y-%m-%d' + "," '%H:%M:%S'))

    return filePath


def errorLogToFile(errorMessage):
    elogPath = Path('/home/pi/Python-Dev/ErrorLogs/UartLoggerErrors.txt')
    elogPath.touch(exists_ok=True)

    with (open(elogPath, "a")) as elog:
        elog.write(datetime.today().strftime('%Y-%m-%d' + "," '%H:%M:%S'))
        elog.write(': >' + str(errorMessage) + '<\n')
        elog.close()
    print(datetime.today().strftime('%Y-%m-%d' + "," '%H:%M:%S'))
    print(': >' + str(errorMessage) + '<\n')

    main()


def main():
    try:
        logToFile = openFile()
        activateUart(logToFile)
    except Exception as e:
        errorLogToFile(e)


if __name__ == '__main__':
    main()
