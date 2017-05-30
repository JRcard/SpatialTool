#!/usr/bin/env python
# encoding: utf-8

import wx, os
from Constants import *
import Variables as vars
from pyo import *

class PrefDlg(wx.Dialog):
    def __init__(self, parent=None, title="Initial Configuration"):                  
        wx.Dialog.__init__(self, parent=parent, title=title)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.outputs, self.outputIndexes, self.defaultOutput = self.getAvailableAudioOutputsDrivers()

        # Audio Driver Section
        boxAU = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Audio Driver:")
        self.au = wx.ComboBox(self, -1, self.outputs[0], choices=self.outputs, style=wx.CB_DROPDOWN)
        
        boxAU.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        boxAU.Add(self.au, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(boxAU, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        # Separator line
        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)
        
        # Create Section
        self.radioNew = wx.RadioButton(self, -1, "Create new configuration", style=wx.RB_GROUP)
        sizer.Add(self.radioNew, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        boxSP = wx.BoxSizer(wx.HORIZONTAL)
        boxOSC = wx.BoxSizer(wx.HORIZONTAL)
        
        self.numSpkLabel = wx.StaticText(self, -1, "Speakers Setup: ")
        self.numSpkChoices = wx.Choice(self, choices = SPEAKERS_SETUP_LIST)
        self.OSCPortLabel = wx.StaticText(self, -1, "OSC Input Port: ") 
        self.OSCPortText = wx.TextCtrl(self, -1, "5555", size=(80,20))
        boxSP.Add(self.numSpkLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        boxSP.Add(self.numSpkChoices, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        boxOSC.Add(self.OSCPortLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        boxOSC.Add(self.OSCPortText, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(boxSP, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        sizer.Add(boxOSC, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        # Separator line
        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)
          
        # Load Section
        self.radioOpen = wx.RadioButton(self, -1, "Open existing config.")
        sizer.Add(self.radioOpen, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        boxOpen = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Path:")
        self.path = wx.TextCtrl(self, -1, value="", style=wx.TE_PROCESS_ENTER)
        self.chooseBtn = wx.Button(self, label="Choose...", style=wx.BU_EXACTFIT)
        boxOpen.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        boxOpen.Add(self.path, 1, wx.ALIGN_CENTRE|wx.ALL, 5) 
        boxOpen.Add(self.chooseBtn, 0, wx.ALIGN_CENTRE|wx.ALL, 5) 
        sizer.Add(boxOpen, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        # Ok Button
        btnsizer = wx.StdDialogButtonSizer()
        okBtn = wx.Button(self, wx.ID_OK)
        okBtn.SetDefault()
        btnsizer.AddButton(okBtn)
        btnsizer.Realize()
        sizer.Add(okBtn, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        
        self.radioNew.SetValue(1)
        self.SetSizer(sizer)
        sizer.Fit(self)
        
        # Binds
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.chooseBtn.Bind(wx.EVT_BUTTON, self.chooseSessionFile)

    def OnClose(self, e):
        try:
            self.Destroy()
        except:
            pass
        raise SystemExit
            
    def getAvailableAudioOutputsDrivers(self):
        outputDriverList, outputDriverIndexes = pa_get_output_devices()
        defaultOutputDriver = outputDriverList[outputDriverIndexes.index(pa_get_default_output())]
        return outputDriverList, outputDriverIndexes, defaultOutputDriver
        
    def getMaxChnlsFromIndex(self, output):
        return pa_get_output_max_channels(output)
        
    def getOutputDriverIndexFromString(self, string):
        try:
            return self.outputIndexes[self.outputs.index(string)]
        except:
            return 0
            
    def chooseSessionFile(self, e):
        wildcard = "Save file (*.txt)|*.txt|"        \
           "All files (*.*)|*.*"
        dlg = wx.FileDialog(self, message="Open configuration ...", defaultDir=os.getcwd(), 
            defaultFile="", wildcard=wildcard, style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.path.SetValue(dlg.GetPath())
        dlg.Destroy()
        self.FitInside()  
        
    # Cette fonction permet aux préférences de se mettre à jour même si on ne les a pas changées dans la fenêtre de configuration initiale.
    def commitPrefs(self):
        pref = vars.getVars("Pref")
        
        # On sauvegarde le nom du driver, car l'index peut changer
        pref["AUDIO_DRIVER"] = self.au.GetValue()

        # Max output channels available on the selected driver
        pref["NCHNLS"] = self.getMaxChnlsFromIndex(self.getOutputDriverIndexFromString(pref["AUDIO_DRIVER"]))
        
        # Speakers setup
        pref["SPEAKERS_SETUP"] = self.numSpkChoices.GetSelection()
        if pref["SPEAKERS_SETUP"] == 0:
            vars.setVars("Speakers_setup", SETUP_STEREO)
            pref["NUM_SPEAKERS"] = len(SETUP_STEREO)
        elif pref["SPEAKERS_SETUP"] == 1:
            vars.setVars("Speakers_setup", SETUP_QUAD)
            pref["NUM_SPEAKERS"] = len(SETUP_QUAD)
        elif pref["SPEAKERS_SETUP"] == 2:
            vars.setVars("Speakers_setup", SETUP_OCTO_STEREO)
            pref["NUM_SPEAKERS"] = len(SETUP_OCTO_STEREO)
        elif pref["SPEAKERS_SETUP"] == 3:
            vars.setVars("Speakers_setup", SETUP_OCTO_DIAMAND)
            pref["NUM_SPEAKERS"] = len(SETUP_OCTO_DIAMAND)
        else:
            pass
            
        # OSC
        pref["OSCPORT"] = int(self.OSCPortText.GetValue())
        print pref
        
# ***********************************
# JR 27 mai 2017
# Je met ces fonctions ici pour le moment, ne sachant pas encore leur place optimum...

    def onSave(self):
            f = open(PREFERENCES, "w")
            print f
            f.write(str(pref))
            f.close()

    def onOpen(self):
            f = open(PREFERENCES, "r")
            pref = f.read()
            print pref
            f.close()  

            
