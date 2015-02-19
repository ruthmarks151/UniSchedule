from flask import Flask, request, jsonify
import flask
import sys
import os
import urllib
import json

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/')

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public_html")


#By default serve up static files
@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return flask.send_from_directory(root, path)

#Serve the index html from the root
@app.route('/', methods=['GET'])
def redirect_to_index():
    return flask.send_from_directory(root, 'index.html')

@app.route('/courses')
def autofill_courses():
    user = request.args.get("UserToken")
    text = request.args.get("EnteredText")
    number = request.args.get("CourseNumber")
    return 200

@app.route('/preferences/earlylate')
def set_earlylate():
    user = request.args.get("UserToken")
    early_late_preference = request.args.get("EarlyLatePreference")
    return 200

@app.route('/preferences/density')
def set_density():
    user = request.args.get("UserToken")
    density_preference = request.args.get("Density")
    return 200

@app.route('/preferences/exceptions')
def set_exceptions():
    user = request.args.get("UserToken")
    #This might have a tricky datatype, don't handle it for now
    #exceptions = request.args.get("Density")
    return 200

@app.route('/preferences/weekuniformity')
def set_week_uniformity():
    user = request.args.get("UserToken")
    week_uniformity_preference = request.args.get("WeekUniformity")
    return 200


@app.route('/preferences/ThirstyThursdays')
def set_thirsty_thursday():
    user = request.args.get("UserToken")
    thirsty_thursday_preference = request.args.get("ThirstyThursdays")
    return 200

@app.route('/preferences/DayOff')
def set_thirsty_thursday():
    user = request.args.get("UserToken")
    day_off_preference = request.args.get("DayOff")
    return 200

@app.route('/preferences/BreakLength')
def set_break_lengths():
    user = request.args.get("UserToken")
    break_lengths_preference = request.args.get("BreakLength")
    return 200

@app.route('/timetable')
def get_timetable():
    user = request.args.get("UserToken")
    return 200

if __name__ == '__main__':  # pragma: no cover
    app.run(host='0.0.0.0', port=5001, debug = True)
