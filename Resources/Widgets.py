# encoding: utf-8

import wx
import math
from pyo import *
import Variables as vars
from Constants import *




class Source:
    def __init__(self, x, y, c): 
        self.x = x
        self.y = y
        self.c = c
        self.rect = wx.Rect(self.x-self.c,self.y-self.c,self.c*2,self.c*2)

    def draw(self,dc,color):
        dc.SetPen(wx.Pen(color, 1))
        dc.SetBrush(wx.Brush(color))
        dc.DrawCircle(self.x, self.y, self.c)

        # à l'appel, cette fonction ajuste la position du rectangle 
        # pour l'utilisation de la fonction ContainsXY
        self.rect.x = self.x - self.c
        self.rect.y = self.y - self.c

    def isInside(self,x,y):
        if self.rect.ContainsXY(x,y):
            return True
        else:
            return False

    def getPos(self):
        return tuple([self.x, self.y])


class Speaker:
    def __init__(self, x, y, c): 
        self.x = x
        self.y = y
        self.c = c
        self.radius = 25
        self.rect = wx.Rect(self.x-self.c,self.y-self.c,self.c*2,self.c*2)

    def draw(self,dc,color):
        numero = self.getNumOut()
        dc.SetPen(wx.Pen(COLOR_BACK, 1))
        dc.SetBrush(wx.Brush(color))
        dc.DrawCircle(self.x, self.y, self.c)
        dc.DrawText("%d" % numero, self.x-5,self.y-6)
        
        self.rect.x = self.x - self.c
        self.rect.y = self.y - self.c
        

    def getCenter(self):
        return tuple([self.x,self.y])
        
    def getZoneRad(self):
        return self.c * self.radius

    def setZoneRad(self,x):
        self.radius = x
        
    def drawZone(self,dc,color):
        radius = self.getZoneRad()
        dc.SetPen(wx.Pen(color,1))
        dc.SetBrush(wx.Brush(wx.Colour(100,100,100,75)))
        dc.DrawCircle(self.x,self.y,radius)
        
    def getNumOut(self):
        No = vars.getVars("Speakers")
        return No.index(self)+1
        
    def isInside(self,pos):
        x,y = pos[0], pos[1]
        if self.rect.ContainsXY(x,y):
            return True
        else:
            return False

    def getPos(self):
        return tuple([self.x, self.y])