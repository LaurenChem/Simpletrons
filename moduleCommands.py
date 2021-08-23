######################################################################
# Please Do NOT Modify Unless You Know What you're doing #

######################################################################
import opentrons
# Opentrons 2.5.2 (pip install opentrons==2.5.2)
from opentrons import robot, containers, instruments

from modulePipetting import *
from moduleCalibrate import *
#from moduleTransportation import getTransportposition
from time import sleep

import sqlite3
from sqlite3 import Error

import warnings
import serial
import serial.tools.list_ports
import re
######################################################################

# Self Find Serial Port #
def find_arduino(serial_number):
    for pinfo in serial.tools.list_ports.comports():
        if pinfo.serial_number == serial_number:
            return serial.Serial(pinfo.device)
    raise IOError("[#A1] Could not find an Robot - is it plugged in or is serial number setup correct?")

def check_file():
    try:
        with open('usbSerial.txt') as f:
            lines = f.readlines() #Read UsbSerial file
            lines = [line.replace(' ', '') for line in lines] #Remove Empty Spaces
        return lines
    except:
        return lines
        print('[#A7] Error reading usbSerial text file, please double check the file exist and value is entered within the brackets')
        pass

    

def find_ot():
    try:
        # Run 'python3 tools/toolScanner.py' to obtain serial number for your printer
        serial = check_file()
        print(serial)
        #robotUSB = find_arduino(serial_number='05012004AEFC104858093B9CF50020C3') #Configurable Serial
        robotUSB = find_arduino(serial) #Configurable Serial
        robotUSB = str(robotUSB) #Array to Convert to string
        robotUSB = re.findall(r"port='(.*?)'", robotUSB)
        robotUSB = str(robotUSB) #Array to Convert to string
        robotUSB = str(robotUSB).strip('['']') #Remove Brackets 
        robotUSB = eval(robotUSB) #Remove Quotation
    except:
        print('[#A2] Error Phrasing serial number, please submit issue on github')
        pass

    #print(robotUSB)

#######################################################################

#Connect To both Robot
def connect():
    print('Connecting to Robots')
    try:
        find_ot()
        robot.connect(robotUSB)
        versions = robot.versions()
        print('Opentrons Robot Connected, Robot Firmware Version:', versions)
        #robot2.connect()
        #robot2.connect(robot2USB)
        #print('Opentrons Robot Connected')
    except:
        print('Opentrons Robot Not Connected')
        print('[#A3] Running Debugging Mode')

def home_all():
    try:
        print('Homing Opentrons Robot in progress')
        robot.home()
        print('Successfully Homed Opentrons Robot Complete')
        try: 
            #Home Robot 2
            robot2._driver.send_command('G28.2 Y Z')
            robot2._driver.send_command('G28.2 A')
            robot2._driver.send_command('G28.2 B')
            robot2._driver.send_command('G28.2 X')
            robot2._driver.send_command('G90')
            print('Successfully Homed Transport Robot')
        except:
            print('[#A4] Robot 2 Not Loaded')
            pass
    except: 
        print('[#A5] Running Debugging Mode')
        pass

#Homes All Axis For Opentrons Robot
def home_robot():
    try:
        print('Homing Opentrons Robot in progress')
        robot.home()
        print('Successfully Homed Opentrons Robot Complete')
    except: 
        print('[#A6] Running Debugging Mode')
        print('[#H1] Unable to Home Robot')
        pass

#Homes All Axis For Transport Robot
def home_robot2():
    try:
        print('Homing Transport Robot in progress')
        robot2._driver.send_command('G28.2 Y Z')
        robot2._driver.send_command('G28.2 A')
        robot2._driver.send_command('G28.2 B')
        robot2._driver.send_command('G28.2 X')
        robot2._driver.send_command('G90')
        print('Successfully Homed Transport Robot')
    except: 
        print('[#A5] Note: Running Debugging Mode')
        print('[#H2] Unable to Home Robot2')
        pass

#Reset Connection
def reset_all():
    try:
        #Reset Robot Opentron Robot
        print('Reseting Opentrons Robot')
        robot.reset()
        print('Successfully Rested Opentrons Robot')
        try: 
            #ResetRobot 2(Transport Platforms)
            print('Reseting Transport Robot')
            robot2.reset()
            print('Successfully Rested Opentrons Robot')
        except:
            print('[#A5] Note: Running Debugging Mode')
            print('[#H2] Unable to Home Robot2')
            pass
    except:
        print('[#A5] Note: Running Debugging Mode')
        print('[#H2] Unable to Home Robot2')
        pass
    
def load_calibration():
    print('Loaded Pre-Configured Robot Calibration')


##################################################################
# Database
# Test Connection
db_file = 'database/data.db'
def create_connection():
    """ create a test database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        print('Datbase Found')
    except Error as e:
        print(e)
        print('[#A7] Error Loading Database')
    finally:
        if conn:
            conn.close()

def create_table(conn, create_table_sql):
    # create a table from the create_table_sql statement
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            con.close()

#Delete A Single Record
def deleteRecord(variable, id):
    try:
        c = conn.cursor()
        print("Connected to SQLite")

        # Deleting Whole Table Values
        if variable == "custom_container":
            sql_delete_query = """DELETE FROM custom_container WHERE id=?;"""

        if variable == "custom_workspace":
            sql_delete_query = """DELETE FROM custom_workspace WHERE id=?;"""

        if variable == "custom_protocol":
            sql_delete_query = """DELETE FROM custom_protocol WHERE id=?;"""

        c.execute(sql_delete_query)
        conn.commit()
        print("Record deleted successfully ")
        conn.close()

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("the sqlite connection is closed")

#Delete Whole Table
def deleteTable(variable):
    try:
        c = conn.cursor()
        print("Connected to SQLite")

        # Deleting Whole Table Values
        if variable == "custom_container":
            sql_delete_query = """DELETE FROM custom_container;"""

        if variable == "custom_workspace":
            sql_delete_query = """DELETE FROM custom_workspace;"""

        if variable == "custom_protocol":
            sql_delete_query = """DELETE FROM custom_protocol;"""

        c.execute(sql_delete_query)
        conn.commit()
        print("Record deleted successfully ")
        conn.close()

    except sqlite3.Error as error:
        print("Failed to delete whole table from sqlite", error)
    finally:
        if conn:
            conn.close()
            print("the sqlite connection is closed")


#Save Data to specific database
def save_data(table, insert):

    if table == "custom_container":
        sql_insert_template = ''' INSERT INTO custom_container(id,name,grid_c,grid_r,spacing_c,diameter,depth)
            VALUES(?,?,?,?,?,?,?) '''

    if table == "custom_workspace":
        sql_insert_template = ''' INSERT INTO custom_workspace(id,name,grid_c,container,location,)
            VALUES(?,?,?,?,?) '''        

    if table == "custom_protocol":
        sql_insert_template = ''' INSERT INTO custom_protocol(id,grid_c,shortcuts,pipette, volume,value1,value2,value3,value4,notes)
            VALUES(?,?,?,?,?,?,?,?,?,?) '''

    #Excute Task to Database
    c.execute(sql_insert_template, insert)
    conn.commit()
    print("Record Added successfully to", table)
    conn.close()  



# #Read Data
# def read_data(table):
#     conn = sqlite3.connect(db_file)
#     c = conn.cursor()

#     #Read Number of rows
#     if table == "custom_container":
#         cursor_obj.execute("SELECT * FROM custom_container")
#     if table == "custom_workspace":
#         cursor_obj.execute("SELECT * FROM custom_workspace")
#     if table == "custom_protocol":
#         cursor_obj.execute("SELECT * FROM custom_protocol")

#     x = len(cursor_obj.fetchall())
#     print(x)

#     for x 

#     #Close Database Connection
#     conn.close()  
#     return list



#Setup New Table if none exist in DB File
def setup_table(variable):

    #Custom container Database Creation
    if variable == "custom_container":
        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS custom_container (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            grid_c REAL,
                                            grid_r REAL,
                                            spacing_c REAL,
                                            diameter REAL,
                                            depth REAL
                                        ); """

    #Custom workspace Database Creation
    if variable == "custom_workspace":
        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS custom_workspace (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            container text,
                                            location text,
                                        ); """

    #Custom protocol Database Creation
    if variable == "custom_protocol":
        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS custom_protocol (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            shortcuts text,
                                            pipette text,
                                            volume REAL,
                                            value1 text,
                                            value2 text,
                                            value3 text,
                                            value4 text,
                                            option text
                                            notes text,
                                        ); """

    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)

    else:
        print("Error! cannot create the database connection.")



###########################################################################################################
#
# Robot Move Commands
#
###########################################################################################################
