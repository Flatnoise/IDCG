import os
import json
import idcg_common
import sys
from os import path
from PyQt5 import QtCore, QtGui, QtWidgets
from UI_GalaxyMap import Ui_MainWindow



class SimpleViewerSettings:
    """
    This class contains all global setting for this application
    """
    def __init__(self):
        self.resolutionX = 1024     # Windows default dimentios
        self.resolutionY = 700
        self.inputJSON = 'new_galaxy.json'  # Name of input file
        # Main directories
        self.dir_main = path.dirname(os.path.realpath(__file__))
        self.dir_resources = path.join(self.dir_main, 'resources')
        self.dir_images = path.join(self.dir_resources, 'images')

        self.starSystemFrameSize = 80       # Size of each star system graphic representation
        self.starSystemSpace = 150          # Distance between star systems


    # Print all setting, one parameter for one line
    def __str__(self):
        seq = ("Default window size:\t" + str(self.resolutionX) + "x" + str(self.resolutionY),
               "Input\t" + self.inputJSON,
               "Main dir:\t" + self.dir_main,
               "Resources dir\t" + self.dir_resources,
               "Images dir\t" + self.dir_images,
               "Size of each star frame, px: " + str(self.starSystemFrameSize),
               "Stars grid size, px: " + str(self.starSystemSpace))
        return '\n'.join(seq)

class GalaxyMapMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Graphic representation of main window with galaxy map
    """
    def __init__(self):
        super(GalaxyMapMainWindow, self).__init__()
        self.setupUi(self)

        # Calculate window position
        screen_resolution = app.desktop().screenGeometry()
        screen_width, screen_height = screen_resolution.width(), screen_resolution.height()
        # left upper corner coordinates
        luCornerX = int(screen_width / 2 - settings.resolutionX / 2)
        luCornerY = int(screen_height / 2 - settings.resolutionY / 2)
        self.setGeometry(luCornerX, luCornerY, settings.resolutionX, settings.resolutionY)

        # self.scrollerFrame.setStyleSheet("background-color: rgb(0, 255, 0)")
        self.galaxyMapFrame.setStyleSheet("background-color: rgb(0, 0, 0)")
        self.infoPanelFrame.setStyleSheet("background-color: rgb(255, 255, 200)")

        # Correction parameter for topleft corner of star's positions
        self.galaxyMapFrame.shiftX = -50
        self.galaxyMapFrame.shiftY = -50



        self.stars = []     # list of star's frames. Only graphic representation, do not miss with main stars list!
        max_starX = -1      # Rightmost star's position in grid
        max_starY = -1      # Downmost star's position on grid
        # Looping through main stars list, creating small frames, one for each star system
        for star in stars:
            sid = starsIndex[star.id]       # Get index from list
            square = StarSystemFrame(self.galaxyMapFrame, star.id)
            if star.x > max_starX: max_starX = star.x
            if star.y > max_starY: max_starY = star.y

            square.move(star.x * settings.starSystemSpace + self.galaxyMapFrame.shiftX,
                        star.y * settings.starSystemSpace + self.galaxyMapFrame.shiftY)
            self.stars.append(square)

        # Set size of galaxy map frame
        self.galaxyMapFrame.setFixedSize(QtCore.QSize(max_starX * settings.starSystemSpace + 90,
                                                     max_starY * settings.starSystemSpace + 90))

    def resizeEvent(self, resizeEvent):
        """
        Event: resize main window
        :param resizeEvent:
        :return:
        """
        # Adjust dimensions of scroll area with galaxy map frame
        self.scrollArea1.setFixedSize(QtCore.QSize(self.scrollerFrame.width(),
                                                     self.scrollerFrame.height()))



class StarSystemFrame(QtWidgets.QFrame):
    """
    Main frame for star system
    Icon of star, text label with name, other icons will be drawn here
    """
    def __init__(self, parent, sid):
        super().__init__(parent)

        # Calculate position of system in list
        lpos = starsIndex[sid]

        # Resize frame
        self.resize(settings.starSystemFrameSize, settings.starSystemFrameSize)

        # Calculating center of frame
        centerX = int(self.height()/2)
        centerY = int(self.width()/2)

        # Text label with name of the star
        label = QtWidgets.QLabel(stars[lpos].name, self)
        label.move (1,65)
        label.setText(stars[lpos].name)
        label.setStyleSheet("color: rgb(255, 255, 255)")

        # Icon with star
        pix = QtGui.QPixmap(self.selectStarImage(stars[lpos].star_type))
        img = QtWidgets.QLabel('',self)
        img.setPixmap(pix)
        img.move(centerX - int(pix.width()/2), centerY - int(pix.height()/2))

        # Writing IDs
        self.id = sid

    def selectStarImage(self, type):
        """
        This function return a path to a star's icon depending on type of star
        """
        if type == 1: filename = "icon_star_o.png"
        elif type == 2: filename = "icon_star_b.png"
        elif type == 3: filename = "icon_star_a.png"
        elif type == 4: filename = "icon_star_f.png"
        elif type == 5: filename = "icon_star_g.png"
        elif type == 6: filename = "icon_star_k.png"
        elif type == 7: filename = "icon_star_m.png"
        else: filename = "icon_star_m.png"
        return path.join(settings.dir_images, filename)

    def mousePressEvent(self, event):
        """
        This event is handling clicks on star systems
        """
        print(self.id, stars[starsIndex[self.id]].name)


# Load default settings
settings = SimpleViewerSettings()

# Input .JSON filename with path
json_input_filename = path.join(settings.dir_main, settings.inputJSON)

# Creating list of star systems and load JSON with data
stars = []
with open(json_input_filename, 'r') as json_input:
    json_data = json.load(json_input)
    json_input.close()

# Importing stars data from input savefile to list of stars
for item in json_data:
    stars.append(idcg_common.import_star(item))

# Create dictionary for fast search of star's indexed by IDs
starsIndex = idcg_common.index_StarSystems(stars)

app = QtWidgets.QApplication(sys.argv)
galaxyMap = GalaxyMapMainWindow()
galaxyMap.show()

galaxyMap.resize(1024,701)  # Crutch. To redraw windows right after start

sys.exit(app.exec_())