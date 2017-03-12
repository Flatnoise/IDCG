"""

Common classes and functions for all IDCG programs and utilites

"""

def jsonDefault(object):
    """
    default JSON object, for correct output of JSON to file
    """
    return object.__dict__

def import_star(json_string):
    """
    Converts a single JSON string to a StarSystem instance
    :param json_string:
    :return:
    """
    return StarSystem(json_string['id'], json_string['name'], json_string['x'], json_string['y'],
                                  json_string['star_type'], json_string['nation_prime'], json_string['nation_sec'])

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
    def __init__(self, sid, name, x, y, star_type, nation_prime, nation_sec):
        self.id = sid
        self.name = name
        self.x = x
        self.y = y
        self.star_type = star_type
        self.nation_prime = nation_prime
        self.nation_sec = nation_sec

    def __str__(self):
        seq = (str(self.id), str(self.x), str(self.y),
               str(self.star_type), str(self.nation_prime), str(self.nation_sec), self.name)
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

    def __str__(self):
        seq = (str(self.id), str(self.star1_id), str(self.x1), str(self.y1),
               str(self.star2_id), str(self.x2), str(self.y2), str(self.length))
        return '\t'.join(seq)
