#!/usr/bin/python2
import os
import sys
import json
import time

settings_file = "{}/.config/{}".format(os.path.expanduser("~"), ".rotonde")

base = {
        "profile": {
            "name": "void", 
            "location": "the seas of rotonde", 
            "color": "#000000"},
        "feed": [],
        "portal": ["rotonde.cblgh.org", "rotonde.xxiivv.com"]
        }

def save_location(rotonde_file): 
    settings = {}
    rotonde_path = os.path.abspath(rotonde_file)
    # supplied path didn't contain a json file
    if rotonde_path.find(".json") < 0:
        print "assuming rotonde.json as name of rotonde file..."
        print "remembering path to rotonde file as", rotonde_path
        rotonde_path = rotonde_path.rstrip("/")
        rotonde_path += "/rotonde.json"
    settings["rotonde location"] = rotonde_path
    print "saving {}..".format(rotonde_path)

    with open(settings_file, "w") as f:
        f.write(json.dumps(settings))
    print "saved!"

def write(msg):
    rotonde = get_rotonde()
    rotonde["feed"].append({"text": msg, "time": str(int(time.time()))})
    save_rotonde(rotonde)
    print "published '{}'".format(msg)

def get_rotonde():
    # fetch the location of your rotonde file
    settings = load_settings()
    # get the contents of your rotonde file
    try:
        with open(settings["rotonde location"]) as f:
            rotonde = json.loads(f.readlines()[0])
    except IOError as e:
        print "couldn't find rotonde file {}; creating a default template".format(settings["rotonde location"])
        print
        print "please provide some details to fill it with"
        base["profile"]["name"] = raw_input("profile name: ")
        base["profile"]["location"] = raw_input("profile location: ")
        base["profile"]["color"] = raw_input("profile color (e.g #00000): ")
        return base
    return rotonde

def save_rotonde(rotonde):
    settings = load_settings()
    # get the contents of your rotonde file
    with open(settings["rotonde location"], "w") as f:
        f.write(json.dumps(rotonde))
    return rotonde

def load_settings():
    # fetch the location of your rotonde file
        with open(settings_file) as f:
            settings = json.loads(f.readlines()[0])
            return settings

def check_settings():
    try:
        with open(settings_file) as f:
            pass
    except IOError as e:
       print "no settings file detected; please run\n\trotonde.py save <location of your rotonde.json>"
       sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "supply a command -\n\twrite <msg>\n\tsave <rotonde.json location>"
        check_settings()
    elif len(sys.argv) == 2:
        print "not enough parameters"
    else:
        command = sys.argv[1]
        data = sys.argv[2]
        if command == "write": 
            check_settings()
            write(data)
        elif command == "save": save_location(data)
