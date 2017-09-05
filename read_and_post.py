from smeterd.meter import SmartMeter,P1PacketError
from influx.influxpost import post, influxPostError
from rs485.rs485 import rsReader,EqidError

import logging 
import sys,getopt
import ConfigParser

#config
Config = ConfigParser.ConfigParser()
Config.read('config.ini')

#logging
numeric_level = getattr(logging, Config.get('logging', 'level').upper(), 10) #convert log level to numeric loglevel
logging.basicConfig(level=numeric_level)
log = logging.getLogger(__name__)
log.info('Starting..')


meter = SmartMeter( Config.get('smeter', 'device'), baudrate = Config.get('smeter', 'baudrate') )

solar = rsReader(
					 **dict(Config.items('rs485'))
				)

def p1PostPacket(packet, poster):
	eqid = str(packet['kwh']['eid']).decode('hex')
	tariff = packet['kwh']['tariff']

	body=''
	bodyTemplate_energy = 'emeter_energy,eqid='+ eqid +',tarif={tarif},direction={dir} value={value}\n'
	bodyTemplate_power = 'emeter_power,eqid='+ eqid +',tarif={tarif},direction={dir},phase={phase} value={value}\n'

	body += bodyTemplate_energy.format( dir='in', tarif='2', value=packet['kwh']['high']['consumed'] )
	body += bodyTemplate_energy.format( dir='out', tarif='2', value=packet['kwh']['high']['produced'] )
	body += bodyTemplate_energy.format( dir='in', tarif='1', value=packet['kwh']['low']['consumed'] )
	body += bodyTemplate_energy.format( dir='out', tarif='1', value=packet['kwh']['low']['produced'] )

	body += bodyTemplate_power.format( dir='in', tarif=tariff, phase='L1', value=packet['kwh']['current_consumed_phaseOne'] )
	body += bodyTemplate_power.format( dir='in', tarif=tariff, phase='L2', value=packet['kwh']['current_consumed_phaseTwo'] )
	body += bodyTemplate_power.format( dir='in', tarif=tariff, phase='L3', value=packet['kwh']['current_consumed_phaseThree'] )
	body += bodyTemplate_power.format( dir='in', tarif=tariff, phase='total', value=packet['kwh']['current_consumed'] )

	body += bodyTemplate_power.format( dir='out', tarif=tariff, phase='L1', value=packet['kwh']['current_produced_phaseOne'] )
	body += bodyTemplate_power.format( dir='out', tarif=tariff, phase='L2', value=packet['kwh']['current_produced_phaseTwo'] )
	body += bodyTemplate_power.format( dir='out', tarif=tariff, phase='L3', value=packet['kwh']['current_produced_phaseThree'] )
	body += bodyTemplate_power.format( dir='out', tarif=tariff, phase='total', value=packet['kwh']['current_produced'] )
	
	poster.httpsPost(body)

	return eqid

def solarPostPacket(packet, poster, eqid):
	bodyTemplate_solar = 'emeter_solar,eqid={eqid},type={type} value={value}\n'
	body = ''
	if packet['sol_pow'] and packet['sol_nrg']:
		log.debug('Solar values read: %s and %s',  packet['sol_pow'] , packet['sol_nrg'] ) 
		body  = bodyTemplate_solar.format(eqid=eqid,type='cumulative', value=packet['sol_nrg'])
		body += bodyTemplate_solar.format(eqid=eqid,type='instant', value=packet['sol_pow'])

		poster.httpsPost(body)
	else:
		log.info('Niet alle waarden van Solar! Skipping')

def main():
	global eqid
	while True:
		poster = post()

		try:
			smeter_packet = meter.read_one_packet()
			eqid = p1PostPacket(smeter_packet, poster)


		except P1PacketError:
			log.info('invalid checksum, pass')
			pass


		try:
			solar_packet =  solar.readRS485(eqid)
			solarPostPacket(solar_packet, poster, eqid)

		except influxPostError:
			log.info('influx posting went wrong')
			pass
		except EqidError:
			log.info('geen Equipment ID voor rs485')
			pass
		except IOE

if __name__ == "__main__":
   main()
