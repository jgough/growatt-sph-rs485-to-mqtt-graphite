# Growatt SPH-XXXX series to MQTT and Grafana using Whisper DB backend

Requirements: 

- 64 bit machine capable of running Linux and python version 3.12 connected to the internet. Raspberry Pi 3 / Pi Zero 2 or above should suffice, though an old laptop/desktop running Ubuntu or similar would do.

- USB to RS485 device to connect to the inverter. Please check the inverter's manual for wiring the RJ45 cable to the USB-RS458 correctly, or purchase the correct cable.

To use:

Change config.toml to the right USB adapter for your inverter. Usually /dev/ttyUSB0. Optionally change the mapper to the JSON file for your inverter. 

`docker-compose up -d`

Then go to `<ip of raspberry pi>:3000` in a browser, and import the dashboard from grafana/dashboard.json

Home assistant discovery is supported with the MQTT integration.

Mosquitto MQTT broker is run on the same docker instance to assist with new setups.

Uses the whisper database from graphite as backend storage, offering fast and efficient storage of data for many years.  You can view the graphite backend at `<ip of raspberry pi>:8080`.  Configure the data retention period in the file at graphite/storage-schemas.conf
  
Currently only Growatt SPH-XXXX inverters are supported, or inverters that support Growatt ModBus Version 2. You can add more modbus mappings in the `python/mapping` folder.

Tested with recent Growatt SPH-3600 and SPH-5000 inverters with battery pack.
