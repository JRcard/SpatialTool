#!/usr/bin/env python
# encoding: utf-8

import wx, os
from Constants import *
import Variables as vars

pref = vars.getVars("Pref")

class PrefDlg(wx.Frame):
    def __init__(self, parent=None, title="Login Prefs"):                  
        wx.Frame.__init__(self, parent=parent, title=title)
        self.panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.nchnlsLabel = wx.StaticText(self.panel, -1, "Nchnls")
        self.nchnlsText = wx.TextCtrl(self.panel, -1, "%s" % pref["NCHNLS"], size=(80,20))       
        sizer.Add(self.nchnlsLabel, 0, wx.TOP|wx.LEFT, 5)
        sizer.Add(self.nchnlsText, 1, wx.BOTTOM|wx.LEFT, 5)

        btnsizer = wx.StdDialogButtonSizer()
        
        btn = wx.Button(self.panel, wx.ID_OK)
        btn.SetDefault()
        btnsizer.Add(btn)
        
        btn2 = wx.Button(self.panel, wx.ID_CANCEL)
        btnsizer.Add(btn2,0,wx.LEFT,15)
        btnsizer.Realize()
        
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL| wx.TOP|wx.LEFT, 10)

        self.SetSizer(sizer)
        sizer.Fit(self.panel)

        btn.Bind(wx.EVT_TOGGLEBUTTON, self.testOk)
        
    def setPref(self):
        global pref
        pref["NCHNLS"] = self.nchnlsText.GetValue()
        
    def isOk(self,e):
        if e.GetInt == 1:
            return True
            
            