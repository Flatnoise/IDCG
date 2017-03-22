import socket
# import ssh
import json
import argparse
from os import path
import idcg_common

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
    def __init__(self, logging = 1, port = 26500, hosts = '', useSSL = 0, buffSize = 1024,
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
parser.add_argument('--logging', help="Logging level", type=int, default=2)
args = parser.parse_args()

# Load setting here
try:
    settings = loadSettings(args.config)
except:
    settings = ServerSettings()
    print("Error loading configuration! Using default config")
    print(settings)


inputSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
inputSocket.bind((settings.hosts, settings.port))
inputSocket.listen(10)

while True:
    clientSocket, address = inputSocket.accept()
    print("Connected from:\t", address)
    while True:


    # PLACEHOLDER
        data = clientSocket.recv(settings.buffSize)
        if not data: break
        udata = data.decode('utf8')
        print (udata)
        if udata == 'S':
            clientSocket.close()
        else:
            clientSocket.send(bytes("-= " + udata + " =-", 'utf8'))



#inputSocket.close()



