# encoding: utf-8
import math
from Constants import *
from pyo import *


savefile([[0,0,0,0],[0,0,0,0]], EMPTY_AUDIO_FILE, channels=2)


class Audio():
    def __init__(self):

        self.server = Server(sr=44100, nchnls=NCHNLS, buffersize=512).boot()

        # Player et canaux individuelles.
        self.player = SfPlayer(EMPTY_AUDIO_FILE, speed=1, loop=False, offset=0, interp=2, mul=1, add=0)
        self.left = Sig(self.player[0])
        self.right = Sig(self.player[1])

        # Liste d'amplitude pour chaque canal d'entré relatif au nombre de canaux de sortie.
        for i in range(NUM_SPEAKERS):
            blueAmp = SigTo(value=0.0, time=0.1) # l'ajout d'un controle sur le Time serait bien
            redAmp = SigTo(value=0.0, time=0.1)
            BLUEAMPLIST.append(blueAmp)
            REDAMPLIST.append(redAmp)

        # Valeur de départ, Avant(gauche-droite).
        self.setBlueAmp(0,1)
        self.setRedAmp(1,1)
        
        # OUTPUTS
        self.outBlue = Mix(self.left, voices=NUM_SPEAKERS, mul=BLUEAMPLIST).out()
        self.outRed = Mix(self.right, voices=NUM_SPEAKERS, mul=REDAMPLIST).out()

        self.ampAnal = PeakAmp(self.outBlue+self.outRed)

    def registerMeter(self, meter):
        self.ampAnal.setFunction(meter.setRms)

    def changeSnd(self, snd):
        self.player.path = snd

    # mise à niveau des listes d'amplitude en lien avec les distances calculées dans SURFACE.
    def setBlueAmp(self,i,amp):
        blueAmp = BLUEAMPLIST[i]
        blueAmp.value = math.sqrt(amp)
        #print "blue", blueAmp.value

    def setRedAmp(self,i,amp):
        redAmp = REDAMPLIST[i]
        redAmp.value = math.sqrt(amp)

