from flask import Flask, render_template, request, url_for, jsonify
from flask.ext.cors import CORS
import requests
from pymongo import MongoClient
from datetime import datetime
from requests.auth import HTTPBasicAuth


app = Flask(__name__,static_url_path='')
cors = CORS(app)

cus_id = 'cus_KAcVLFvhNbupSF'
api_key = 'c96b649c-d25d-465a-bffe-66546a32be58'
client = MongoClient('localhost', 27017)
quotes_db = client.quotes_db
collection = quotes_db.userInfo



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
    origin = "University of Pennsylvania Philadelphia, PA 19104"
    destination = "21 N Juniper St Philadelphia, PA 19107"

    print collection.find_one()
    return render_template('map2.html',
        origin = origin,
        destination = destination)

#---------- EVERYTHING BELLOW IS FOR PAV-------------
from mandrillUtils import sendEmail
import json

def getDeliveryInfo(delivery_id):
    headers = {'Authorization': 'Basic ' + api_key + '=='}
    headers = auth=(api_key,'')
    r = requests.get('https://api.postmates.com/v1/customers/'+cus_id+'/deliveries/'+delivery_id,auth=headers)
    return r.json()

@app.route('/recievereply', methods=['GET','POST'])
def recieveReply():
    if request.method == 'POST':
        emailText = str(json.loads(str(request.form['mandrill_events']))[0]['msg']['text'])
        from_email = str(json.loads(str(request.form['mandrill_events']))[0]['msg']['from_email'])
        address = emailText.split('\n')[0]
        
        from pymongo import MongoClient
        client = MongoClient()
        db = client['postmates']
        collection = db['deliveries']
        payload = collection.find_one({"seller_email": from_email})
        payload['pickup_address'] = address
        payload['pickup_name']='Seller\'s home'

        headers = {'Authorization': 'Basic ' + api_key + '=='}
        headers = auth=(api_key,'')
        
        r = requests.post('https://api.postmates.com/v1/customers/'+cus_id+'/deliveries',auth=headers,data=payload)
        	
        from firebase import firebase
        firebase = firebase.FirebaseApplication('https://freeforfee.firebaseio.com/id', None)
        delivery_id = r.json()['id']
        delivery_info = getDeliveryInfo(delivery_id)
        lat = 0#delivery_info['courier']['location']['lat']
        lon = 0#delivery_info['courier']['location']['lng']
        firebase.post('id/'+delivery_id,{'lat':lat,'long':lon}) 
        sendEmail('pavleen.me/random/'+delivery_id+'\n\n'+str(r.json()),'pav920@gmail.com')
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

    from pymongo import MongoClient
    client = MongoClient()
    db = client['postmates']
    collection = db['deliveries']
    collection.insert(payload)
    #save in mongo
    sendEmail('Hi, \n    My name is '+payload['dropoff_name']+" and I would love to take the '"+payload['manifest']+"' off your hands! I'm using the Postmates delivery service to pick it up, and they will automatically read your email reply to this email. \n\n    If you're okay with letting me pick up the item in your listing, simply reply to this email with only your address. Reply when you'll be arround in the next hour. \n\n    The postmate service will read the email and automatically send someone out to pick it up within an hour of when you reply.\n    Again, if you reply only include your pickup address and nothing else! Thanks so much. Have a great day.\nSincerely,\n"+payload['dropoff_name'],payload['seller_email'])
    return 'done'
#---------EVERYTHING BELLOW IS FOR CHRIS-------------

from pygeocoder import Geocoder

def convertToDatetime(s):
    return datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')

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

        userID = request.form["id"]
        kind = request.form["kind"]
        fee = request.form["fee"]
        created = convertToDatetime(request.form["created"])
        expires = convertToDatetime(request.form["expires"])
        currency = request.form["currency"]
        duration = request.form["duration"]
        dropoffEta = convertToDatetime(request.form["dropoff_eta"])

        collection.update(
            {"userID": userID},
            {
                "userID": userID,
                "kind": kind,
                "fee": fee,
                "created": created, 
                "expires": expires, 
                "currency": currency, 
                "duration": duration, 
                "dropoffEta": dropoffEta
            },
            upsert=True
        )

        returnDict = json.loads(r.text)

    	returnDict['dropoff_address'] = payload['dropoff_address']
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
