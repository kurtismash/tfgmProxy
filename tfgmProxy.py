from gevent import monkey; monkey.patch_all()

import requests
from gevent.pywsgi import WSGIServer
from flask import Flask, Response, request, jsonify, abort, render_template
from bs4 import BeautifulSoup

config = {
	'defaultTramStop' : 'mediacityuk',
	'bindAddr' : 'localhost',
	'bindPort' : '5004'	
}

app = Flask(__name__)

@app.route('/departures.json')
def departures():
	location = request.args.get('location') or config['defaultTramStop']
	departures = []
	page = requests.get('https://beta.tfgm.com/public-transport/tram/stops/%s-tram' % location)
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

#Configure and serve webserver
if __name__ == '__main__':
    http = WSGIServer((config['bindAddr'], int(config['bindPort'])), app.wsgi_app)
    http.serve_forever()

