#!/usr/bin/env python
# encoding: utf-8
import os
import wx
from pyo import *
from Surface import Surface
from Constants import *
import Variables as vars
from Waveform import *


#*************************************************************************************
#  22/05/2017 - Francis Lecavalier
#  Conversion des valeurs du AmpSlider en dB et ajout de fonctions à cet effet.
#
#  23/05/2017 - Francis Lecavalier
#  Ajout d'un try/catch et d'un raise pour éviter les segs faults qui surviennet 
#  parfois lorsque l'on quitte l'application. Ne semble pas toujours fonctionner...
#*************************************************************************************

class MyFrame(wx.Frame):
    def __init__(self, parent=None, title="SpatialTool", pos=(100,100),
                 size=(800,700), numSpeakers=2):
        wx.Frame.__init__(self, parent, id=-1, title=title, pos=pos, size=size)

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(COLOR_MAIN)
        
        self.audio = vars.getVars("Audio")
        self.numSpeakers = numSpeakers
        
        # Start JR 31 mai 2017
        frameSizer = wx.BoxSizer(wx.VERTICAL)
        surfaceSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        radiusSizer = wx.BoxSizer(wx.VERTICAL)
        volumeSizer = wx.BoxSizer(wx.VERTICAL)
        controlSizer = wx.BoxSizer(wx.VERTICAL)
        waveform = wx.BoxSizer(wx.VERTICAL)
        upSizer = wx.BoxSizer(wx.HORIZONTAL)
        downSizer = wx.BoxSizer(wx.HORIZONTAL)
        # END JR 31 mai 2017
        
##### MENU #####
        self.menu = wx.MenuBar()
        self.SetMenuBar(self.menu)
        self.file = wx.Menu()
        
        # Put the "File" menu on the menu bar and put action in this menu           
        self.menu.Append(self.file, "&File")
        self.menuSave = self.file.Append(wx.ID_SAVE, "&Save\tCtrl+S", "Save preferences")
        self.file.AppendSeparator()
        self.menuExit = self.file.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
        

        self.Bind(wx.EVT_MENU, self.quit, self.menuExit)    
        self.Bind(wx.EVT_MENU, self.onSave, self.menuSave)
       
##### BOUTONS et GRAPHIQUES ##### 

        self.chooseSndText = wx.StaticText(self.panel, id=-1, label="Choose file",
                                       pos=(20,80))
        self.chooseSnd = wx.Button(self.panel, id=-1, label="Load Snd", 
                                      pos=(10,100))

        self.playStop = wx.ToggleButton(self.panel, id=-1, label="Play", 
                                     pos=(10,130))

        self.radiusSliderText = wx.StaticText(self.panel, id=-1, label="Speakers Zones",
                                       pos=(10,175))
        self.radiusSlider = PyoGuiControlSlider(self.panel, 2, 25, 25, pos=(35,200), size=(35,225), orient=wx.VERTICAL)
        
        # FL -START 22/05/17
        self.ampSliderText = wx.StaticText(self.panel, id=-1, label="Master Volume (dB)",
                                       pos=(13,435))

        self.ampSlider = PyoGuiControlSlider(self.panel, -18, 9, self.convertTodB(1), pos=(35,460), size=(35,225), orient=wx.VERTICAL)
        # FL - END 22/05/17
        
#        self.onOffText.SetForegroundColour(COLOR_AR) # JR 20 mai
        self.radiusSliderText.SetForegroundColour(COLOR_AR)
        self.chooseSndText.SetForegroundColour(COLOR_AR)
        self.ampSliderText.SetForegroundColour(COLOR_AR)

        # BINDS
#        self.onOff.Bind(wx.EVT_TOGGLEBUTTON, self.startServ) # JR 20 mai
        self.radiusSlider.Bind(EVT_PYO_GUI_CONTROL_SLIDER, self.radiusZone)
        self.ampSlider.Bind(EVT_PYO_GUI_CONTROL_SLIDER, self.masterAmp)
        self.Bind(wx.EVT_CLOSE, self.quit)
        self.chooseSnd.Bind(wx.EVT_BUTTON, self.loadSnd)
        self.playStop.Bind(wx.EVT_TOGGLEBUTTON, self.playSnd)
        self.ampSlider.Bind(wx.EVT_LEFT_DCLICK, self.ampSliderReset) #FL 22/05/2017
        
        # VuMeter                       
        self.meter = PyoGuiVuMeter(parent=self.panel,
                                   nchnls=self.numSpeakers, 
                                   pos=(150, 10),
                                   size=(600, 30),
                                   orient=wx.VERTICAL,
                                   style=0)

        self.audio.registerMeter(self.meter)
        
        # START JR 1 juin 2017
        self.waveform = Waveform(self.panel, self.audio.table)
        vars.setVars("Waveform", self.waveform)
        self.sndView = self.waveform.createSndTable()
        self.timeSlider = self.waveform.createTimeSlider()
        
#        self.sndView = PyoGuiSndView(parent=self.panel,
#                                    pos=(150, 680),
#                                    size=(1200, 200),
#                                    style=0)
#                                    
#        self.sndView.setTable(self.audio.table)
        # END JR 1 juin 2017
        
        # cree un objet Surface pour le controle des parametres
        self.surface = Surface(self.panel, pos=(150,60), size=(GRID_WIDTH,GRID_HEIGHT), numSpeakers=self.numSpeakers)
        vars.setVars("Surface", self.surface) #JR 20 mai

##### SIZERS ######
        # START JR 31 mai 2017
        surfaceSizer.Add(self.surface, 0, wx.ALL | wx.EXPAND, 5)
        
        radiusSizer.Add(self.radiusSliderText, 0, wx.ALL | wx.CENTER, 5)
        radiusSizer.Add(self.radiusSlider, 0, wx.ALL | wx.wx.CENTER, 5)
        volumeSizer.Add(self.ampSliderText, 0, wx.ALL | wx.CENTER, 5)
        volumeSizer.Add(self.ampSlider, 0, wx.ALL | wx.CENTER, 5)
        
        buttonSizer.Add(self.chooseSndText, 0, wx.ALL | wx.CENTER, 5)
        buttonSizer.Add(self.chooseSnd, 0, wx.ALL | wx.CENTER, 5)
        buttonSizer.Add(self.playStop, 0, wx.ALL | wx.CENTER, 5)
        
        controlSizer.Add(buttonSizer, 0, wx.ALL | wx.CENTER, 5)
        controlSizer.Add(radiusSizer, 0, wx.ALL | wx.CENTER, 5)
        controlSizer.Add(volumeSizer, 0, wx.ALL | wx.CENTER, 5)

        waveform.Add(self.timeSlider, 0, wx.ALL | wx.EXPAND, 5)        
        waveform.Add(self.sndView, 0, wx.ALL | wx.EXPAND, 5)
#                
        upSizer.Add(controlSizer,0, wx.ALL | wx.EXPAND, 5)        
        upSizer.Add(surfaceSizer, 0, wx.ALL | wx.EXPAND, 5)
        upSizer.Add(self.meter, 0, wx.ALL | wx.EXPAND, 5)
        
        downSizer.Add(waveform, 0, wx.ALL | wx.EXPAND, 5)        
        
        frameSizer.Add(upSizer, 0, wx.ALL | wx.EXPAND, 5)
        frameSizer.Add(downSizer, 0, wx.ALL | wx.EXPAND, 5)
        
        self.panel.SetSizerAndFit(frameSizer)
        # END JR 31 mai 2017
        
##### METHODES #####

    def playSnd(self,e):
        if e.GetInt() == 1:
            if self.playStop.GetLabel() == "Play":
                self.playStop.SetLabel("Stop")
                self.audio.player.play()
        else:
            self.playStop.SetLabel("Play")
            self.audio.player.stop()
            
    def loadSnd(self,e):
        wildcard = "All files|*.*|" \
               "AIFF file|*.aif;*.aiff;*.aifc;*.AIF;*.AIFF;*.Aif;*.Aiff|" \
               "Wave file|*.wav;*.wave;*.WAV;*.WAVE;*.Wav;*.Wave"
        dlg = wx.FileDialog(self, message="Choose a new soundfile...", 
                            wildcard=wildcard, style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if path != "":
                self.chooseSnd.SetLabel("Ready")
                self.audio.changeSnd(path)
        dlg.Destroy()        
        
    def quit(self,e):
        if os.path.isfile(EMPTY_AUDIO_FILE):
            os.remove(EMPTY_AUDIO_FILE)
        audio = vars.getVars("Audio")
        audio.server.stop()
        # FL - START 22/05/17 
        try:
            self.Destroy()
        except:
            pass
        raise SystemExit
        # FL - END 22/05/17
        
    def onSave(self,e):
        pref = vars.getVars("Pref")
        f = open(PREFERENCES, "w")
        print f
        f.write(str(pref))
        f.close()

    def radiusZone(self,e):
        x = e.value
        speakers = vars.getVars("Speakers")
        print str(len(speakers))
        for i in range(len(speakers)):
            speakers[i].setZoneRad(x)
        self.surface.Refresh()
            
    def masterAmp(self,e):
        x = e.value
        audio = vars.getVars("Audio")
        audio.player.mul = self.convertToMul(x) #FL 22/05/17
#        audio.player.mul = x   FL 22/05/17
        
    # FL - START 22/05/17
    def convertTodB(self, floatValue):
        try:
            return math.log10(floatValue) * 10
        except ValueError:
            return -120.0
            
    def convertToMul(self, floatValue):
        return pow(10, (floatValue/10))
        
    def ampSliderReset(self, e):
        e.GetEventObject().SetValue(0.0)
        audio = vars.getVars("Audio")
        audio.player.mul = 1.0
        self.Refresh()
    # FL - END 22/05/17
        