from flask import Flask, request, jsonify
import flask
import sys
import os
import urllib
import json

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/')

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public_html")

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return flask.send_from_directory(root, path)


@app.route('/', methods=['GET'])
def redirect_to_index():
    return flask.send_from_directory(root, 'index.html')

if __name__ == '__main__':  # pragma: no cover
    app.run(host='0.0.0.0', port=5001, debug = True)
