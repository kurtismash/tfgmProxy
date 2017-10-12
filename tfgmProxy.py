from gevent import monkey; monkey.patch_all()

import requests
from gevent.pywsgi import WSGIServer
from flask import Flask, Response, request, jsonify, abort, render_template
from bs4 import BeautifulSoup

config = {
	'bindAddr' : 'localhost',
	'bindPort' : '5004',
	'url' : 'https://beta.tfgm.com'
}

app = Flask(__name__)

#Tram departures:
@app.route('/tram/<location>/departures.json')
def tramDepartures(location):
	departures = []
	page = requests.get('%s/public-transport/tram/stops/%s-tram' %(config['url'],location))
	soup = BeautifulSoup(page.content, 'html.parser')
	htmlTrams = soup.find_all(class_='tram')
	if len(htmlTrams) == 0:
		return jsonify([])
	else:
		htmlTrams.pop(0)
		#Get data for each tram
		for tram in htmlTrams:
			try:
				destination = tram.find(class_='departure-destination').contents[0]
			except:
				destination = ''
			try:
				carriages = tram.find(class_='departure-carriages').contents[1].contents[0]
			except:
				carriages = ''
			try:
				departs = tram.find(class_='departure-wait').contents[1].contents[0]
			except:
				departs = ''

			departures.append({
			'destination' : destination,
			'carriages' : carriages,
			'departs' : departs
			})
	return jsonify(departures)

#Tram stations:
@app.route('/tram/stops.json')
def tramstops():
	tramstops = []
	page = requests.get('%s/public-transport/tram/stops' % config['url'])
	soup = BeautifulSoup(page.content, 'html.parser')
	stops = soup.find_all(class_='result-button')
	for stop in stops:
		stop = stop.contents[1].contents[0]
		stop = stop.lower()
		stop = stop.replace(' ', '-')
		stop = stop.replace('\'', '')
		stop = stop[:-10]
		tramstops.append(stop)
	return jsonify(tramstops)

#Bus departures:
@app.route('/bus/<location>/departures.json')
def busDepartures(location):
	departures = []
	page = requests.get('https://beta.tfgm.com/public-transport/bus/stations/%s-bus' % location)
	soup = BeautifulSoup(page.content, 'html.parser')
	buses = soup.find_all(class_='bus')
	if len(buses) == 0:
		return jsonify([])
	else:
		buses.pop(0)
		for bus in buses:
			try:
				departureDestination = bus.find(class_='departure-destination').contents[3].contents[0]
			except:
				departureDestination = ''
			try:
				departureRoute = bus.find(class_='departure-destination').contents[1].contents[0]
			except:
				departureRoute = ''
			try:
				departureOperator =  bus.find(class_='departure-operator').contents[0]
			except:
				departureOperator = ''
			try:
				departureStand = bus.find(class_='departure-stand').contents[0]
			except:
				departureStand = ''
			try:
				departureExpected = bus.find(class_='departure-expected').find(class_='figure').contents[0]
			except:
				departureExpected = ''
			try:
				departureIndicator = bus.find(class_='departure-indicator')
				if departureIndicator.find(class_='due-icon nim-icon'):
					departureIndicator = 'Live'
				else:
					departureIndicator = 'Timetabled'
			except:
				departureIndicator = ''
			try:
				palmStand = bus.find(class_='palm-stand').contents[0]
			except:
				palmStand = ''
			try:
				palmOperator = bus.find(class_='palm-operator').contents[0]
			except:
				palmOperator = ''


			departures.append({
				'departureDestination' : departureDestination,
				'departureRoute' : departureRoute,
				'departureOperator' : departureOperator,
				'departureStand' : departureStand,
				'departureExpected' : departureExpected,
				'departureIndicator' : departureIndicator,
				'palmStand' : palmStand,
				'palmOperator' : palmOperator

			})
	return jsonify(departures)

#Bus stations:
@app.route('/bus/stations.json')
def busstops():
	busstops = []
	page = requests.get('%s/public-transport/bus/stations' % config['url'])
	soup = BeautifulSoup(page.content, 'html.parser')
	stops = soup.find_all(class_='result-button')
	for stop in stops:
		stop = stop.contents[1].contents[0]
		stop = stop.lower()
		stop = stop.replace(' ', '-')
		stop = stop.replace('\'', '')
		stop = stop.replace('-bus-station', '')
		stop = stop.replace('-coach-station','')
		busstops.append(stop)
	return jsonify(busstops)

#Configure and serve webserver
if __name__ == '__main__':
    http = WSGIServer((config['bindAddr'], int(config['bindPort'])), app.wsgi_app)
    http.serve_forever()
