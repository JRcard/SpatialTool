#!/usr/bin/env python
# encoding: utf-8

import wx 
from pyo import *

class Waveform(wx.Panel):
    def __init__(self, parent, table, pos=(150, 680), size=(1200, 200)):
        wx.Panel.__init__(self, parent, pos=pos, size=size)
        
        self.parent = parent
        self.table = table
        
    def createSndTable(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sndview = PyoGuiSndView(self.parent, pos=(150, 680), size=(1200, 200))
        self.sndview.setTable(self.table)
        sizer.Add(self.sndview, 0, wx.ALL | wx.EXPAND, 5)
        return sizer

