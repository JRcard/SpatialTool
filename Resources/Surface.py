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
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, pos=pos, size=size)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        self.audio = vars.getVars("Audio")
        self.pos = None
        self.currentCircle = None
        self.currentSpeaker = None
        self.isAList = False
        self.catch = False
        self.catchSpeaker = False
        self.shift = False
        self.alt = False
        self.s = False

        # FL START 23/05/2017
        #OSC Variables
        self.incs = [0, 0, 0, 0]
        # FL END 23/05/2017

        # Creation des cercles/sources
        self.blueCircle = Source(100, 100, CIRCLE_RADIUS) 
        self.redCircle = Source(500, 100, CIRCLE_RADIUS)

# START JR 25 mai2017
        # création des speakers
#        if NUM_SPEAKERS == 2:
#            vars.setVars("Speakers_setup", SETUP_STEREO)
#        elif NUM_SPEAKERS == 4:
#            vars.setVars("Speakers_setup", SETUP_QUAD)
#        elif NUM_SPEAKERS == 8 and TYPE == "A":
#            vars.setVars("Speakers_setup", SETUP_OCTO_DIAMAND)
#        elif NUM_SPEAKERS == 8 and TYPE == "B":
#            vars.setVars("Speakers_setup", SETUP_OCTO_STEREO)
#        else:
#            pass

        speakers = []
        setup = vars.getVars("Speakers_setup")
        pref = vars.getVars("Pref") # JR 25 mai 2017
        numSpk = pref["NUM_SPEAKERS"]
        for i in range(numSpk):
            x, y = setup[i][0], setup[i][1]
            speakers.append(Speaker(x, y, SPEAKER_RADIUS))
        vars.setVars("Speakers", speakers)
# END JR 25 mai 2017
        
        # méthode pour les controles
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)
        self.Bind(wx.EVT_MOTION, self.onMotion)
        
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        
        self.on_timer() #FL 23/05/2017

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
            print "catch!"

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
                self.distance(self.pos)

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
        dc.DrawRectangle(0, 0, w, h)
        
        # Le quadrillage
        dc.SetPen(wx.Pen(COLOR_GRID, 2))
#        for i in range(0, 600, 25):
#            dc.DrawLine(0, i, w, i)
#            dc.DrawLine(i, 0, i, h)

        dc.SetBrush(wx.Brush(COLOR_GRID,style=wx.TRANSPARENT))
        for i in range(8):
            dc.DrawCircle(300,300,CIRCLE_RADIUS*(7*i))

        pref = vars.getVars("Pref") # JR 25 mai 2017
        numSpk = pref["NUM_SPEAKERS"]
        for i in range(numSpk):
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
            print "In red"
            return True

        elif self.blueCircle.isInside(x,y):
            self.currentCircle = self.blueCircle
            self.catch = True
            print "In blue"
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
                self.currentSpeaker.x = initPos[spkIndex][0]
                self.currentSpeaker.y = initPos[spkIndex][1]
                break
        

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
    ##### p-e remplacer la diagonal ds l'équation.... a voir.

    def distance(self,pos):
        pref = vars.getVars("Pref") # JR 25 mai 2017
        numSpk = pref["NUM_SPEAKERS"]        
        for i in range(numSpk):
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
        global incs
        inc = 0
        BIG_INC = 10
        SMALL_INC = 5
        
        # Boule bleue (canal de gauche)
        if chnl == 0:
            if x != None:
                if x < 0.47:
                    if x < 0.25:
                        inc = -BIG_INC
                    else:
                        inc = -SMALL_INC
                elif x > 0.53:
                    if x > 0.75:
                        inc = BIG_INC
                    else:
                        inc = SMALL_INC
                else: 
                    inc = 0
                self.incs[0] = inc
            if y != None:
                if y < 0.47:
                    if y < 0.25:
                        inc = -BIG_INC
                    else:
                        inc = -SMALL_INC
                elif y > 0.53:
                    if y > 0.75:
                        inc = BIG_INC
                    else:
                        inc = SMALL_INC
                else:
                    inc = 0
                self.incs[1] = inc
                
        # Boule rouge (canal de droite)
        elif chnl == 1:
            if x != None:
                if x < 0.47:
                    if x < 0.25:
                        inc = -BIG_INC
                    else:
                        inc = -SMALL_INC
                elif x > 0.53:
                    if x > 0.75:
                        inc = BIG_INC
                    else:
                        inc = SMALL_INC
                else:
                    inc = 0
                self.incs[2] = inc
            if y != None:
                if y < 0.47:
                    if y < 0.25:
                        inc = -BIG_INC
                    else:
                        inc = -SMALL_INC
                elif y > 0.53:
                    if y > 0.75:
                        inc = BIG_INC
                    else:
                        inc = SMALL_INC
                else:
                    inc = 0
                self.incs[3] = inc
        
    def on_timer(self):
        w,h = self.GetSize()
        oldPosBlue = [self.blueCircle.x, self.blueCircle.y]
        oldPosRed = [self.redCircle.x, self.redCircle.y]
        
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
        
        if oldPosRed[0] != self.redCircle.x or oldPosRed[1] != self.redCircle.y:        
            self.currentCircle = self.redCircle
            newPos = [self.redCircle.x, self.redCircle.y]
            self.distance(newPos)
            
        self.Refresh()
        wx.CallLater(50, self.on_timer)
    # FL END 23/05/2017
        
    
### formule pour la distance entre 2 points. pour calculer la distance 
### entre le centre du cercle et le coin sup.Gauche du speaker: 
    ### pour A(x1,y1) et B(x2,y2)
### d(A,B) = math.sqrt(math.pow((x2-x1),2) + math.pow((y2-y1),2))