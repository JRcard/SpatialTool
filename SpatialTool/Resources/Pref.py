#!/usr/bin/env python
# encoding: utf-8

import wx, os
from Constants import *
import Variables as vars

pref = vars.getVars("Pref")
print pref

class PrefDlg(wx.Dialog):
    def __init__(self, parent=None, title="Login Prefs"):                  
        wx.Dialog.__init__(self, parent=parent, title=title)
#        self.panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.nchnlsLabel = wx.StaticText(self, -1, "Nchnls")
        self.nchnlsChoices = wx.Choice(self, choices = NCHNLS_LIST)
        self.numSpkLabel = wx.StaticText(self, -1, "Speakers Setup")
        self.numSpkChoices = wx.Choice(self, choices = SPEAKERS_SETUP_LIST)
        self.OSCPortLabel = wx.StaticText(self, -1, "OSC Port")
        self.OSCPortText = wx.TextCtrl(self, -1, "%s" % pref["OSCPORT"], size=(80,20))
        sizer.Add(self.nchnlsLabel, 0, wx.TOP|wx.LEFT, 5)
        sizer.Add(self.nchnlsChoices, 1, wx.BOTTOM|wx.LEFT, 5)
        sizer.Add(self.numSpkLabel, 0, wx.TOP|wx.LEFT, 5)
        sizer.Add(self.numSpkChoices, 1, wx.BOTTOM|wx.LEFT, 5)
        sizer.Add(self.OSCPortLabel, 0, wx.TOP|wx.LEFT, 5)
        sizer.Add(self.OSCPortText, 1, wx.BOTTOM|wx.LEFT, 5)
        
        # binding
        self.Bind(wx.EVT_CHOICE, self.onNchnls, self.nchnlsChoices)
        self.Bind(wx.EVT_CHOICE, self.onNumSpk, self.numSpkChoices)

        btnsizer = wx.StdDialogButtonSizer()
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.Add(btn)
        
        btn2 = wx.Button(self, wx.ID_CANCEL)
        btnsizer.Add(btn2,0,wx.LEFT,15)
        btnsizer.Realize()
        
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL| wx.TOP|wx.LEFT, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

#    def setPref(self):
#        global pref
#        pref["NCHNLS"] = self.nchnlsText.GetValue()

    def onNchnls(self,e):
        pref["NCHNLS"] = int(self.nchnlsChoices.GetStringSelection())
        print pref
        
        
    def onNumSpk(self,e):
        pref["SPEAKERS_SETUP"] = self.numSpkChoices.GetSelection()
        if pref["SPEAKERS_SETUP"] == 1:
            vars.setVars("Speakers_setup", SETUP_STEREO)
            pref["NUM_SPEAKERS"] = len(SETUP_STEREO)
        elif pref["SPEAKERS_SETUP"] == 2:
            vars.setVars("Speakers_setup", SETUP_QUAD)
            pref["NUM_SPEAKERS"] = len(SETUP_QUAD)
        elif pref["SPEAKERS_SETUP"] == 3:
            vars.setVars("Speakers_setup", SETUP_OCTO_STEREO)
            pref["NUM_SPEAKERS"] = len(SETUP_OCTO_STEREO)
        elif pref["SPEAKERS_SETUP"] == 4:
            vars.setVars("Speakers_setup", SETUP_OCTO_DIAMAND)
            pref["NUM_SPEAKERS"] = len(SETUP_OCTO_DIAMAND)
        else:
            pass
        print pref
        
    def setOSC(self):
        pref["OSCPORT"] = self.OSCPortText.GetValue()
            