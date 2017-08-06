from smeterd.meter import SmartMeter
meter = SmartMeter('/dev/ttyAMA0', baudrate=115200)
packet = meter.read_one_packet()
print packet['kwh']['etime']
'''
        packet['header'] = self.get(b'^\s*(/.*)\r\n')

        packet['kwh'] = {}
        packet['kwh']['eid'] = self.get(b'^0-0:96\.1\.1\(([^)]+)\)\r\n')

        packet['kwh']['tariff'] = self.get_int(b'^0-0:96\.14\.0\(([0-9]+)\)\r\n')
        packet['kwh']['switch'] = self.get_int(b'^0-0:96\.3\.10\((\d)\)\r\n')
        packet['kwh']['treshold'] = self.get_float(b'^0-0:17\.0\.0\(([0-9]{4}\.[0-9]{2})\*kW\)\r\n')

        packet['kwh']['low'] = {}
        packet['kwh']['low']['consumed'] = self.get_float(b'^1-0:1\.8\.1\(([0-9]+\.[0-9]+)\*kWh\)\r\n')
        packet['kwh']['low']['produced'] = self.get_float(b'^1-0:2\.8\.1\(([0-9]+\.[0-9]+)\*kWh\)\r\n')

        packet['kwh']['high'] = {}
        packet['kwh']['high']['consumed'] = self.get_float(b'^1-0:1\.8\.2\(([0-9]+\.[0-9]+)\*kWh\)\r\n')
        packet['kwh']['high']['produced'] = self.get_float(b'^1-0:2\.8\.2\(([0-9]+\.[0-9]+)\*kWh\)\r\n')

        packet['kwh']['current_consumed'] = self.get_float(b'^1-0:1\.7\.0\(([0-9]+\.[0-9]+)\*kW\)\r\n')
        packet['kwh']['current_produced'] = self.get_float(b'^1-0:2\.7\.0\(([0-9]+\.[0-9]+)\*kW\)\r\n')

        packet['kwh']['current_consumed_phaseOne'] = self.get_float(b'^1-0:21\.7\.0\(([0-9]+\.[0-9]+)\*kW\)\r\n')
        packet['kwh']['current_consumed_phaseTwo'] = self.get_float(b'^1-0:41\.7\.0\(([0-9]+\.[0-9]+)\*kW\)\r\n')
        packet['kwh']['current_consumed_phaseThree'] = self.get_float(b'^1-0:61\.7\.0\(([0-9]+\.[0-9]+)\*kW\)\r\n')

        packet['kwh']['current_produced_phaseOne'] = self.get_float(b'^1-0:22\.7\.0\(([0-9]+\.[0-9]+)\*kW\)\r\n')
        packet['kwh']['current_produced_phaseTwo'] = self.get_float(b'^1-0:42\.7\.0\(([0-9]+\.[0-9]+)\*kW\)\r\n')
        packet['kwh']['current_produced_phaseThree'] = self.get_float(b'^1-0:62\.7\.0\(([0-9]+\.[0-9]+)\*kW\)\r\n')


'''

body=''
bodyTemplate_energy = 'emeter_energy,eqid={eid},tarif={tarif},direction={dir} value={value} {etime}\n'
bodyTemplate_power = 'emeter_power,eqid={eqid},tarif={tarif},direction={dir},phase={phase} value={value} {etime}\n'
eid = packet['kwh']['eid']
tariff=packet['kwh']['tariff']
body += bodyTemplate_energy.format(	eqid=eid, dir='in', tarif='1', value=packet['kwh']['high']['consumed']] )
body += bodyTemplate_energy.format(	eqid=eid, dir='in', tarif='1', value=packet['kwh']['high']['produced']] )
body += bodyTemplate_energy.format(	eqid=eid, dir='in', tarif='2', value=packet['kwh']['low']['consumed']] )
body += bodyTemplate_energy.format(	eqid=eid, dir='in', tarif='2', value=packet['kwh']['low']['produced']] )

body += bodyTemplate_power.format( eqid=eid, dir='in', tarif=tariff, phase='L1', value=packet['kwh']['current_consumed_phaseOne']] )
body += bodyTemplate_power.format( eqid=eid, dir='in', tarif=tariff, phase='L2', value=packet['kwh']['current_consumed_phaseTwo']] )
body += bodyTemplate_power.format( eqid=eid, dir='in', tarif=tariff, phase='L3', value=packet['kwh']['current_consumed_phaseThree']] )
body += bodyTemplate_power.format( eqid=eid, dir='in', tarif=tariff, phase='total', value=packet['kwh']['current_consumed'] )

body += bodyTemplate_power.format( eqid=eid, dir='out', tarif=tariff, phase='L1', value=packet['kwh']['current_produced_phaseOne']] )
body += bodyTemplate_power.format( eqid=eid, dir='out', tarif=tariff, phase='L2', value=packet['kwh']['current_produced_phaseTwo']] )
body += bodyTemplate_power.format( eqid=eid, dir='out', tarif=tariff, phase='L3', value=packet['kwh']['current_produced_phaseThree']] )
body += bodyTemplate_power.format( eqid=eid, dir='out', tarif=tariff, phase='total', value=packet['kwh']['current_produced'] )
		
print body

