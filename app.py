from flask import Flask, render_template, request, url_for
from flask.ext.cors import CORS
import requests

app = Flask(__name__,static_url_path='')
cors = CORS(app)


cus_id = 'cus_KAcVLFvhNbupSF'
api_key = 'c96b649c-d25d-465a-bffe-66546a32be58'

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
    seller = request.form['seller_name']
    itemName = request.form['item_name']
    pickupAddress = request.form['pickup_address']
    phoneNum = request.form['pickup_phone_number']
    notes = request.form['dropoff_notes']
    buyer = request.form['buyer_name']
    dropAddress = request.form['dropoff_address']
    dropPhoneNum = request.form['dropoff_phone_number']
    quoteId = request.form['quote_id']

    payload = {'user':api_key,'pickup_name':seller,'manifest':itemName,'pickup_address':pickupAddres,'pickup_phone_number':phoneNum,'pickup_notes':notes,'dropoff_name':buyer,'dropoff_address':dropAddress,'dropoff_phone_number':dropPhoneNum,'dropoff_notes':notes,'quote_id':quoteId}
    r = requests.post('https://api.postmates.com/v1/customers/'+cus_id+'/deliveries',params=payload)
    return 'done'
#---------EVERYTHING BELLOW IS FOR CHRIS-------------

import json
from pygeocoder import Geocoder

@app.route('/getquote', methods=['GET','POST'])
def getquote():
    if request.method == 'POST':
        url = 'https://api.postmates.com/v1/customers/cus_KAe13l92WYA7fV/delivery_quotes'
        headers = {'Authorization': 'Basic OGE3OWJmYzQtZmUxMS00OTRkLTg1ZjMtMzYyNmFjNGM5YTIzOg=='}
        payload = {}
        
        lat = request.form['destLat']
        lon = request.form['destLon']
        payload['pickup_address'] = Geocoder.reverse_geocode(lat, lon)
        payload["destination_address"] = request.form['destination_address']
        r = requests.post(url, headers=headers, data=payload)
        #do things with the form 

        returnDict = json.loads(r.text)
        return flask.jsonify(**returnDict)
    else:
        return 'HI DOE'

#-------- EVERYTHING BELLOW IS FOR HIMANSHU----------
@app.route('/map')
def map():
    #DO POST REQUEST
    lat = 39.96 
    lon = -75.2
    return render_template('googlemap.html', latitude=lat, longitude=lon)
