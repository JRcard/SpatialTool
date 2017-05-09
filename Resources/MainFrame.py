#!/usr/bin/env python
# encoding: utf-8
import os
import wx
from pyo import *
from Surface import Surface
from Constants import *
import Variables as vars


class MyFrame(wx.Frame):
    def __init__(self, parent=None, title="SpatialTool", pos=(100,100),
                 size=(800,700)):
        wx.Frame.__init__(self, parent, id=-1, title=title, pos=pos, size=size)

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(COLOR_MAIN)
        
        self.audio = vars.getVars("Audio")

##### MENU #####
        self.menu = wx.MenuBar()
        self.SetMenuBar(self.menu)
        self.file = wx.Menu()
        
        # Put the "File" menu on the menu bar and put action in this menu           
        self.menu.Append(self.file, "&File")
        self.menuExit = self.file.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
        

        self.Bind(wx.EVT_MENU, self.quit, self.menuExit)    
        
       
##### BOUTONS et GRAPHIQUES ##### 


        self.onOffText = wx.StaticText(self.panel, id=-1, label="Audio Server",
                                       pos=(17,10))
        self.onOff = wx.ToggleButton(self.panel, id=-1, label="On", 
                                     pos=(10,30))

        self.chooseSndText = wx.StaticText(self.panel, id=-1, label="Choose file",
                                       pos=(20,80))
        self.chooseSnd = wx.Button(self.panel, id=-1, label="Load Snd", 
                                      pos=(10,100))

        self.playStop = wx.ToggleButton(self.panel, id=-1, label="Play", 
                                     pos=(10,130))

        self.radiusSliderText = wx.StaticText(self.panel, id=-1, label="Speakers Zones",
                                       pos=(10,175))
        self.radiusSlider = PyoGuiControlSlider(self.panel, 2, 25, 25, pos=(35,200), size=(35,225), orient=wx.VERTICAL)
        
        self.ampSliderText = wx.StaticText(self.panel, id=-1, label="Master Volume",
                                       pos=(13,435))
        self.ampSlider = PyoGuiControlSlider(self.panel, 0, 2, 1, pos=(35,460), size=(35,225), orient=wx.VERTICAL)
        
        self.radiusSliderText.SetForegroundColour(COLOR_AR)
        self.onOffText.SetForegroundColour(COLOR_AR)
        self.chooseSndText.SetForegroundColour(COLOR_AR)
        self.ampSliderText.SetForegroundColour(COLOR_AR)

        # BINDS
        self.radiusSlider.Bind(EVT_PYO_GUI_CONTROL_SLIDER, self.radiusZone)
        self.ampSlider.Bind(EVT_PYO_GUI_CONTROL_SLIDER, self.masterAmp)
        self.Bind(wx.EVT_CLOSE, self.quit)
        self.onOff.Bind(wx.EVT_TOGGLEBUTTON, self.startServ)
        self.chooseSnd.Bind(wx.EVT_BUTTON, self.loadSnd)
        self.playStop.Bind(wx.EVT_TOGGLEBUTTON, self.playSnd)
        
        # VuMeter                       
        self.meter = PyoGuiVuMeter(parent=self.panel,
                                   nchnls=NUM_SPEAKERS,
                                   pos=(150, 10),
                                   size=(600, 30),
                                   orient=wx.HORIZONTAL,
                                   style=0)

        self.audio.registerMeter(self.meter)

        # cree un objet Surface pour le controle des parametres
        self.surface = Surface(self.panel, pos=(150,60), size=(GRID_WIDTH,GRID_HEIGHT))


##### METHODES #####        
    def startServ(self,e):
        if e.GetInt() == 1:
            if self.onOff.GetLabel() == "On":
                self.onOff.SetLabel("Off")
            
            self.audio.server.start()
        else:
            self.onOff.SetLabel("On")
            self.audio.server.stop()

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
        print "Cleaning up..."
        self.Destroy()

    def radiusZone(self,e):
        x = e.value
        speakers = vars.getVars("Speakers")
        for i in range(len(speakers)):
            speakers[i].setZoneRad(x)
        self.surface.Refresh()
            
    def masterAmp(self,e):
        x = e.value
        audio = vars.getVars("Audio")
        audio.player.mul = x
        