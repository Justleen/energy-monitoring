#!/usr/bin/env python
from datetime import datetime
from time import sleep
import crcmod
import serial, sys, re

class P1():
	def __init__():
		self.crc16 = crcmod.predefined.mkPredefinedCrcFun('crc16')
		self.ser          = serial.Serial()
		self.ser.baudrate = 115200
		self.ser.timeout  = 8
		self.ser.port     = '/dev/ttyUSB0'
		self.ser.open()
        self.telegram = ''
        self checksum_found = False
        self.good_checksum =  False
	def readTelegram():
        while not checksum_found:
                # Read in a line
                telegram_line = ser.readline()

                # Check if it matches the start line (/ at start)
                if telegram_line[0] == "/":
                        self.telegram += telegram_line
                        print('Found start!')
                        if  not self.checksum_found:
                                telegram_line = ser.readline()
                                # Check if it matches the checksum line (! at start)
                                if telegram_line[0] == "!":
                                        self.telegram += telegram_line
                                        print('Found checksum!')
                                        self.checksum_found = True
                                else:
                                        self.telegram += telegram_line


	def checkCRC():
        for m in pattern.finditer(self.telegram):
                # Remove the exclamation mark from the checksum,
                # and make an integer out of it.
                given_checksum = int('0x' + self.telegram[m.end() + 1:].decode('ascii'), 16)
                # The exclamation mark is also part of the text to be CRC16'd
                calculated_checksum = crc16(self.telegram[:m.end() + 1])
                if given_checksum == calculated_checksum:
                        self.good_checksum = True
                if self.good_checksum:
                        print("Good checksum!")
                else:
                        print("No Good, next!")
	#def postP1():

	def tijdomvormer(timestamp):
		year	= '20' + timestamp[0:2]
		month	= timestamp[2:4]
		day		= timestamp[4:6]
		hour	= timestamp[6:8] 
		minutes	= timestamp[8:10]
		seconds	= timestamp[10:12] 
		return datetime(*map(int,( year, month, day, hour, minutes, seconds ) )).strftime('%s')  # epoch	


def main():
	P1tele  =   P1()

	P1tele.readTelegram()
	P1tele.checkCRC()


if __name__ == '__main__': 
	main()
