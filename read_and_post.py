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

def postBodyCreate(packet, poster):
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

def main():
	while True:
		poster = post()
		try:
			packet = meter.read_one_packet()
			eqid = postBodyCreate(packet, poster)
		except P1PacketError:
			log.info('invalid checksum, pass')
			pass

		try:
			poster.httpsPost(solar.readRS485(eqid) )
		except influxPostError:
			log.info('influx posting went wrong')
			pass
		except EqidError:
			log.info('geen Equipment ID voor rs485')
			pass

if __name__ == "__main__":
   main()
