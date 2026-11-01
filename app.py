from flask import Flask, jsonify
import datetime
import pytz
import ephem

app = Flask(__name__)

@app.route('/')
def home():
    return "Ritam API is Live!"

@app.route('/panchang')
def get_panchang():
    # भारत का समय (IST)
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(ist)
    
    # खगोलीय गणना (Ephemeris) के लिए सेटअप
    observer = ephem.Observer()
    observer.date = now.astimezone(pytz.utc)
    
    sun = ephem.Sun(observer)
    moon = ephem.Moon(observer)
    
    # सूर्य और चंद्रमा की डिग्री से तिथि निकालना (1 तिथि = 12 डिग्री)
    sun_lon = ephem.Ecliptic(sun).lon
    moon_lon = ephem.Ecliptic(moon).lon
    
    diff = (moon_lon - sun_lon)
    if diff < 0:
        diff += 2 * ephem.pi
        
    tithi_number = int((diff / ephem.pi * 180) / 12) + 1

    # सुरक्षित और सटीक डेटा भेजना
    return jsonify({
        "live_date": now.strftime('%d %B %Y'),
        "live_time": now.strftime('%I:%M %p'),
        "day": now.strftime('%A'),
        "tithi_index": tithi_number,
        "message": "Success"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
