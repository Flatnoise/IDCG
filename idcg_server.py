import json
import argparse
from os import path
import idcg_common
import logging
import json


def loadSettings(config_filename):
    """
    Load server setting from JSON file;
    Put them into settings object from ServerSettings class
    """
    with open(config_filename, 'r') as settings_file:
        settings_data = json.load(settings_file)
        settings_file.close()

    # Check if config has only one set of settings
    # Use default settings otherwise
    if len(settings_data) == 1:
        tmp = settings_data[0]

        return ServerSettings(
            logging=tmp['logging'],
            port = tmp['port'],
            hosts = tmp['allowed_hosts'],
            useSSL = tmp['useSSL'],
            buffSize = tmp['buffSize'],
            serverLog = tmp['serverLog'],
            msgLog = tmp['msgLog']
        )
    else:
        return ServerSettings()

class ServerSettings:
    """
    This class is for storing server settings
    """
    def __init__(self, logging = 30, port = 26500, hosts = '', useSSL = 0, buffSize = 1024,
                 serverLog = 'server.log', msgLog = 'messages.log'):
        self.logging = logging
        self.port = port
        self.hosts = hosts

        if useSSL == 0: self.useSSL = False
        elif useSSL == 1: self.useSSL = True
        else: self.useSSL = False

        if buffSize < 1: buffSize = 1024
        self.buffSize = buffSize

        self.dir_main = path.dirname(path.realpath(__file__))
        self.serverLog = path.join(self.dir_main, serverLog)
        self.msgLog = path.join(self.dir_main, msgLog)

    def __str__(self):
        seq = ("Logging level:\t" + str(self.logging),
               "Port:\t" + str(self.port),
               "Allowed hosts:\t" + str(self.hosts),
               "Use SSL:\t" + str(self.useSSL),
               "Buffer size:\t" + str(self.buffSize),
               "Working dir:\t" + self.dir_main,
               "Server log:\t" + self.serverLog,
               "Messages log:\t" + self.msgLog)
        return '\n'.join(seq)



#Parsing command-line parameters
# USAGE: idcg_server [parameters]
# --input <JSON FILE>
# --logging <NUMBER>
parser = argparse.ArgumentParser(description="IDCG server",
                                 usage='idcg_server [options]')
parser.add_argument('--input', help="name of starging input savefile, JSON", default="new_galaxy.json")
parser.add_argument('--config', help="name of configuration file, JSON", default="config.json")
parser.add_argument('--logging', help="Logging level", type=int, default=30)
args = parser.parse_args()


# Configure logging

# Load setting here
try:
    settings = loadSettings(args.config)
except:
    settings = ServerSettings()
    print("Error loading configuration! Using default config")
    print(settings)

# Configure logger
logging.basicConfig(format = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s', level = settings.logging,
                    filename = settings.serverLog)


# Input .JSON filename with path
json_input_filename = path.join(settings.dir_main, args.input)

# Load JSON with data
with open(json_input_filename, 'r') as json_input:
    json_data = json.load(json_input)
    json_input.close()

# Creating lists with starSystems and wormholes
stars = []
wormholes = []

# Importing stars data from input savefile to list of stars
for item in json_data:
    if item['object_type'] == 1:
        stars.append(idcg_common.import_star(item))
    elif item['object_type'] == 2:
        wormholes.append(idcg_common.import_wormhole(item))

# Create dictionary for fast search of star's indexed by IDs
starIndex = idcg_common.index_StarSystems(stars)

# for star in stars:
#     print (star)
#     for planet in stars[starIndex[star.id]].planets:
#             print(planet.printPlanet())
#



inputSocket = idcg_common.JsonServer(settings.hosts, settings.port)
inputSocket.acceptConnection()

try:
    while True:
        data = inputSocket.readObj()

        if data == '':
            break
        else:
            json_data = json.loads(data)

            # Creating lists with starSystems and wormholes
            stars = []
            wormholes = []

            # Importing stars data from input savefile to list of stars
            for item in json_data:
                if item['object_type'] == 1:
                    stars.append(idcg_common.import_star(item))
                elif item['object_type'] == 2:
                    wormholes.append(idcg_common.import_wormhole(item))

            for star in stars:
                print(star)
                for planet in star.planets:
                    print(planet.printPlanet())

            for wormhole in wormholes:
                print(wormhole)


            inputSocket.sendObj(data)

finally:
    inputSocket.close()

