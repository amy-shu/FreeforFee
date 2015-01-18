from flask import Flask, render_template, request, url_for, jsonify
from flask.ext.cors import CORS
import requests
from requests.auth import HTTPBasicAuth


app = Flask(__name__,static_url_path='')
cors = CORS(app)

cus_id = 'cus_KAe13l92WYA7fV'
api_key = '8a79bfc4-fe11-494d-85f3-3626ac4c9a23'


@app.route('/')
def index():
    return "Hello, World!"

@app.route('/post', methods=['POST'])
def test():
    print request.form
    print request.method
    a = request.form['a']
    print a
    return a

@app.route('/random/<rString>')
def displayString(rString):
    origin = "asdasd"
    destination = "Sasdssssssasd"
    return render_template('map2.html',
        origin = origin,
        destination = destination)

#---------- EVERYTHING BELLOW IS FOR PAV-------------
from mandrillUtils import sendEmail

@app.route('/recievereply', methods=['GET','POST'])
def recieveReply():
    if request.method == 'POST':
	#print request.form['event']

    	sendEmail('Himanshu Hoe doe','pav920@gmail.com')
        return 'done'
    else:
	return 'yolo'

@app.route('/sendpurchase',methods=['GET','POST'])
def sendpurchase():
    payload = {}
    payload['manifest'] = request.form['item_name']
    payload['pickup_phone_number'] = request.form['pickup_phone_number']
    payload['dropoff_notes'] = request.form['dropoff_notes']
    payload['dropoff_name'] = request.form['buyer_name']
    payload['dropoff_address'] = request.form['dropoff_address']
    payload['dropoff_phone_number'] = request.form['dropoff_phone_number']
    payload['quote_id'] = request.form['quote_id']
    payload['seller_email'] = request.form['seller_email']
    #save in mongo
    sendEmail('Hi, \n    My name is '+payload['dropoff_name']+" and I would love to take the '"+payload['manifest']+"' off your hands! I'm using the Postmates delivery service to pick it up, and they will automatically read your email reply to this email. \n    If you're okay with letting  me pick up the item in your listing simply reply to this email with your address when you'll be arround in the next hour. The postmate guys will read the email and automatically send someone out to pick it up within an hour of when you reply.\n    But again if you reply only include your pickup address and nothing else! Thanks so much. Have a great day.\nSincerely,\n"+payload['dropoff_name'],payload['seller_email'])
    return str(r.json())
#---------EVERYTHING BELLOW IS FOR CHRIS-------------

import json
from pygeocoder import Geocoder

@app.route('/getquote', methods=['GET','POST'])
def getquote():
    if request.method == 'POST':
        url = 'https://api.postmates.com/v1/customers/' + cus_id + '/delivery_quotes'
	headers = {'Authorization': 'Basic ' + api_key + '=='}
	headers = auth=(api_key,'')
        payload = {}
        
        lat = request.form['destLat']
        lon = request.form['destLon']
        address = Geocoder.reverse_geocode(float(lat), float(lon))
        payload['pickup_address'] = str(address)
        payload["dropoff_address"] = request.form['destination_address']
        r = requests.post(url, auth=headers, data=payload)
        #do things with the form 

        returnDict = json.loads(r.text)
	#return str(address)
	return jsonify(**returnDict)
    else:
        return 'HI DOE'

#-------- EVERYTHING BELLOW IS FOR HIMANSHU----------
@app.route('/map')
def map():
    #DO POST REQUEST
    lat = 39.96 
    lon = -75.2
    return render_template('googlemap.html', latitude=lat, longitude=lon)
