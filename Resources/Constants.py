#!/usr/bin/env python
# encoding: utf-8
import os, math

#SPEAKERS = []
BLUEAMPLIST = []
REDAMPLIST = []
BLUE_START = [0.1667, 0.1667]
RED_START = [0.8333, 0.1667]

#NCHNLS =  2 # FL 23/05/2017
#NCHNLS = int(pref["NCHNLS"]) # JR 24 mai 2017
NCHNLS_LIST = ["2", "4", "8"] # JR 23 mai 2017

CIRCLE_RADIUS = 10
GRID_CIRCLE_RADIUS = 10
SPEAKER_RADIUS = 15
INIT_SOUND_RADIUS = 20

# JR 25 mai 2017
#NUM_SPEAKERS = 2
TYPE = "A" 

# Liste pour le l'utilisateur
SPEAKERS_SETUP_LIST = ["Stereo", "Quad", "Octo-Left-Right", "Octo-Front-Back"] # FL 26/05/17

# FL START 02/09/2017
# On utilise des proportions pour pouvoir adapter l'écran à toutes les tailles de moniteurs.
SETUP_STEREO = [(0.1667, 0.1667), (0.8333, 0.1667)]
SETUP_QUAD = [(0.1667, 0.1667), (0.8333, 0.1667), (0.8333,0.8333), (0.1667, 0.8333)]
SETUP_OCTO_DIAMAND = [(0.1667,0.1667),(0.5,0.0333),(0.8333,0.1667),(0.9667,0.5),
                      (0.8333,0.8333),(0.5,0.9667),(0.1667,0.8333),(0.0333,0.5)]
                      
SETUP_OCTO_STEREO = [(0.2917,0.0833),(0.7083,0.0833),(0.9167,0.2917),(0.9167,0.7083),
                     (0.7083,0.9167),(0.2917,0.9167),(0.0833,0.7083),(0.0833,0.2917)]
                     
# FL END 02/09/2017

#SETUP_STEREO = [(100, 100), (500, 100)]
#SETUP_QUAD = [(100, 100), (500, 100), (500,500), (100, 500)]
#SETUP_OCTO_DIAMAND = [(100,100),(300,20),(500,100),(580,300),
#                      (500,500),(300,580),(100,500),(20,300)]
#                      
#SETUP_OCTO_STEREO = [(175,50),(425,50),(550,175),(550,425),
#                     (425,550),(175,550),(50,425),(50,175)]
                     
# FL 02/09/2017
GRID_WIDTH = 0.65
GRID_HEIGHT = 0.65
#GRID_WIDTH = 635
#GRID_HEIGHT = 635

COLOR_BLUE = "#0C456F"
COLOR_RED = "#DD3636"
COLOR_AV = "#888888"
COLOR_AR = "#888888"
COLOR_GRID = "#555555"
COLOR_BACK = "#000000"
COLOR_MAIN = "#222222"

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

