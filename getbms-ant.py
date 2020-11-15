#Create getbms-ant.py file
import sys
import time
import serial
import struct
from binascii import unhexlify
import requests as req
import bluetooth
from bluetooth import *
import paho.mqtt.client as mqtt
import json
import time

#if sys.version < '3':
#    input = raw_input
timestamp = int(time.time())

bd_addr = "AA:BB:CC:B1:23:45"

port = 1

#sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
#sock.connect((bd_addr, port))
#sock.close()
#time.sleep(1)

#Define RS485 serial port
ser = serial.Serial(
    port='/dev/rfcomm1',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 1)

client = mqtt.Client('bms')
#client.on_connect = on_connect
#client.on_message = on_message
#set up username and password for your MQTT server
client.username_pw_set("mqqt", password="Alina.1980")
#ip address/website of MQTT server
client.connect("10.10.10.3", 1883, 60)
topic_prefix = 'homeassistant'
#state_topic = "bms/"entity"/state"
client.loop_start()
device = 'bms'
commands = ['ON', 'OFF']


entities = {
    'soc': ['sensor', {'name': 'SoC', 'device_class': 'battery', 'unit_of_measurement': '%', 'icon': 'mdi:battery'}],
#    'shh': ['switch', {'name': 'Frontr'}],
    'power': ['sensor', {'name': 'Power', 'unit_of_measurement': 'W', 'device_class': 'power'}],
    'amps': ['sensor', {'name': 'Amps', 'unit_of_measurement': 'A', 'icon': 'mdi:current-dc', 'device_class': 'current'}],
    'volts': ['sensor', {'name': 'Battery BMS Voltage', 'unit_of_measurement': 'V', 'icon': 'mdi:flash', 'device_class': 'voltage'}],
    'cell_avg': ['sensor', {'name': 'Cell Avg', 'unit_of_measurement': 'V', 'icon': 'mdi:flash', 'device_class': 'voltage'}],
    'cell_min': ['sensor', {'name': 'Cell Min', 'unit_of_measurement': 'V', 'icon': 'mdi:flash', 'device_class': 'voltage'}],
    'cell_max': ['sensor', {'name': 'Cell Max', 'unit_of_measurement': 'V', 'icon': 'mdi:flash', 'device_class': 'voltage'}],
    'cell_1': ['sensor', {'name': 'Cell 1', 'unit_of_measurement': 'V', 'icon': 'mdi:flash', 'device_class': 'voltage'}],
    'cell_2': ['sensor', {'name': 'Cell 2', 'unit_of_measurement': 'V', 'icon': 'mdi:flash', 'device_class': 'voltage'}],
    'cell_3': ['sensor', {'name': 'Cell 3', 'unit_of_measurement': 'V', 'icon': 'mdi:flash', 'device_class': 'voltage'}],
    'cell_4': ['sensor', {'name': 'Cell 4', 'unit_of_measurement': 'V', 'icon': 'mdi:flash', 'device_class': 'voltage'}],
    'cell_5': ['sensor', {'name': 'Cell 5', 'unit_of_measurement': 'V', 'icon': 'mdi:flash', 'device_class': 'voltage'}],
    'cell_6': ['sensor', {'name': 'Cell 6', 'unit_of_measurement': 'V', 'icon': 'mdi:flash', 'device_class': 'voltage'}],
    'cell_7': ['sensor', {'name': 'Cell 7', 'unit_of_measurement': 'V', 'icon': 'mdi:flash', 'device_class': 'voltage'}],
    'cell_8': ['sensor', {'name': 'Cell 8', 'unit_of_measurement': 'V', 'icon': 'mdi:flash', 'device_class': 'voltage'}],
}
for entity, value in entities.items():
    part2 = {
        "unique_id": entity,
        "state_topic": device+"/sensor/"+entity+"/state",
        "device":{
                "identifiers": "619",
                "name": device,
                "model": "local",
                "sw_version": "11.11.2020",
                "manufacturer": "home"
                }
    }
    topic = '{}/{}/{}/{}/{}'.format(topic_prefix, value[0], device,  entity, 'config')
    if value[0] not in ['binary_sensor', 'sensor']:
        value[1]['command_topic'] = '{}/{}/{}/{}/{}'.format(topic_prefix, value[0], device, entity, 'set')
    mes1 = json.dumps(value[1])
    mes2 =json.dumps(part2)
    dictA = json.loads(mes1)
    dictB = json.loads(mes2)
    merged_dict = {key: value for (key, value) in (dictA.items() + dictB.items())}
    message = json.dumps(merged_dict)
    client.publish(topic, message)
    time.sleep(0.2)


while True :
 test='DBDB00000000'
 try:
  ser.write (test.decode('hex'))
 except:
  ser.close()
 time.sleep(3)
 Antw33 = ser.read(140)
 
 #SoC
 try:
   SoC = (Antw33.encode('hex') [(74*2):(75*2)])
   print (SoC)
   SoC = int(SoC, 16)
   SoC = str(SoC)
   print (SoC)
   client.publish(device+"/sensor/soc/state", SoC)
 except ValueError:
   # handle ValueError exception
   print "Value Error!"
   pass

 #Power
 try:
    power = (Antw33.encode('hex') [(111*2):(114*2+2)])
    if int(power,16)>2147483648:
      power=(-(2*2147483648)+int(power,16))
      print (power)
      client.publish(device+"/sensor/power/state", str(power))
    else:
      power=int(power,16)
      print (power)
      client.publish(device+"/sensor/power/state", str(power))
 except:
    pass 
 
 #BMS current
 try:
    amps = (Antw33.encode('hex') [(70*2):(73*2+2)])
    if int(amps,16)>2147483648:
      amps=(-(2*2147483648)+int(amps,16))*0.1
      print (amps)
      client.publish(device+"/sensor/amps/state", amps)
    else:
      amps = int(amps,16)*0.1
      print (amps)
      client.publish(device+"/sensor/amps/state", amps)
 except:
    pass
 #BMS V
 try:
   volts = (Antw33.encode('hex') [8:12])
   volts = struct.unpack('>H',unhexlify(volts))[0]*0.1
   print (volts)
   client.publish(device+"/sensor/volts/state", volts)
 except:
    pass
 #Cell_avg
 try:
   cell_avg = (Antw33.encode('hex') [(121*2):(122*2+2)])
   cell_avg = struct.unpack('>H',unhexlify(cell_avg))[0]*0.001
   print (cell_avg)
   client.publish(device+"/sensor/cell_avg/state", cell_avg)
 except:
    pass
 #Cell_min
 try:
   cell_min = (Antw33.encode('hex') [(119*2):(120*2+2)])
   cell_min = struct.unpack('>H',unhexlify(cell_min))[0]*0.001
   print (cell_min)
   client.publish(device+"/sensor/cell_min/state", cell_min)
 except:
    pass
 #Cell_max 
 try:
   cell_max = (Antw33.encode('hex') [(116*2):(117*2+2)])
   cell_max = struct.unpack('>H',unhexlify(cell_max))[0]*0.001
   print (cell_max)
   client.publish(device+"/sensor/cell_max/state", cell_max)
 except:
   pass
  #Cell_1
 try:
   cell_1 = (Antw33.encode('hex') [(6*2):(7*2+2)])
   cell_1 = struct.unpack('>H',unhexlify(cell_1))[0]*0.001
   print (cell_1)
   client.publish(device+"/sensor/cell_1/state", cell_1)
 except:
   pass
 #Cell_2
 try:
   cell_2 = (Antw33.encode('hex') [(8*2):(9*2+2)])
   cell_2 = struct.unpack('>H',unhexlify(cell_2))[0]*0.001
   print (cell_2)
   client.publish(device+"/sensor/cell_2/state", cell_2)
 except:
   pass
  #Cell_3
 try:
   cell_3 = (Antw33.encode('hex') [(10*2):(11*2+2)])
   cell_3 = struct.unpack('>H',unhexlify(cell_3))[0]*0.001
   print (cell_3)
   client.publish(device+"/sensor/cell_3/state", cell_3)
 except:
   pass
  #Cell_4
 try:
   cell_4 = (Antw33.encode('hex') [(12*2):(13*2+2)])
   cell_4 = struct.unpack('>H',unhexlify(cell_4))[0]*0.001
   print (cell_4)
   client.publish(device+"/sensor/cell_4/state", cell_4)
 except:
   pass
  #Cell_5
 try:
   cell_5 = (Antw33.encode('hex') [(14*2):(15*2+2)])
   cell_5 = struct.unpack('>H',unhexlify(cell_5))[0]*0.001
   print (cell_5)
   client.publish(device+"/sensor/cell_5/state", cell_5)
 except:
   pass
 #Cell_6
 try:
   cell_6 = (Antw33.encode('hex') [(16*2):(17*2+2)])
   cell_6 = struct.unpack('>H',unhexlify(cell_6))[0]*0.001
   print (cell_6)
   client.publish(device+"/sensor/cell_6/state", cell_6)
 except:
   pass
 #Cell_7
 try:
   cell_7 = (Antw33.encode('hex') [(18*2):(19*2+2)])
   cell_7 = struct.unpack('>H',unhexlify(cell_7))[0]*0.001
   print (cell_7)
   client.publish(device+"/sensor/cell_7/state", cell_7)
 except:
   pass
 #Cell_8
 try:
   cell_8 = (Antw33.encode('hex') [(20*2):(21*2+2)])
   cell_8 = struct.unpack('>H',unhexlify(cell_8))[0]*0.001
   print (cell_8)
   client.publish(device+"/sensor/cell_8/state", cell_8)
 except:
   pass

 time.sleep(10)

ser.close()
