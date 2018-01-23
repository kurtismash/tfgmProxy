DEPRECIATED
========
This has been depreciated as TFGM now provide an API for this, see https://developer.tfgm.com.

## tfgmProxy

A flask app that scrapes html from Travel For Greater Manchester to provide a JSON API.

## tfgmProxy configuration
1. Configure tfgmProxy.py options as per your setup and neeeds.
2. Create a virtual environment  `$ virtualenv env`
3. Activate the virtual environment  `$ . env/bin/activate`
4. Install the requirements `$ pip install -r requirements.txt`
5. Run the app `$ python tfgmProxy.py`

## systemd service configuration
A startup script for Ubuntu is located in tfgmProxy.service (the paths need changing to match your setup), install with:

````
$ sudo cp tfgmProxy.service /etc/systemd/system/tfgmProxy.service
$ sudo systemctl daemon-reload
$ sudo systemctl enable tfgmProxy.service
$ sudo systemctl start tfgmProxy.service 
````

## Using the JSON API
The API can now be accessed at the IP address and port you've specified in `tfgmProxy.py`.
Currently, the following calls are implemented:
* /tram/[location]/departures.json
* /tram/stops.json
* /bus/[location]/departures.json
* /bus/stations.json
