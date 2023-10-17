"""
Miles Anderson's Flask API.
"""

from flask import Flask
from flask import send_file #added this so I can easily handle html files
from flask import send_from_directory #for the .css file
from flask import abort
import os #so I can handle 404 errors
import configparser

# Border for the Config Parser

def parse_config(config_paths):
    config_path = None
    for f in config_paths:
        if os.path.isfile(f):
            config_path = f
            break

    if config_path is None:
        raise RuntimeError("Configuration file not found!")

    config = configparser.ConfigParser()
    config.read(config_path)
    return config

config = parse_config(["credentials.ini", "default.ini"])
portNum = config["SERVER"]["PORT"]
dbug = config["SERVER"]["DEBUG"]

# Border for the Config Parser

app = Flask(__name__)

@app.route("/")
def hello():
    return "UOCIS docker demo!\n"

@app.errorhandler(403)
def forbidden(e):
    return send_from_directory("pages/", "403.html"), 403

@app.errorhandler(404)
def notFound(e):
    return send_from_directory("pages/", "404.html"), 404

# First test to see if there are any illegal characters
@app.route("/<string:address>")
def fileHandler(address):
    address=address
    path = "./pages/"+address
    for i in range(len(address)): #first check for illegal characters
        if (address[i] == "." and address[i-1] == '.') or address[i] == '~':
            abort(403)
    if os.path.exists(path) == False:
        abort(404)
    else:
        return send_from_directory("pages/", address), 200

if __name__ == "__main__":
    app.run(debug=dbug, host='0.0.0.0', port=portNum)
