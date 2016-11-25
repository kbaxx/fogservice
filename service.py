from grovepi import *

import requests
import sys
import json
import math

def calculateData(data):
	avgTemp = 0
	avgHum = 0
	maxTemp = -sys.maxint - 1
	maxHum = -sys.maxint - 1 
	minTemp = sys.maxint
	minHum = sys.maxint
	sumTemp = 0
	sumHum = 0
	for value in data:
		temp = value.get("temp")
		hum = value.get("hum")
		if temp > maxTemp:
			maxTemp = temp
		if hum > maxHum: 
			maxHum = hum
		if temp < minTemp:
			minTemp = temp
		if hum < minHum:
			minHum = hum
		sumTemp += temp
		sumHum += hum
	avgTemp = sumTemp / len(data)
	avgHum = sumHum / len(data)

	return [{"key":"temp", "data":[{"avg":avgTemp, "max":maxTemp, "min": minTemp}]}, {"key":"hum", "data":[{"avg":avgHum, "max":maxHum, "min": minHum}]}]


def sendRequest(data):
	host = "http://192.168.1.101:8081"
	response = requests.post(host+"/compunit/serviceData", data=json.dumps(data), headers={"Content-Type": "application/json"})
	print(response.text)


# -------------------------------------------------------------------------------------------------------------------------------------------------

dht_sensor_port = 7             # Connect the DHt sensor to port 7
dht_sensor_type = 0             # change this depending on your sensor type - see header comment

data = []
counter = 0
MAX = 50
while True:
    try:
        [ temp,hum ] = dht(dht_sensor_port,dht_sensor_type)             #Get the temperature and Humidity from the DHT sensor
        #temp = 0
        #hum = 0
	if temp == -1 or math.isnan(temp) or hum == -1 or math.isnan(hum):
        	print("invalid read")
        	continue 

        print("temp =", temp, "C, humidity =", hum,"%")

        # calculate the average, max, min of a specific size of measurements and send it to the cloud
        data.append({"temp": temp, "hum": hum})
        counter = counter + 1
        if counter > MAX:
        	calculatedData = calculateData(data)
        	sendRequest(calculatedData)
        	counter = 0
    except (IOError,TypeError) as e:
        print("Error")