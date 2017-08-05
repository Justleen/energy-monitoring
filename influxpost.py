from smeterd.meter import SmartMeter
meter = SmartMeter('/dev/ttyAMA0', baudrate=115200)
packet = meter.read_one_packet()
print packet['kwh']['etime']
