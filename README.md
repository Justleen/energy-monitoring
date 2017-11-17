Install requirements:
sudo apt-get install python-serial python-crcmod python-pip
sudo pip install MinimalModbus


Create a config file config.ini, and set correct path/filename in script.
# config example:
```
[influxdb]
dbname = db_name
influxHost = 
port = 8086
huisID = 8121JZ48
username = 
wachtwoord = 

[smeter]
baudrate = 115200
timeout = 8
device = /dev/ttyAMA0

[rs485]
Instrument = /dev/ttyUSB0
debug = False
baudrate = 9600
bytesize = 8
stopbits = 1
timeout = 5

[logging]
level = Error
```




# Influxdb schema
```
	emeter_energy
		tagKey:
			eqid	
			phase [total, L1, L2, L3]
			tarif [1,2]
			direction [in, out]
		values:
			energy [float/int]

	emeter_power
		tagKey:
			eqid	
			phase [total, L1, L2, L3]
			tarif [1,2]
			direction [in, out]			
		values:
			power [float/int]			

	esp_events
		tagKey:
			eqid
			event	
			ssid	
		values:
			count [1, none]
```
