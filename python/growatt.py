import os
import time
import json
import lib.registers as registers
from configparser import ConfigParser
import paho.mqtt.client as mqtt
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusIOException
import graphyte

config = ConfigParser()
config.read("config.toml")
mapper = config['DEFAULT']['mapper']
with open("mapping/" + mapper) as f:
    mapping = json.load(f)

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK to MQTT Returned code=",rc)
    else:
        print("Bad connection Returned code=",rc)

mqtt_client = mqtt.Client("inverter")
mqtt_client.on_connect = on_connect
mqtt_client.connect("mosquitto")
mqtt_client.loop_start()

mqtt_client.publish('homeassistant/sensor/growattmqtt/config',payload='{"name": "Growatt MQTT", "object_id": "growatt_inverter"}')

for reg in mapping['registerGroups']:
    regMap = reg['registerMap']
    for map in regMap:
        mqtt_client.publish('homeassistant/sensor/growatt_' + map + '/config',payload='{"device_class" : "' + regMap[map]['class'] + '","name" : "'+ regMap[map]['name'] + '","state_topic" : "inverter/growattmqtt/'+map+'","unit_of_measurement" : "' + regMap[map]['unit']+'", "unique_id": "growatt_'+map+'", "object_id": "growatt_'+map+'", "device_id": "growatt_inverter"}', retain=True)

port = config['DEFAULT']['port'] 

client = ModbusClient(method='rtu', port=port, baudrate=9600, stopbits=1, parity='N', bytesize=8, timeout=1)
client.connect()
graphyte.init('graphite', port=2003)

while True:
    regs = {}
    for reg in mapping['registerGroups']:
        row = client.read_input_registers(reg['start'], reg['length'], unit=0).registers
        regMap = reg['registerMap']
        for map in regMap:
            if regMap[map]['words'] == 2:
                regs[map] = registers.get_double(row, regMap[map]['id'] - reg['start'], regMap[map]['mul'])
            else:
                regs[map] = registers.get_single(row, regMap[map]['id'] - reg['start'], regMap[map]['mul'])

    print(regs)
    for key, value in regs.items():
        graphyte.send("inverter." + key, value)
        mqtt_client.publish("inverter/growattmqtt/" + key, payload=value)

    time.sleep(5)
