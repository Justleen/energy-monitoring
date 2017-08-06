import minimalmodbus #rs485

def readRS485():
	''' read DSM120 powermeter over rs485 '''
		ret = {}
		try:
			Activepower =  rs485.read_float( 12, functioncode=4, numberOfRegisters=2)
			sleep(1)
			TotalPower =  rs485.read_float( 342, functioncode=4, numberOfRegisters=2)
		except IOError as err:
			print( 'Ooops, rs458 hickups %s' % err)
			pass
		else:
			ret['sol_pow'] = float(Activepower)
			ret['sol_nrg'] = float(TotalPower)
			postRS485( ret, stop_event ) 
		sleep(9)

def postRS485(values, ):
		# solar power / energy, pass if not both there
		bodyTemplate_solar = 'emeter_solar,eqid={eqid},type={type} value={value}\n'

		body  = bodyTemplate_solar.format(eqid=meterID,type='cumulative', value=values['sol_nrg'])
		body += bodyTemplate_solar.format(eqid=meterID,type='instant', value=values['sol_pow'])

		httpPost(body)
