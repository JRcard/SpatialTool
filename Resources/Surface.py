#!/usr/bin/env python
# encoding: utf-8
import wx
import math
from Constants import *
from Widgets import *
import Variables as vars

#*************************************************************************************
# 23/05/2017 - Francis Lecavalier
# Implémentation du OSC dans l'application. Fonction "OSCMove" reçoit les message du
# OSCServer et détermine l'incrémentation de la position des boules. La fonction "on_timer"
# est une fonction qui est constamment exécutée dans un thread séparé, et qui met à jour
# la position des boules en fonction des incrémentations définies dans la variable globale
# "incs". Ces incrémentations sont modifiées dans OSCMove, selon la position des joysticks
# d'une manette de PlayStation 3.
#*************************************************************************************


class Surface(wx.Panel):
    def __init__(self, parent, pos=(0,0), size=(100,100), numSpeakers=2):
        wx.Panel.__init__(self, parent, pos=pos, size=size)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        self.audio = vars.getVars("Audio")
        self.pos = None
        self.size = size
        self.currentCircle = None
        self.currentSpeaker = None
        self.isAList = False
        self.catch = False
        self.catchSpeaker = False
        self.shift = False
        self.alt = False
        self.s = False
        self.numSpeakers = numSpeakers # FL 29/05/17

        #OSC Variables
        self.incs = [0, 0, 0, 0]
        self.absPos = [0, 0, 0, 0] # FL 04/09/2017
        self.mode2 = False # FL 04/09/2017

        # Creation des cercles/sources
        self.blueCircle = Source(self.size[0]*BLUE_START[0], self.size[1]*BLUE_START[1], CIRCLE_RADIUS) 
        self.redCircle = Source(self.size[0]*RED_START[0], self.size[1]*RED_START[1], CIRCLE_RADIUS)


        speakers = []
        for i in range(self.numSpeakers):
            setup = vars.getVars("Speakers_setup")
            x, y = self.size[0]*setup[i][0], self.size[1]*setup[i][1] #FL 02/09/2017
            speakers.append(Speaker(x, y, SPEAKER_RADIUS))
        vars.setVars("Speakers", speakers)

#        print vars.getVars("Speakers")[0].c
        self.speakerAdjusted() # FL 29/05/17
      
        # méthode pour les controles
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)
        self.Bind(wx.EVT_MOTION, self.onMotion)
        
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        
        self.on_timer()

    def onKeyDown(self,e):
        key = e.GetKeyCode()

        if key == 306:
            self.shift = True
        if key == 307:
            self.alt = True
        if key == 83:
            self.s = True
        
    def onKeyUp(self,e):
        key = e.GetKeyCode()
        
        if key == 306 and self.shift:
            self.shift = False
        elif key == 307 and self.alt:
            self.alt = False
        elif key == 83 and self.s:
            self.s = False
        
    def onLeftDown(self, e):
        self.CaptureMouse()
        self.pos = self.clip(e.GetPosition())
        
        self.onCircle(self.pos[0],self.pos[1])
        
        if self.alt and self.shift:
            self.catch = True
            self.isAList = True
            self.currentCircle = [self.blueCircle, self.redCircle]
            self.currentCircle[0].x = self.pos[0]
            self.currentCircle[0].y = self.pos[1]
            self.currentCircle[1].x = self.pos[0]
            self.currentCircle[1].y = self.pos[1]
            self.distance(self.pos)

        elif self.shift:
            self.catch = True
            self.currentCircle = self.blueCircle 
            self.currentCircle.x = self.pos[0]
            self.currentCircle.y = self.pos[1]
            self.distance(self.pos)

        elif self.alt:
            self.catch = True
            self.currentCircle = self.redCircle 
            self.currentCircle.x = self.pos[0]
            self.currentCircle.y = self.pos[1]
            self.distance(self.pos)
            
        elif self.s:
            self.onSpeaker(self.pos)
            
        elif self.catch:
            pass

        self.Refresh()

    def onRightDown(self,e):
        self.pos = self.clip(e.GetPosition())
        self.initSpkPos(self.pos)
        self.Refresh()
        
    def onMotion(self, e):
        if self.HasCapture():

            self.pos = self.clip(e.GetPosition())

            # si le cercle est attrapé, ajustement des positions (x,y)
            if self.isAList and self.catch:
                self.currentCircle[0].x = self.pos[0]
                self.currentCircle[0].y = self.pos[1]
                self.currentCircle[1].x = self.pos[0]
                self.currentCircle[1].y = self.pos[1]
                self.distance(self.pos)

            elif self.catch:
                self.currentCircle.x = self.pos[0]
                self.currentCircle.y = self.pos[1]
                self.distance(self.pos)
                
            elif self.catchSpeaker:
                self.currentSpeaker.x = self.pos[0]
                self.currentSpeaker.y = self.pos[1]
#                self.distance(self.pos)
                self.speakerAdjusted() # FL 29/05/17

            self.Refresh()

    def onLeftUp(self, e):

        if self.HasCapture():

            self.ReleaseMouse()

            if self.catch or self.catchSpeaker:
                self.isAList = False
                self.catch = False
                self.catchSpeaker = False
                self.currentCircle = None
                self.currentSpeaker = None

            # reinitialise la position
            self.pos = None
            
            self.Refresh()

    def onPaint(self, e):
        w,h = self.GetSize()

        dc = wx.AutoBufferedPaintDC(self)
        
        # Surface
        dc.SetBrush(wx.Brush(COLOR_BACK))
        dc.DrawRectangle(0, 0, w+1, h+1)
        
        # Le quadrillage
        dc.SetPen(wx.Pen(COLOR_GRID, 2))
#        for i in range(0, 600, 25):
#            dc.DrawLine(0, i, w, i)
#            dc.DrawLine(i, 0, i, h)

        dc.SetBrush(wx.Brush(COLOR_GRID,style=wx.TRANSPARENT))
        for i in range(8):
            dc.DrawCircle(w/2,h/2,GRID_CIRCLE_RADIUS*(7*i))
#            dc.DrawCircle(300,300,CIRCLE_RADIUS*(7*i))

        for i in range(self.numSpeakers):
            vars.getVars("Speakers")[i].draw(dc, COLOR_AV)
            vars.getVars("Speakers")[i].drawZone(dc, COLOR_AV)

        
        # ecriture de valeurs
        if self.catch:            
            # conversion des positions X et Y entre 0 et 1
            x = self.pos[0] / float(w)
            y = 1.- self.pos[1] / float(h)
            
            # affiche la position normalisee du pointeur
            dc.DrawText("%.3f, %.3f" % (x,y), 10, 10)
            
        # Les cercles
        self.blueCircle.draw(dc,COLOR_BLUE)
        self.redCircle.draw(dc,COLOR_RED)
        

    def onCircle(self,x,y):
        if self.redCircle.isInside(x,y):
            self.currentCircle = self.redCircle
            self.catch = True
#            print "In red"
            return True

        elif self.blueCircle.isInside(x,y):
            self.currentCircle = self.blueCircle
            self.catch = True
#            print "In blue"
            return True

        else: 
            self.catch = False
            #print "Nanh han!"
            return False
            
    def onSpeaker(self,pos):
        spk = vars.getVars("Speakers")
        for i in spk:
            if i.isInside(pos):
                self.currentSpeaker = i
                self.catchSpeaker = True
                break

            else:
                self.currentSpeaker = None
                self.catchSpeaker = False
                
    def spkInMotion(self,pos):
        pass
        
    def initSpkPos(self,pos):
        initPos = vars.getVars("Speakers_setup")
        spk = vars.getVars("Speakers")
        for i in spk:
            if i.isInside(pos):
                self.currentSpeaker = i
                spkIndex = spk.index(i)
                self.currentSpeaker.x = initPos[spkIndex][0] * self.size[0] # FL 02/09/2017
                self.currentSpeaker.y = initPos[spkIndex][1] * self.size[1] # FL 02/09/2017
                break
        self.speakerAdjusted() # FL 29/05/17

    def clip(self,pos):
        w,h = self.GetSize()
        if pos[0] < 0:
            pos[0] = 0
        elif pos[0] > w:
            pos[0] = w
        if pos[1] < 0:
            pos[1] = 0
        elif pos[1] > h:
            pos[1] = h
        return pos


##### for each spk, getZone() calculer la distance de ce radius:

    def distance(self,pos):    
        for i in range(self.numSpeakers):
            SpkPos = vars.getVars("Speakers")[i].getCenter()
            SpkRad = vars.getVars("Speakers")[i].getZoneRad()
            dist = math.sqrt(math.pow((pos[0]-SpkPos[0]),2) + math.pow((pos[1]-SpkPos[1]),2))
            amp = max(0, 1. - dist / float(SpkRad))
                

            if self.isAList:
                self.audio.setBlueAmp(i,amp)
                self.audio.setRedAmp(i,amp)

            elif self.currentCircle == self.blueCircle:
                self.audio.setBlueAmp(i,amp)

            elif self.currentCircle == self.redCircle:
                self.audio.setRedAmp(i,amp)
         
    # FL START 23/05/2017
    # Cette fonction est adaptée pour fonctionner avec une manette de PlayStation 3.
    # Le code devra probablement être ajusté si un autre type de controleur OSC est utilisé.
    def OSCMove(self, chnl, x=None, y=None):
        global incs, absPos
        inc = 0
        BIG_INC = 40
        SMALL_INC = 10
        
        if self.mode2:
            if chnl == 0:
                if x != None:
                    self.absPos[0] = x
                if y != None:
                    self.absPos[1] = y
            if chnl == 1:
                if x != None:
                    self.absPos[2] = x
                if y != None:
                    self.absPos[3] = y
        else:
            # Boule bleue (canal de gauche)
            if chnl == 0:
                if x != None:
                    if x < 0.45:
                        if x < 0.001:
                            inc = -BIG_INC
                        else:
                            inc = -SMALL_INC
                    elif x > 0.55:
                        if x > 0.999:
                            inc = BIG_INC
                        else:
                            inc = SMALL_INC
                    else: 
                        inc = 0
                    self.incs[0] = inc
                if y != None:
                    if y < 0.45:
                        if y < 0.001:
                            inc = -BIG_INC
                        else:
                            inc = -SMALL_INC
                    elif y > 0.55:
                        if y > 0.999:
                            inc = BIG_INC
                        else:
                            inc = SMALL_INC
                    else:
                        inc = 0
                    self.incs[1] = inc
                    
            # Boule rouge (canal de droite)
            elif chnl == 1:
                if x != None:
                    if x < 0.45:
                        if x < 0.001:
                            inc = -BIG_INC
                        else:
                            inc = -SMALL_INC
                    elif x > 0.55:
                        if x > 0.999:
                            inc = BIG_INC
                        else:
                            inc = SMALL_INC
                    else:
                        inc = 0
                    self.incs[2] = inc
                if y != None:
                    if y < 0.45:
                        if y < 0.001:
                            inc = -BIG_INC
                        else:
                            inc = -SMALL_INC
                    elif y > 0.55:
                        if y > 0.999:
                            inc = BIG_INC
                        else:
                            inc = SMALL_INC
                    else:
                        inc = 0
                    self.incs[3] = inc
        
    def on_timer(self):
        w,h = self.size[0], self.size[1]
        oldPosBlue = [self.blueCircle.x, self.blueCircle.y]
        oldPosRed = [self.redCircle.x, self.redCircle.y]
        changed = False
        
        if self.mode2:
            rate = 30
            self.blueCircle.x = floatmap(self.absPos[0], 0, w)
            self.blueCircle.y = floatmap(self.absPos[1], 0, h)
            self.redCircle.x = floatmap(self.absPos[2], 0, w)
            self.redCircle.y = floatmap(self.absPos[3], 0, h)
        else:
            rate = 40
            self.blueCircle.x += self.incs[0]
            self.blueCircle.y += self.incs[1]
            self.redCircle.x += self.incs[2]
            self.redCircle.y += self.incs[3]
            
            if self.blueCircle.x < 0:
                self.blueCircle.x = 0
            elif self.blueCircle.x > w:
                self.blueCircle.x = w
               
            if self.blueCircle.y < 0:
                self.blueCircle.y = 0
            elif self.blueCircle.y > h:
                self.blueCircle.y = h
                
            if self.redCircle.x < 0:
                self.redCircle.x = 0
            elif self.redCircle.x > w:
                self.redCircle.x = w
               
            if self.redCircle.y < 0:
                self.redCircle.y = 0
            elif self.redCircle.y > h:
                self.redCircle.y = h

        if oldPosBlue[0] != self.blueCircle.x or oldPosBlue[1] != self.blueCircle.y:
            self.currentCircle = self.blueCircle
            newPos = [self.blueCircle.x, self.blueCircle.y]
            self.distance(newPos)
            changed = True
        
        if oldPosRed[0] != self.redCircle.x or oldPosRed[1] != self.redCircle.y:        
            self.currentCircle = self.redCircle
            newPos = [self.redCircle.x, self.redCircle.y]
            self.distance(newPos)
            changed = True
                
        if changed:
            self.Refresh()
        wx.CallLater(rate, self.on_timer)
        # FL END 23/05/2017
    
    # FL START 29/05/17
    # Fonction qui ajuste les volumes quand on change les radius des speakers
    def speakerAdjusted(self):
        self.currentCircle = self.blueCircle
        pos = [self.blueCircle.x, self.blueCircle.y]
        self.distance(pos)
        
        self.currentCircle = self.redCircle
        pos = [self.redCircle.x, self.redCircle.y]
        self.distance(pos)
    # FL START 29/05/17
        
    # FL START 04/09/2017
    def modeChange(self):
        if self.mode2:
            self.mode2 = False
        else:
            self.mode2 = True
    # FL END
    
# formule pour la distance entre 2 points. 
# pour A(x1,y1) et B(x2,y2)
# d(A,B) = math.sqrt(math.pow((x2-x1),2) + math.pow((y2-y1),2))