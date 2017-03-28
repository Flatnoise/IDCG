"""
Common classes and functions for all IDCG programs and utilites
"""

from math import sqrt
import logging
import socket

def jsonDefault(object):
    """
    default JSON object, for correct output of JSON to file
    """
    return object.__dict__

def import_star(json_string):
    """
    Converts a single JSON string to a StarSystem instance
    """
    tmp_star = StarSystem(json_string['id'], json_string['name'], json_string['x'], json_string['y'],
                      json_string['star_type'], json_string['nation_prime'], json_string['nation_sec'],
                      json_string['special1'], json_string['special2'])

    # Import planets list from JSON
    json_planets = json_string['planets']
    for json_planet in json_planets:
        planet = import_planet(json_planet)
        tmp_star.planets.append(planet)

    return tmp_star

def import_planet(json_string):
    """
    Converts a single JSON string to a Planet instance
    pid, sid, name, planet_type, planet_size, atm_pressure, gravity
    """
    return Planet(json_string['id'], json_string['star_id'], json_string['name'],
                  json_string['planet_type'], json_string['planet_size'],
                  json_string['atm_pressure'], json_string['gravity'])


def import_wormhole(json_string):
    """
    Converts a single JSON string to a StarSystem instance
    """
    return Wormhole(json_string['id'], json_string['star1'], json_string['star2'], json_string['length'])

def calcRange(x1, y1, x2, y2):
    """
    Calculate range between two point by their coordinates
    """
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)


def index_StarSystems(starSystems: list):
    """
    Returns a dictionary: StarSystem ID: Star System number in list
    :param object:
    :return:
    """
    indx = {}
    for number, star in enumerate(starSystems):
        indx[star.id] = number
    return indx


class StarSystem:
    """
    Main star system definition
    """
    def __init__(self, sid, name, x, y, star_type, nation_prime, nation_sec, special1, special2):
        self.object_type = 1    # Star system type
        self.id = sid
        self.name = name
        self.x = x
        self.y = y
        self.nation_prime = nation_prime    # Primary nation tag
        self.nation_sec = nation_sec        # Secondary nation tag; feudal domain for some lord, for example

        self.star_type = star_type          # Star class (O-B-A-F-G-K-M)
        self.special1 = special1            # First special for this system; Just the int number;
        self.special2 = special2            # Second special for this system; Just the int number;

        self.planets = []

    def __str__(self):
        seq = (str(self.id), str(self.x), str(self.y),
               str(self.star_type), str(self.nation_prime), str(self.nation_sec), self.name)
        return '\t'.join(seq)

    def addPlanet(self, planet):
        pass

class Planet:
    """
    Main definition of planet
    Planet types
    1   Terran
    2   Ocean
    3   Savanna
    4   Tundra
    5   Arctic
    6   Desert
    7   Jungle
    8   Arid
    9   Barren
    10  Frozen
    11  Molten
    12  Toxic
    13  Gaz giant
    """
    def __init__(self, pid, sid, name, planet_type, planet_size, atm_pressure, gravity):
        self.id = pid
        self.star_id = sid
        self.name = name
        self.planet_type = planet_type
        self.planet_size = planet_size
        self.atm_pressure = atm_pressure
        self.gravity = gravity


    def __str__(self):
        seq = (str(self.id), str(self.star_id), str(self.planet_type), str(self.planet_size),
               str(self.atm_pressure), str(self.gravity), self.name)
        return '\t'.join(seq)

    def printPlanet(self):
        if self.planet_type == 1: planetType = 'Terran'
        elif self.planet_type == 2: planetType = 'Ocean'
        elif self.planet_type == 3: planetType = 'Savanna'
        elif self.planet_type == 4: planetType = 'Tundra'
        elif self.planet_type == 5: planetType = 'Arctic'
        elif self.planet_type == 6: planetType = 'Desert'
        elif self.planet_type == 7: planetType = 'Jungle'
        elif self.planet_type == 8: planetType = 'Arid'
        elif self.planet_type == 9: planetType = 'Barren'
        elif self.planet_type == 10: planetType = 'Frozen'
        elif self.planet_type == 11: planetType = 'Molten'
        elif self.planet_type == 12: planetType = 'Toxic'
        elif self.planet_type == 13: planetType = 'Gas Giant'

        seq = ('ID ' + str(self.id),
               'StarID ' + str(self.star_id),
               planetType,
               'Size ' + str(self.planet_size),
               'Atm ' + str(self.atm_pressure),
               'Grav ' + str(self.gravity),
               self.name)
        return '\t'.join(seq)

class Wormhole:
    """
    Main wormhole definition
    star1, star2 - IDs of stars, connected by particular wormhole
    """
    def __init__(self, sid, star1_id, star2_id, length):
        self.id = sid
        self.star1 = star1_id
        self.star2 = star2_id
        self.length = length
        self.object_type = 2    # Wormhole type

    def __str__(self):
        seq = (str(self.id), str(self.star1), str(self.star2), str(self.length))
        return '\t'.join(seq)

class JsonSocket(object):
    def __init__(self, address='', port=26500):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = self.socket
        self._timeout = None
        self._address = address
        self._port = port


    def sendObj(self, msg):
        lenString = '%08i' % len(msg)
        self.conn.send(lenString.encode())
        self.conn.send(msg.encode())
        logging.debug("Data sent %d" % (len(msg)))


    def readObj(self):
        try:
            length = int(self.conn.recv(8))
            string = self.conn.recv(length)
            while len(string) < length:
                string += self.conn.recv(length - len(string))
            return string.decode()
            logging.debug("Data received %d" % (len(msg)))
        except:
            logging.error("Socket error")
            return ''

    def close(self):
        logging.debug("closing main socket")
        self.socket.close()
        if self.socket is not self.conn:
            logging.debug("closing connection socket")
            self.conn.close()






class JsonServer(JsonSocket):
    def __init__(self, address='', port=26500):
        super(JsonServer, self).__init__(address, port)
        self.socket.bind((address, port))

    def acceptConnection(self):
        self.socket.listen(10)
        self.conn, addr = self.socket.accept()
        logging.debug("connection accepted, conn socket (%s,%d)" % (addr[0], addr[1]))



class JsonClient(JsonSocket):
    def __init__(self, address='', port=26500):
        super(JsonClient, self).__init__(address, port)

    def connect(self, address, port):
        for i in range(10):
            try:
                self.socket.connect((address, port))
            except socket.error as msg:
                logging.error("SockThread Error: %s" % msg)
                time.sleep(3)
                continue
            logging.info("...Socket Connected")
            return True