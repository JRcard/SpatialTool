# encoding: utf-8
import os, math

#SPEAKERS = []
BLUEAMPLIST = []
REDAMPLIST = []

#NCHNLS =  2 # FL 23/05/2017
#NCHNLS = int(pref["NCHNLS"]) # JR 24 mai 2017
NCHNLS_LIST = ["2", "4", "8"] # JR 23 mai 2017

CIRCLE_RADIUS = 10
SPEAKER_RADIUS = 15

# JR 25 mai 2017
#NUM_SPEAKERS = ""
#TYPE = "A" 

# Liste pour le l'utilisateur
SPEAKERS_SETUP_LIST = ["Stereo", "Quad", "Octo-Left-Right", "Octo-Front-Back"] # FL 26/05/17
#SPEAKERS_SETUP_LIST = ["", "Stereo", "Quad", "Octo-Left-Right", "Octo-Front-Back"] # JR 23 mai 2017


SETUP_STEREO = [(100, 100), (500, 100)]
SETUP_QUAD = [(100, 100), (500, 100), (500,500), (100, 500)]
SETUP_OCTO_DIAMAND = [(100,100),(300,20),(500,100),(580,300),
                      (500,500),(300,580),(100,500),(20,300)]
                      
SETUP_OCTO_STEREO = [(175,50),(425,50),(550,175),(550,425),
                     (425,550),(175,550),(50,425),(50,175)]

GRID_WIDTH = 600
GRID_HEIGHT = 600

COLOR_BLUE = "#0C456F"
COLOR_RED = "#DD3636"
COLOR_AV = "#888888"
COLOR_AR = "#888888"
COLOR_GRID = "#555555"
COLOR_BACK = "#000000"
COLOR_MAIN = "#222222"

# Distance entre le centre du speaker gauche et droit
#DIAGONAL = math.sqrt(math.pow((78-78),2.) + math.pow((523-78),2.)) # JR 25 mai 2017


# Dossier appartenant au programme. 
TEMP_PATH = os.path.join(os.path.expanduser("~"), ".Spatial")

# s'il n'existe pas on le cree
if not os.path.isdir(TEMP_PATH):
    os.mkdir(TEMP_PATH)

# Fichier audio contenant du silence
EMPTY_AUDIO_FILE = os.path.join(TEMP_PATH, "Spatial_temp.wav")
# Fichier musical
TESTFILE = '/Users/Jrcard/Google Drive/Jeremie_Ricard_Darkest_Fear.wav'
# Préférences
PREFERENCES = os.path.join(TEMP_PATH, "Preferences.txt")

