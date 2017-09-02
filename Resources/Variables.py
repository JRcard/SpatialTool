#!/usr/bin/env python
# encoding: utf-8

# Dictionnaire qui enregistre les references des differents objets
# du programme. Cela permet un acces simple et efficace a n'importe
# quel objet de n'importe ou dans le programme.
vars = {}
vars["Surface"] = None
vars["Audio"] = None
vars["MainFrame"] = None
vars["OSCServer"] = None
vars["Waveform"] = None # JR 1 juin 2017
vars["Speakers"] = []
vars["Speakers_setup"] = [] # [(x, y), (x, y), ...]
vars["Pref"] = {"AUDIO_DRIVER": "None", "NCHNLS": "2","SPEAKERS_SETUP": 0, "NUM_SPEAKERS": 2, "OSCPORT": "5555"} # FL 29/05/17

# Enregistre une reference dans le dictionnaire.
def setVars(key, obj):
    vars[key] = obj
    
# Recupere une reference dans le dictionnaire.
def getVars(key):
    return vars.get(key, None)
    