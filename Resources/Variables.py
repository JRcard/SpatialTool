# encoding: utf-8
#JR Start 

# Dictionnaire qui enregistre les references des differents objets
# du programme. Cela permet un acces simple et efficace a n'importe
# quel objet de n'importe ou dans le programme.
vars = {}
vars["Surface"] = None
vars["Audio"] = None
vars["MainFrame"] = None
vars["OSCServer"] = None
vars["Speakers"] = []
vars["Speakers_setup"] = [] # [(x, y), (x, y), ...]
vars["Pref"] = {"NCHNLS": "","NUM_SPEAKERS": "", "OSCPORT": ""}
# Enregistre une reference dans le dictionnaire.
def setVars(key, obj):
    vars[key] = obj
    
# Recupere une reference dans le dictionnaire.
#def getVars(key):
#    return vars.get(key, None)
def getVars(key):
    return vars.get(key, None)
    
#JR END