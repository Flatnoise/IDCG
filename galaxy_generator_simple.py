# Simple galaxy generator
# Just for test use

output_version = 1  # Version of output format


import argparse
import random
import string
import json
import idcg_common



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
tmp_indx = 0
stars = []  # main list of all star systems

# Iterating through coord.grid with step of 10
for itr_x in range(1, int(glx_width / 10)):
    for itr_y in range(1, int(glx_height / 10)):
        # Getting random name from list of names;
        # Deleting name from the list after that
        rnd_index = random.randrange(0, len(star_names))
        rnd_starname = star_names[rnd_index]
        del star_names[rnd_index]

        # Create index and StarSystem object
        tmp_indx += 1
        tmp_star = idcg_common.StarSystem(tmp_indx, rnd_starname, itr_x, itr_y, random.randrange(1,7), 1, 1)
        stars.append(tmp_star)


# Generating wormholes
#for star in stars:



# Writing all data to JSON file
with open(args.out, 'w', encoding='utf-8') as out_file:
    json.dump(stars, out_file, ensure_ascii=True, indent="", default=idcg_common.jsonDefault)