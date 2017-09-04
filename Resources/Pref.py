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
        
        # Liste pour nombre de speakers (en fonction du max. de channels en output du premier driver audio)
        self.chnlList = ["2"]
        self.currentDriverMaxChannels = self.getMaxChnlsFromIndex(self.getOutputDriverIndexFromString(self.outputs[0]))
        for i in range(self.currentDriverMaxChannels):
            if i > 2:
                self.chnlList.append(str(i))

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
        
        # Radio button de la section "Load". Il est créé ici afin de ne pas faire entrer les deux groupe de radio buttons en conflit.
        self.radioOpen = wx.RadioButton(self, -1, "Open existing config.")
        
        boxSP = wx.BoxSizer(wx.HORIZONTAL)
        boxCH = wx.BoxSizer(wx.HORIZONTAL)
        boxOSC = wx.BoxSizer(wx.HORIZONTAL)
        
        self.numSpkLabel = wx.StaticText(self, -1, "Speakers Setup: ")
        self.numSpkChoices = wx.Choice(self, choices = SPEAKERS_SETUP_LIST)
        self.numChnlsLabel = wx.StaticText(self, -1, "Number of speakers (Real): ")
        self.radioSame = wx.RadioButton(self, -1, "Same as speaker setup", style=wx.RB_GROUP)
        self.radioDiff = wx.RadioButton(self, -1, "Other: ")
        self.chnls = wx.ComboBox(self, -1, self.chnlList[0], choices=self.chnlList, style=wx.CB_DROPDOWN)
        self.OSCPortLabel = wx.StaticText(self, -1, "OSC Input Port: ") 
        self.OSCPortText = wx.TextCtrl(self, -1, "5555", size=(80,20))
        
        boxSP.Add(self.numSpkLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        boxSP.Add(self.numSpkChoices, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        boxCH.Add(self.numChnlsLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        boxCH.Add(self.radioSame, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        boxCH.Add(self.radioDiff, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        boxCH.Add(self.chnls, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        boxOSC.Add(self.OSCPortLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        boxOSC.Add(self.OSCPortText, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(boxSP, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        sizer.Add(boxCH, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        sizer.Add(boxOSC, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        self.radioSame.SetValue(1)
        self.chnls.Enable(False)
        
        # Separator line
        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)
          
        # Load Section
        # Le bouton radio self.radioOpen est créé dans la section "New config."
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
        btnsizer.AddButton(okBtn)
        btnsizer.Realize()
        sizer.Add(okBtn, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        
        self.radioNew.SetValue(1)
        self.SetSizer(sizer)
        sizer.Fit(self)
        
        # Binds
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.chooseBtn.Bind(wx.EVT_BUTTON, self.chooseSessionFile)
        self.radioSame.Bind(wx.EVT_RADIOBUTTON, self.onSameRadio)
        self.radioDiff.Bind(wx.EVT_RADIOBUTTON, self.onDiffRadio)
        self.au.Bind(wx.EVT_COMBOBOX, self.updateChnlsList)
        self.numSpkChoices.Bind(wx.EVT_CHOICE, self.updateChnlsList)

        okBtn.SetDefault()

    def OnClose(self, e):
        try:
            self.Destroy()
        except:
            pass
        raise SystemExit
        
    def onSameRadio(self, e):
        self.chnls.Enable(False)
            
    def onDiffRadio(self, e):
        self.updateChnlsList(None)
        self.chnls.Enable(True)
        
    def updateChnlsList(self, e):
        self.chnls.Clear()
        sel = self.numSpkChoices.GetSelection()
        if sel == 0:
            maxSpks = 2
        elif sel == 1:
            maxSpks = 4
        else:
            maxSpks = 8
        self.currentDriverMaxChannels = self.getMaxChnlsFromIndex(self.getOutputDriverIndexFromString(self.au.GetValue()))
        for i in range(self.currentDriverMaxChannels):
            if i >= 1 and i < maxSpks:
                self.chnlList.append(str(i+1))
                self.chnls.Append(str(i+1))
        self.chnls.SetSelection(0)

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
        if self.radioSame.GetValue() == 1:
            pref["NCHNLS"] = self.currentDriverMaxChannels
        elif self.radioDiff.GetValue() == 1:
            pref["NCHNLS"] = int(self.chnls.GetValue())
        
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
#        print pref 
        
# ***********************************
# JR 27 mai 2017

    def onOpen(self):
            f = open(PREFERENCES, "r")
            pref = f.read()
            print pref
            f.close()  

            
