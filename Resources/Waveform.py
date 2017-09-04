#!/usr/bin/env python
# encoding: utf-8

import wx 
from pyo import *
from SndView import GuiSndViewPlayHead

class Waveform(wx.Panel):
    def __init__(self, parent, table, pos=(150, 680), size=(1000, 200)):
        wx.Panel.__init__(self, parent, pos=pos, size=size)
        
        self.parent = parent
        self.table = table
        self.size = size
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sndView = GuiSndViewPlayHead(self.parent, size=self.size)
        self.sndView.setTable(self.table)
        sizer.Add(self.sndView, 0, wx.EXPAND)
        
                
#    def createSndTable(self):
#        print self.parent.GetSize()
#        sizer = wx.BoxSizer(wx.HORIZONTAL) # jr 1 juin 2017
#        self.sndview = GuiSndViewPlayHead(self.parent, size=(1000, 400))
#        self.sndview.setTable(self.table)
#        sizer.Add(self.sndview, 0, wx.LEFT | wx.EXPAND, 155) # JR 1 juin 2017
#        return sizer

#    def createTimeSlider(self):
#        sizer = wx.BoxSizer(wx.VERTICAL)
#        self.timeSlider = PyoGuiControlSlider(self.parent, 0, self.table.getDur(False), 0, orient=wx.HORIZONTAL)
#        self.timeSlider.Bind(EVT_PYO_GUI_CONTROL_SLIDER, self.moveTimeSlider)
#  #      self.timeSlider = wx.Slider(self.parent, -1, value=0, minValue=0, maxValue=self.table.getDur(False),
# #                                   style=wx.SL_HORIZONTAL|wx.SL_LABELS)
##        self.timeSlider.Bind(wx.EVT_SLIDER, self.moveTimeSlider)
#        sizer.Add(self.timeSlider, 0, wx.LEFT | wx.EXPAND, 155)
#        return sizer
        
#    def moveTimeSlider(self,e):
#        print self.timeSlider.value
#        
#    def setRange(self,min,max):
#        self.timeSlider.setRange(min,max)