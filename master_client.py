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

        return MasterClientSettings(
            logging=tmp['logging'],
            port = tmp['port'],
            server = tmp['server'],
            useSSL = tmp['useSSL'],
            clientLog = tmp['clientLog']
        )
    else:
        return MasterClientSettings()

class MasterClientSettings:
    """
    This class is for storing master client settings
    """
    def __init__(self, logging = 1, port = 26500, server = 'localhost', useSSL = 0, clientLog = 'master_client.log'):
        self.logging = logging
        self.port = port
        self.server = server

        if useSSL == 0: self.useSSL = False
        elif useSSL == 1: self.useSSL = True
        else: self.useSSL = False

        self.dir_main = path.dirname(path.realpath(__file__))
        self.clientLog = path.join(self.dir_main, clientLog)

    def __str__(self):
        seq = ("Logging level:\t" + str(self.logging),
               "Port:\t" + str(self.port),
               "Server address:\t" + str(self.server),
               "Use SSL:\t" + str(self.useSSL),
               "Client log:\t" + self.clientLog)
        return '\n'.join(seq)


#Parsing command-line parameters
# USAGE: idcg_server [parameters]
# --input <JSON FILE>
# --logging <NUMBER>
parser = argparse.ArgumentParser(description="IDCG server",
                                 usage='idcg_server [options]')
parser.add_argument('--config', help="name of configuration file, JSON", default="client_config.json")
parser.add_argument('--logging', help="Logging level", type=int, default=2)
args = parser.parse_args()

# Load setting here
try:
    settings = loadSettings(args.config)
except:
    settings = MasterClientSettings()
    print("Error loading configuration! Using default config")
    print(settings)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((settings.server, settings.port))

# PLACEHOLDER

data = b'SOME TEST or not some test?'
client_socket.sendall(data)

rdata = client_socket.recv(1024)
client_socket.close()
print('Received', repr(rdata))






