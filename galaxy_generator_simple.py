# Simple galaxy generator
# Just for test use

output_version = 1  # Version of output format


import argparse
import random
import string
import json
import idcg_common

max_wh_range = 19  # Maximum wormhole range


class StarSystem(idcg_common.StarSystem):
    """
    Star system class with additions, needed only for galaxy generation
    """
    def __init__(self, sid, name, x, y, star_type, nation_prime, nation_sec, special1, special2):
        super().__init__(sid, name, x, y, star_type, nation_prime, nation_sec, special1, special2)

        # Set maximum allowed number of wormhole depending on star type
        if star_type == 1: self.max_wormholes = 8
        elif star_type == 2: self.max_wormholes = 8
        elif star_type == 3: self.max_wormholes = 6
        elif star_type == 4: self.max_wormholes = 6
        elif star_type == 5: self.max_wormholes = 4
        elif star_type == 6: self.max_wormholes = 3
        elif star_type == 7: self.max_wormholes = 2
        else: self.max_wormholes = 2

        # Number of unused wormhole nodes
        self.free_nodes = self.max_wormholes

        self.special1 = special1
        self.special2 = special2



#Parsing command-line parameters
# USAGE: galaxy_generator_simple.py [parameters]
# --width <WIDTH OF GALAXY IN POINTS>
# --height <WIDTH OF GALAXY IN POINTS>
# --dict <TEXT FILE> - file with stat names
# --out <JSON FILE> - output savefile
parser = argparse.ArgumentParser(description="Simple Galaxy Generator for IDCG",
                                 usage='galaxy_generator_simple.py [options]')

parser.add_argument('--width', help="Galaxy width, default 110", type=int, default=110)
parser.add_argument('--height', help="Galaxy height, default 110", type=int, default=110)
parser.add_argument('--dict', help="Specify text file with star names, default star_names.txt",
                    default='star_names.txt')
parser.add_argument('--out', help="Output file", default='new_galaxy.json')
args = parser.parse_args()

# Minimal allowed size if 50x50
glx_width = 50 if args.width < 50 else args.width
glx_height = 50 if args.height < 50 else args.height

# Maximum allowed size if 1100x1100
glx_width = 1100 if glx_width > 1100 else glx_width
glx_height = 1100 if glx_height > 1100 else glx_height

# Read content of file with star's names
star_names = []
with open(args.dict,'r') as file:
    for line in file:
        if line.strip():
            if line[-1] == '\n':
                star_names.append(line[:-1])
            else:
                star_names.append(line)
file.close()


# Counting stars
# This is very simple star system generator
# Stars are placed in grid with 10 units squares
max_stars = int((glx_width / 10 - 1) * (glx_height / 10 - 1))

# Append random star names if the list if too short
while max_stars > len(star_names):
    star_names.append((''.join(random.choices(string.ascii_uppercase, k=4))) + '-' +
                      (''.join(random.choices(string.digits, k=7))))


# Generating stars
tmp_indx1 = 0
tmp_indx2 = 0

stars = []  # main list of all star systems

# Iterating through coord.grid with step of 10
for itr_x in range(1, int(glx_width / 10)):
    for itr_y in range(1, int(glx_height / 10)):
        # Getting random name from list of names;
        # Deleting name from the list after that
        rnd_index = random.randrange(0, len(star_names))
        rnd_starname = star_names[rnd_index]
        del star_names[rnd_index]

        # Create index and StarSystem parameters
        tmp_indx1 += 1

        # Other parameters
        nation_prime = 1    # All stars are assigned to player at this moment
        nation_sec = 1
        star_type = random.randrange(1,7)   # Generate random startype
        special1 = 0                        # Specials; both not used at this moment
        special2 = 0

        # Creating instance and adding it to an list of systems
        tmp_star = StarSystem(tmp_indx1, rnd_starname, itr_x * 10, itr_y * 10,
                              star_type, nation_prime, nation_sec, special1, special2)

        # generating planets
        planets_count = random.randrange(2,4)

        for tmp_indx3 in range(1, planets_count):
            tmp_indx2 += 1

            # Create planetName
            if tmp_indx3 == 1: planetName = 'I'
            elif tmp_indx3 == 2: planetName = 'II'
            elif tmp_indx3 == 3: planetName = 'IIII'
            elif tmp_indx3 == 4: planetName = 'IV'
            elif tmp_indx3 == 5: planetName = 'V'
            elif tmp_indx3 == 6: planetName = 'VI'
            elif tmp_indx3 == 7: planetName = 'VII'
            elif tmp_indx3 == 8: planetName = 'VIII'
            elif tmp_indx3 == 9: planetName = 'IX'
            planetName = rnd_starname + ' ' + planetName

            planetType = random.randrange(1,14)
            if planetType != 13:
                planetSize = random.randrange(4,21)
                density = round(random.random() * 2.3 + 0.1, 2)
            else:
                planetSize = random.randrange(20,51)
                density = round(random.random() * 0.7 + 0.1, 2)

            gravity = round(planetSize / 10 * density, 2)

            # Calculate atmosphere
            if planetType <= 7:
                pressure = round(random.random() * 1.4 + 0.4, 2)
            elif planetType == 8:   # Arid
                pressure = round(random.random() * 0.4 + 0.1, 2)
            elif planetType == 9 or planetType == 10: # Barren, frozen
                pressure = round(random.random() * 0.2, 2)
                if pressure < 0.1: pressure = 0
            elif planetType == 11:  # Molten
                pressure = round(random.random() * 2, 2)
            elif planetType == 12:  # Toxix
                pressure = round(random.random() * 3 + 1, 2)
            elif planetType == 13:  # Gaz Giant
                pressure = round(random.random() * 9 + 1, 2)

            tmp_planet = idcg_common.Planet(tmp_indx2, tmp_indx1, planetName, planetType, planetSize, pressure, gravity)
            tmp_star.planets.append(tmp_planet)



        stars.append(tmp_star)


# Creating index of star systems
starIndex = idcg_common.index_StarSystems(stars)

# Generating wormholes
wormholes = []
tmp_indx = 0
for star in stars:

    # Creating list of all possible connections for particular star system
    pos_whls = []
    for star2 in stars:
        # Calculating range
        rng = idcg_common.calc_range(star.x, star.y, star2.x, star2.y)

        # Only neightboring systems can share wormhole
        # So I calculate distance and screen star that too far away
        # I also screen stars that don't have free wormhole nodes left
        if rng <= max_wh_range and rng > 0 and star2.free_nodes > 0:
            # print(star.name, "\t", star2.name, "\t", rng)
            pos_whls.append(star2.id)

    # Randomize list of possible wormholes
    random.shuffle(pos_whls)


    for whl in pos_whls:
        star2 = stars[starIndex[whl]]

        # Checking for unused nodes in both star systems
        if star.free_nodes > 0 and star2.free_nodes > 0:
            tmp_indx += 1   # This will be owr unique ID
            tmp_wormhole = idcg_common.Wormhole(tmp_indx, star.id, star2.id,
                                                int(idcg_common.calc_range(star.x, star.y, star2.x, star2.y)))
            wormholes.append(tmp_wormhole)

            # Correcting number of unused nodes in both systems
            star.free_nodes -= 1
            stars[starIndex[whl]].free_nodes -= 1

# Check for duplicates
for w1 in wormholes:
    for indx, w2 in enumerate(wormholes):
        if w1.id == w2.id: continue
        if ((w1.star1 == w2.star1 and w1.star2 == w2.star2) or
                (w1.star2 == w2.star1 and w1.star1 == w2.star2)):
            del wormholes[indx]



# Deleting unnecessary attributes to save space in JSON
for star in stars:
    del star.free_nodes
    del star.max_wormholes



# Merging all list for output in one JSON
output_list = stars + wormholes

# Writing all data to JSON file
with open(args.out, 'w', encoding='utf-8') as out_file:
    json.dump(output_list, out_file, ensure_ascii=True, indent="", default=idcg_common.json_default)
    out_file.close()