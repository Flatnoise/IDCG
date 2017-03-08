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

class StarSystem:
    """Main star system definition"""
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
    """Main wormhole definition"""
    def __init__(self, sid, star1_id, x1, y1, star2_id, x2, y2, length):
        self.id = sid
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.star1_id = star1_id
        self.star2_id = star2_id
        self.length = length

    def __str__(self):
        seq = (str(self.id), str(self.star1_id), str(self.x1), str(self.y1),
               str(self.star2_id), str(self.x2), str(self.y2), str(self.length))
        return '\t'.join(seq)