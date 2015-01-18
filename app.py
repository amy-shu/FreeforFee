from flask import Flask, render_template, request, url_for
app = Flask(__name__)


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


#-------- EVERYTHING BELLOW IS FOR HIMANSHU----------
@app.route('/map')
def map():
    #DO POST REQUEST
    lat = 40 
    lon = -76
    return render_template('googlemap.html', latitude=lat, longitude=lon)
