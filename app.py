from flask import Flask, render_template, request, url_for
from flask.ext.cors import CORS
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

@app.route('/sendpurchase',method=['GET','POST'])
def sendpurchase():
    return 'done'
#---------EVERYTHING BELLOW IS FOR CHRIS-------------

@app.route('/getquote', methods=['GET','POST'])

def getQuote():
    if request.method == 'POST':
        #print request.form['event']
        #do things with the form data
        return 'done'
    else:
        return 'HI DOE'

#-------- EVERYTHING BELLOW IS FOR HIMANSHU----------
@app.route('/map')
def map():
    #DO POST REQUEST
    lat = 39.96 
    lon = -75.2
    return render_template('googlemap.html', latitude=lat, longitude=lon)
