import minimalmodbus #rs485

#init rs485 
rs485 = minimalmodbus.Instrument( '/dev/ttyUSB0', 1)
rs485.mode =  minimalmodbus.MODE_RTU
rs485.serial.parity =  minimalmodbus.serial.PARITY_NONE
#rs485.debug = Config.get('rs485', 'debug')
rs485.serial.baudrate = 9600
rs485.serial.bytesize = 8
rs485.serial.stopbits = 1
rs485.serial.timeout = 5



class rsReader(object):
	def readRS485(self):
		bodyTemplate_solar = 'emeter_solar,eqid={eqid},type={type} value={value}\n'
		''' read DSM120 powermeter over rs485 '''
		ret = {}
		try:
			Activepower =  rs485.read_float( 12, functioncode=4, numberOfRegisters=2)
			TotalPower =  rs485.read_float( 342, functioncode=4, numberOfRegisters=2)
		except IOError as err:
			print( 'Ooops, rs458 hickups %s' % err)
			pass
		else:
			ret['sol_pow'] = float(Activepower)
			ret['sol_nrg'] = float(TotalPower)


			self.body  = bodyTemplate_solar.format(eqid='E0005001501964013',type='cumulative', value=ret['sol_nrg'])
			self.body += bodyTemplate_solar.format(eqid='E0005001501964013',type='instant', value=ret['sol_pow'])

		return self.body
