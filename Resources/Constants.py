# encoding: utf-8
import os, math

#SPEAKERS = []
BLUEAMPLIST = []
REDAMPLIST = []

NCHNLS = 8

CIRCLE_RADIUS = 10
SPEAKER_RADIUS = 15

NUM_SPEAKERS = 8
TYPE = "A"

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
DIAGONAL = math.sqrt(math.pow((78-78),2.) + math.pow((523-78),2.)) 


# Dossier appartenant au programme. 
TEMP_PATH = os.path.join(os.path.expanduser("~"), ".radio")

# s'il n'existe pas on le cree
if not os.path.isdir(TEMP_PATH):
    os.mkdir(TEMP_PATH)

# Fichier audio contenant du silence
EMPTY_AUDIO_FILE = os.path.join(TEMP_PATH, "radio_tempfile.wav")
TESTFILE = '/Users/Jrcard/Google Drive/Jeremie_Ricard_Darkest_Fear.wav'

# OCS Port
PORT = 9900
