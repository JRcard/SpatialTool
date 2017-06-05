#!/usr/bin/env python
# encoding: utf-8
import math
from Constants import *
from pyo import *
import Variables as vars

savefile([[0,0,0,0],[0,0,0,0]], EMPTY_AUDIO_FILE, channels=2)

class Audio():
    def __init__(self, driver, nchnls, numSpeakers): # FL 29/04/17

        self.driver = driver
        self.nchnls = nchnls # FL 29/04/17
        self.numSpeakers = numSpeakers # FL 29/04/17
        
#        pref = vars.getVars("Pref") FL 29/05/17
#        self.server = Server(sr=44100, nchnls=self.nchnls, buffersize=512).boot() FL 29/05/17
        self.server = Server(sr=44100, nchnls=self.nchnls, buffersize=512) #FL 29/05/17
        self.server.setOutputDevice(self.driver) #FL 29/05/17
        self.server.boot() # FL 29/05/17
        time.sleep(1) # FL 29/05/17
        
        self.table = SndTable(EMPTY_AUDIO_FILE) # JR 31 mai 2017

        
        # Player et canaux individuelles.
        self.player = SfPlayer(EMPTY_AUDIO_FILE, speed=1, loop=False, offset=0, interp=2, mul=1, add=0)
        self.left = Sig(self.player[0])
        self.right = Sig(self.player[1])

        # Liste d'amplitude pour chaque canal d'entré relatif au nombre de canaux de sortie.
#        numSpk = pref["NUM_SPEAKERS"] FL 29/05/17
        for i in range(self.numSpeakers): # FL 29/05/17
            blueAmp = SigTo(value=0.0, time=0.1) 
            redAmp = SigTo(value=0.0, time=0.1)
            BLUEAMPLIST.append(blueAmp)
            REDAMPLIST.append(redAmp)

        # Valeur de départ, Avant(gauche-droite).
        self.setBlueAmp(0,1)
        self.setRedAmp(1,1)
        
        # OUTPUTS
        self.outBlue = Mix(self.left, voices=self.numSpeakers, mul=BLUEAMPLIST).out()
        self.outRed = Mix(self.right, voices=self.numSpeakers, mul=REDAMPLIST).out()

        self.ampAnal = PeakAmp(self.outBlue+self.outRed)
        self.server.start()

    def registerMeter(self, meter):
        self.ampAnal.setFunction(meter.setRms)

    def changeSnd(self, snd):
        self.player.path = snd
        self.table.path = snd # JR 31 mai 2017
        
        # Marche pas......... JR 1 juin 2017
#        waveform = vars.getVars("Waveform")
#        waveform.setRange(0,self.table.getDur(False))
        
    # mise à niveau des listes d'amplitude en lien avec les distances calculées dans SURFACE.
    def setBlueAmp(self,i,amp):
        blueAmp = BLUEAMPLIST[i]
        blueAmp.value = math.sqrt(amp)

    def setRedAmp(self,i,amp):
        redAmp = REDAMPLIST[i]
        redAmp.value = math.sqrt(amp)
