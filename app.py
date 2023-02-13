from flask import Flask, render_template, request, jsonify, send_file
from geopy.geocoders import Nominatim
import boto3
import requests
import venv
import os
import json
import datetime 

app = Flask(__name__)
#dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
#table = dynamodb.Table('weatherapp')
name_dir = "history"
bg_color = os.environ.get('color')

if not os.path.exists(name_dir):
   os.mkdir(name_dir)

def get_data(values, userInput):
    lat = values[0]
    lon = values[1]
    
    data_obj = requests.get(f"http://api.weatherunlocked.com/api/forecast/{lat},{lon}?app_id={venv.app_id}&app_key={venv.app_key}")
    data_obj = data_obj.json()
    data_list = data_obj["Days"]
    days_list = []   #array of dictionaries data about all 7 days/ len = 7
    for item in data_list:
       days_list.append(item)

    """for i in range(0, 7):
       table.put_item(
          Item={
            'city': userInput,
            'date': days_list[i]['date'],
            'tmp_max': days_list[i]['temp_max_c'],
            'tmp min': days_list[i]['temp_min_c'],
          }
       )"""
    """for i in range(0, 7):
       print(f"day {i+1}: {days_list[i]['date']} {days_list[i]['temp_max_c']} {days_list[i]['temp_min_c']}")"""

    with open(f"{name_dir}/{userInput}_{datetime.datetime.now()}.json", "w") as fp:
         json.dump(data_obj, fp)  
    
    
    return days_list 


@app.route("/", methods=["POST","GET"])
def home():  
    res = ""
    if request.method == "POST":
        try:
           userInput = request.form["City"]
           loc = Nominatim(user_agent="GetLoc")
           get_loc = loc.geocode(userInput)
           lat = get_loc.latitude
           lon = get_loc.longitude
           print(get_loc)
           print(f"lat: {lat} lon: {lon}")
           res = get_data([lat, lon], userInput)
           return render_template("index.html", data=res, address=get_loc, bg_color=bg_color)
        except Exception: 
           message = "invalid input"
           return render_template("index.html", message=message)
    if request.method == "GET":
        return render_template("index.html", bg_color=bg_color)
      
@app.route("/history")
def history():
    dir_list = os.listdir(f"{name_dir}/")
    return render_template("history.html", list_history=dir_list)

@app.route("/history/<string:filename>")   
def download(filename):   
   return send_file(f"history/{filename}", as_attachment=True)
   
   
   
   
if __name__ == "__main__":
   app.run(host='0.0.0.0')
   

