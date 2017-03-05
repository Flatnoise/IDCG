# Simple galaxy generator
# Just for test use

output_version = 1  # Version of output format


import argparse
import random
import string

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

for line in star_names:
    print(line)



