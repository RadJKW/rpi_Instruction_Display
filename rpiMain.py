"""This program will do the following: 
    1: Start GUI on raspberry pi
    2: Run a startup check and output the status 
       report on a console.
    3: Selenium
      - Start Chrome to URL
    4: PySerial
      -Check if serial can open
      -open serial port
          • flush input buffer
          • flush output buffer
      -wait for serial input
      -receive serial input
      -close serial port
      -store serial input to a list
    5: PySQL
      -send UART received list to SQL
      -request linked URL
      -check if URL received
    6: Selenium
      -Open PySQL URL on chrome
    7: Repeat @step #4
    """
# %%
from os import path
import pytds
from pytds import Error

import time
import serial

import pygetwindow as gw
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from serial import SerialException

division = None
stopType = None


def open_webpage(url):
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    #driver = webdriver.Chrome(options=options, executable_path=r'/usr/bin/chromedriver')
    driver = webdriver.Chrome(
        options=options,
        executable_path=r'.\chromeDriver\chromedriver.exe'
    )
    driver.get('{}'.format(url))

    chromeWindow = gw.getWindowsWithTitle('Winding Practices - Google Chrome')
    if chromeWindow != []:
        try:
            chromeWindow[0].activate()
        except:
            chromeWindow[0].minimize()
            chromeWindow[0].maximize()
    pass


def uart_connect(dict):
    """[summary]

    Args:
        dict ([type]): [description]

    Returns:
        [type]: [description]
    """
    ser = serial.Serial()
    ser.port = dict['port']
    ser.baudrate = dict['baudrate']
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.bytesize = serial.EIGHTBITS
    ser.timeout = 1
    return ser


def uart_request(uart_conn):
    """[summary]

    Args:
        uart_conn ([type]): [description]

    Returns:
        [type]: [description]
    """
    global division
    global stopType
    try:
        uart_conn.close()
        time.sleep(0.5)
        uart_conn.open()
    except Exception as e:
        print("error opening serail port " +
              str(uart_conn.port) + " : " + str(e))
        exit()

    if uart_conn.isOpen():
        try:
            # flush input buffer, discarding contents
            uart_conn.flushInput()
            # give serial port sometime to receive the data
            print("Acquiring UART DATA.....")
            time.sleep(0.5)
            # retrieve input data
            while True:
                rx_data = uart_conn.readline()
                utf8_data = rx_data.decode('utf8')

                if(len(utf8_data) >= 2):
                    print(utf8_data)
                    str1, str2 = utf8_data.split()
                    division = str1
                    stopType = str2
                    uart_conn.close()
                    return True
        # hand port not open exception, print error
        except Exception as e1:
            print("error communicating...: " + str(e1))
    else:
        print("Cannot open Serial port " + str(uart_conn.port))


def sql_connect(dict):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = pytds.connect(dict['server'],
                             dict['database'],
                             dict['user'],
                             dict['password'])

    except Error as e:
        print(e)
        print(dict['password'])

    return conn


def sql_close(cnxn):
    """[summary]

    Args:
        cnxn ([type]): [description]
    """

    try:
        cnxn.close()
    except Error as e:
        print(e)
    return


def sql_request(sql_conn, str1, str2):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cursor = sql_conn.cursor()
    cursor.execute("""
                  select URL
                  from StopURLLookUP
                  where Division = '{}'
                  and StopType = '{}'
                  """.format(str1, str2))
    row = cursor.fetchone()
    sql_data = row[0]
    print(row[0])

    return sql_data


def main():
    """[summary]
    """
    # define sql database connection
    sql_cnxn_Dict = {
        'server': 'RAD-SQL',
        'database': 'CoilWinderStops',
        'user': 'CoilStops',
        'password': 'Temp12345678'
    }
    # define serial parameters
    uart_cnxn_Dict = {
        # windows USB - serial port = 'COM3'
        # rpi USB - serial port = /dev/ttyUSB0"
        'port': 'COM4',
        'baudrate': 9600
    }
    # create a uart serial connection
    uart_cnxn = uart_connect(uart_cnxn_Dict)
    with uart_cnxn:
        print("ATTEMPTING UART REQUEST")
        uart_request(uart_cnxn)
        print("Division: {} \nStopType: {}".format(division, stopType))

    # create a sql database connection
    sql_cnxn = sql_connect(sql_cnxn_Dict)

    with sql_cnxn:
        print("REQUESTING URL FOR {} -> {}".format(division, stopType))
        url_rx = sql_request(sql_cnxn, division, stopType)
        url_path = ('http://svr-webint1/WindingPractices')
        print(url_path)
    sql_close(sql_cnxn)

    open_webpage(url_path)


if __name__ == '__main__':
    main()


# %%
