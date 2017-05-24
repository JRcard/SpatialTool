#!/usr/bin/env python
# encoding: utf-8
from pyo import *
import Variables as vars
# Fonctions bidons pour fins de tests

#*************************************************************************************
# 22/05/2017 - Francis Lecavalier
# Suppression des fonctions bidons et ajout de fonctions appelant la nouvelle fonction OSCMove de "Surface.py".
# Les boules et leurs positions seront modifiées dans le fichier "Surface.py", afin de compartimenter
# davantage OSCServer.
#*************************************************************************************

# FL 22/05/2017 
# J'ai supprimé les fonctions bidons puisqu'ils n'étaient là que pour l'exemple

# JR START 21 mai    
def function5(data):
#    print "PadL: " + str(data)
        surface = vars.getVars("Surface")
        surface.OSCMove(0, x=data)
    
    
# JR END 21 mai

class OSCServer:
    def __init__(self):
        #Dictionnaire avec fonctions associées à chaque message OSC reçu.
        self.bindings = {"/stickL/x": self.stickLeftXMove, "/stickL/y": self.stickLeftYMove, "/stickR/x": self.stickRightXMove, "/stickR/y": self.stickRightYMove, "/padL": function5} # FL 22/05/17
        #Objet OscListener de Pyo permet de gérer l'OSC dans un thread indépendant de l'audio. On peut donc gérer l'OSC même si le moteur audio n'est pas démarré
        self.listen = OscListener(self._oscrecv, 5555)
        self.listen.start()
        print "go!"
    # Fonction appelée à chaque fois qu'on message OSC est reçu
    def _oscrecv(self, address, *args):
        #print address, args
        # Si le message OSC est listé dans notre dictionnaire, on appele la fonction associée
        if address in self.bindings:
            # junXion retourne des tuples commes arguments OSC, même si on n'envoie qu'une seule valeur. On va donc chercher la première valeur du tuple (un float)
            self.bindings[address](args[0])
            
    # FL START 22/05/17
    def stickLeftXMove(self, data):
#        print "Left X: " + str(data)
        surface = vars.getVars("Surface")
        surface.OSCMove(0, x=data)
    
    def stickLeftYMove(self, data):
#        print "Left Y: " + str(data)
        surface = vars.getVars("Surface")
        surface.OSCMove(0, y=data)
        
    def stickRightXMove(self, data):
#        print "Right X: " + str(data)
        surface = vars.getVars("Surface")
        surface.OSCMove(1, x=data)
        
    def stickRightYMove(self, data):
#        print "Right Y: " + str(data)
        surface = vars.getVars("Surface")
        surface.OSCMove(1, y=data)
    #FL END 22/05/17
         
# JR 21 mai        
#s = Server().boot()
#osc = OSCServer()
#s.gui(locals())
