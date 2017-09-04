#!/usr/bin/env python
# encoding: utf-8
import os
import wx
import time
import threading
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
noResizeStyle = wx.SYSTEM_MENU|wx.wx.CLOSE_BOX|wx.CAPTION|wx.MINIMIZE_BOX

class MyFrame(wx.Frame):
    def __init__(self, parent=None, title="SpatialTool", pos=(100,100),
                 size=(800,700), numSpeakers=2):
        wx.Frame.__init__(self, parent, id=-1, title=title, pos=pos, size=size, style=noResizeStyle)

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(COLOR_MAIN)
        
        self.audio = vars.getVars("Audio")
        self.numSpeakers = numSpeakers
        self.size = size # FL 02/09/2017
        
        # FL 02/09/2017
        self.sndDurSecs = 0.0;
        self.sndOffset = 0.0;
        self.isPlaying = False
        self.elapsedTime = 0.0
        self.initTime = 0.0
        
        # Start JR 31 mai 2017
        frameSizer = wx.GridBagSizer() #FL 02/09/2017
#        frameSizer = wx.BoxSizer(wx.VERTICAL) # FL 02/09/2017
        surfaceSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        radiusSizer = wx.BoxSizer(wx.VERTICAL)
        volumeSizer = wx.BoxSizer(wx.VERTICAL)
        controlSizer = wx.BoxSizer(wx.VERTICAL)
        waveform = wx.BoxSizer(wx.VERTICAL)
        infoSizer = wx.BoxSizer(wx.VERTICAL) # FL 02/09/2017
        vuMeterSizer = wx.BoxSizer(wx.HORIZONTAL) # FL 02/09/2017
        songInfoSizer = wx.BoxSizer(wx.HORIZONTAL) # FL 02/09/2017
        oscSizer = wx.BoxSizer(wx.VERTICAL) # FL 02/09/2017
#        upSizer = wx.BoxSizer(wx.HORIZONTAL) FL 02/09/2017 
#        downSizer = wx.BoxSizer(wx.HORIZONTAL)FL 02/09/2017 
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

        self.chooseSndText = wx.StaticText(self.panel, id=-1, label="Audio Controls",# FL 02/09/2017
                                       pos=(20,80))
        self.chooseSnd = wx.Button(self.panel, id=-1, label="Open File...") # FL 02/09/2017

        self.playPause = wx.ToggleButton(self.panel, id=-1, label="Play")  # FL 02/09/2017 J'ai renommé le bouton pour mieux refléter sa nouvelle fonction
        self.stopBtn = wx.Button(self.panel, id=-1, label="Stop") # FL 02/09/2017
                                      
                                      
        self.radiusSliderText1 = wx.StaticText(self.panel, id=-1, label="Zone", style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.radiusSliderText2 = wx.StaticText(self.panel, id=-1, label="Radius", style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.radiusSlider = PyoGuiControlSlider(self.panel, 2, 25, INIT_SOUND_RADIUS, orient=wx.VERTICAL)
        
        # FL -START 22/05/17
        self.ampSliderText1 = wx.StaticText(self.panel, id=-1, label="Master", style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.ampSliderText2 = wx.StaticText(self.panel, id=-1, label="Vol. (dB)", style=wx.ALIGN_CENTRE_HORIZONTAL)

        self.ampSlider = PyoGuiControlSlider(self.panel, -60, 9, self.convertTodB(1), orient=wx.VERTICAL)
        # FL - END 22/05/17
        
        # FL START 02/09/2017
        self.sndName = wx.StaticText(self.panel, id=-1, label="<WAV or AIFF soundfiles only>", style=wx.ALIGN_CENTRE_HORIZONTAL | wx.ST_NO_AUTORESIZE | wx.ST_ELLIPSIZE_MIDDLE)
        self.chrono = wx.StaticText(self.panel, id=-1, label="--:--:--.--", style=wx.ALIGN_LEFT)
        self.timeLeft = wx.StaticText(self.panel, id=-1, label="- --:--:--.--", style= wx.ALIGN_LEFT)
        self.oscText1 = wx.StaticText(self.panel, id=-1, label="OSC Port:", style=wx.ALIGN_CENTRE)
        self.oscPort = wx.StaticText(self.panel, id=-1, label=str(vars.getVars("Pref")["OSCPORT"]), style= wx.ALIGN_CENTRE)
        
        # FL END
        
#        self.onOffText.SetForegroundColour(COLOR_AR) # JR 20 mai
        self.radiusSliderText1.SetForegroundColour(COLOR_AR)
        self.radiusSliderText2.SetForegroundColour(COLOR_AR)
        self.chooseSndText.SetForegroundColour(COLOR_AR)
        self.ampSliderText1.SetForegroundColour(COLOR_AR)
        self.ampSliderText2.SetForegroundColour(COLOR_AR)
        self.sndName.SetForegroundColour(COLOR_AR) #FL 02/09/2017
        self.chrono.SetForegroundColour(COLOR_AR) #FL 02/09/2017
        self.timeLeft.SetForegroundColour(COLOR_AR) #FL 02/09/2017
        
        # FL 02/09/2017 START
        self.infoText1 = wx.StaticText(self.panel, id=-1, label=u"Developed by Jérémie Ricard && Francis Lecavalier", style=wx.ALIGN_RIGHT)
        self.infoText2 = wx.StaticText(self.panel, id=-1, label=u"Montreal, 2017", style=wx.ALIGN_RIGHT)
        self.infoText1.SetForegroundColour(COLOR_AR)
        self.infoText2.SetForegroundColour(COLOR_AR)
        self.oscText1.SetForegroundColour(COLOR_AR)
        self.oscPort.SetForegroundColour(COLOR_AR)
        # FL 02/09/2017 END

        # BINDS
#        self.onOff.Bind(wx.EVT_TOGGLEBUTTON, self.startServ) # JR 20 mai
        self.radiusSlider.Bind(EVT_PYO_GUI_CONTROL_SLIDER, self.radiusZone)
        self.ampSlider.Bind(EVT_PYO_GUI_CONTROL_SLIDER, self.masterAmp)
        self.Bind(wx.EVT_CLOSE, self.quit)
        self.chooseSnd.Bind(wx.EVT_BUTTON, self.loadSnd)
        self.stopBtn.Bind(wx.EVT_BUTTON, self.stopSnd) # FL 02/09/2017
        self.playPause.Bind(wx.EVT_TOGGLEBUTTON, self.playSnd)
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
        self.waveform = Waveform(self.panel, self.audio.table, size=(size[0]*GRID_WIDTH, 100))
        vars.setVars("Waveform", self.waveform)
        self.sndView = self.waveform.sndView
#        self.sndView = self.waveform.createSndTable()
#        self.timeSlider = self.waveform.createTimeSlider()
        
#        self.sndView = PyoGuiSndView(parent=self.panel,
#                                    pos=(150, 680),
#                                    size=(1200, 200),
#                                    style=0)
#                                    
#        self.sndView.setTable(self.audio.table)
        # END JR 1 juin 2017
        
        # cree un objet Surface pour le controle des parametres
        self.surface = Surface(self.panel, size=(size[0]*GRID_WIDTH,size[1]*GRID_HEIGHT), numSpeakers=self.numSpeakers)
#        self.surface = Surface(self.panel, pos=(150,60), size=(GRID_WIDTH,GRID_HEIGHT), numSpeakers=self.numSpeakers)
        vars.setVars("Surface", self.surface) #JR 20 mai
        
        if self.audio.noSound:
            self.playPause.Disable()
            self.stopBtn.Disable()

##### SIZERS ######
        # START JR 31 mai 2017
        surfaceSizer.Add(self.surface, 0, wx.ALL | wx.EXPAND)
        
        radiusSizer.Add(self.radiusSliderText1, 0, wx.LEFT | wx.wx.CENTER | wx.EXPAND, 5)
        radiusSizer.Add(self.radiusSliderText2, 0,  wx.BOTTOM | wx.LEFT | wx.wx.CENTER | wx.EXPAND, 5)
        radiusSizer.Add(self.radiusSlider, 1, wx.TOP | wx.BOTTOM | wx.LEFT | wx.wx.CENTER | wx.EXPAND, 5)
        volumeSizer.Add(self.ampSliderText1, 0,  wx.RIGHT | wx.CENTER | wx.EXPAND, 5)
        volumeSizer.Add(self.ampSliderText2, 0, wx.BOTTOM | wx.RIGHT | wx.CENTER | wx.EXPAND, 5)
        volumeSizer.Add(self.ampSlider, 1, wx.TOP | wx.BOTTOM | wx.RIGHT | wx.CENTER | wx.EXPAND, 5)
        
        buttonSizer.Add(self.chooseSndText, 0, wx.TOP | wx.BOTTOM | wx.CENTER,5 )
        buttonSizer.Add(self.chooseSnd, 0, wx.TOP | wx.BOTTOM | wx.CENTER, 2)
        buttonSizer.Add(self.playPause, 0, wx.TOP | wx.BOTTOM | wx.CENTER, 2)
        buttonSizer.Add(self.stopBtn, 0, wx.TOP | wx.BOTTOM | wx.CENTER, 2) # FL 02/09/2017
        
#        controlSizer.Add(buttonSizer, 0, wx.ALL | wx.CENTER, 5)
#        controlSizer.Add(radiusSizer, 0, wx.ALL | wx.CENTER, 5)
#        controlSizer.Add(volumeSizer, 0, wx.ALL | wx.CENTER, 5)

#        waveform.Add(self.timeSlider, 0, wx.ALL | wx.EXPAND, 5)     FL 02/09/2017   
        waveform.Add(self.sndView, 1, wx.TOP | wx. BOTTOM | wx.EXPAND, 5)
#                
#        upSizer.Add(controlSizer,0, wx.ALL | wx.EXPAND, 5)        FL 02/09/2017 
#        upSizer.Add(surfaceSizer, 0, wx.ALL | wx.EXPAND, 5)FL 02/09/2017 
#        upSizer.Add(self.meter, 0, wx.ALL | wx.EXPAND, 5)FL 02/09/2017 
#        
#        downSizer.Add(self.waveform, 0, wx.ALL | wx.EXPAND, 5)     FL 02/09/2017    

        # FL 02/09/2017 START
        vuMeterSizer.Add(self.meter, 1, wx.LEFT | wx.RIGHT | wx.CENTER | wx.EXPAND, 10)
        infoSizer.Add(self.infoText1, 0, wx.ALIGN_RIGHT | wx.TOP | wx.RIGHT, 5)
        infoSizer.Add(self.infoText2, 0, wx.ALIGN_RIGHT | wx.BOTTOM | wx.RIGHT, 5)
        songInfoSizer.Add((5,1), 1)
        songInfoSizer.Add(self.chrono, 0, wx.ALL|wx.ALIGN_LEFT, 2)
        songInfoSizer.Add((1,1), 5)
        songInfoSizer.Add(self.sndName, 0, wx.CENTER | wx.ALL | wx.ALIGN_CENTER, 2)
        songInfoSizer.Add((1,1), 5)
        songInfoSizer.Add(self.timeLeft, 0, wx.ALL|wx.ALIGN_LEFT , 2)
        songInfoSizer.Add((5,1), 1)
        oscSizer.Add(self.oscText1, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.CENTER, 5)
        oscSizer.Add(self.oscPort, 0, wx.BOTTOM | wx.LEFT | wx.RIGHT | wx.CENTER, 5)
        
        frameSizer.Add(buttonSizer, (0,0), (1,2), wx.ALL | wx.EXPAND | wx.CENTER)
        frameSizer.Add(waveform, (0,2), (1,2), wx.ALL | wx.EXPAND)
        frameSizer.Add(songInfoSizer, (1,2), (1,1), wx.BOTTOM | wx.EXPAND, 5)
        frameSizer.Add(radiusSizer, (1,0), (2,1), wx.ALL | wx.EXPAND)
        frameSizer.Add(volumeSizer, (1,1), (2,1), wx.ALL | wx.EXPAND)
        frameSizer.Add(surfaceSizer, (2,2), (1,1), wx.ALL | wx.EXPAND)
        frameSizer.Add(vuMeterSizer, (1,3), (3,1), wx.ALL | wx.EXPAND)
        frameSizer.Add(oscSizer, (4,0), (1, 2), wx.ALL | wx.EXPAND, 5)
        frameSizer.Add(infoSizer, (4,2), (1, 2), wx.ALL | wx.EXPAND, 5)
        # FL 02/09/2017 END
        
        self.panel.SetSizerAndFit(frameSizer)
        self.Fit() # FL 02/09/2017
        self.CenterOnScreen() # FL 02/09/2017
        # END JR 31 mai 2017
        
##### METHODES #####

    def playSnd(self,e):
        if e.GetInt() == 1:
            if self.playPause.GetLabel() == "Play":
                self.playPause.SetLabel("Pause") # FL 02/09/2017
                self.audio.player.setOffset(self.sndOffset)
                self.audio.player.play()
                self.initTime = time.time()
                self.isPlaying = True # FL 02/09/2017
                self._whenPlaying() # FL 02/09/2017
        else:
            self.isPlaying = False # FL 02/09/2017
            self.playPause.SetLabel("Play")
            self.audio.player.stop()
            self.sndOffset += self.elapsedTime
            
    # FL 02/09/2017 START
    def stopSnd(self,e):
        if self.audio.player.isPlaying():
            self.playPause.SetLabel("Play")
            self.audio.player.stop()
            self.playPause.SetValue(0)
            self.isPlaying = False
        self.sndOffset = 0.0
        self.sndView.refreshPos(0)
        self.chrono.SetLabel(self.secs2Time(0))
        self.timeLeft.SetLabel("- "+ self.secs2Time(self.sndDurSecs))
    # FL END
    
    # FL 02/09/2017 START
    def sndEnd(self):
        if self.audio.player.isPlaying():
            self.audio.player.stop()
        self.playPause.SetLabel("Play")
        self.playPause.SetValue(0)
        self.isPlaying = False
        self.sndOffset = 0.0
        self.chrono.SetLabel(self.secs2Time(0))
        self.timeLeft.SetLabel("- "+ self.secs2Time(self.sndDurSecs))
        self.sndView.refreshPos(0)
    # FL END
            
    def loadSnd(self,e):
        wildcard = "All files|*.*|" \
               "AIFF file|*.aif;*.aiff;*.aifc;*.AIF;*.AIFF;*.Aif;*.Aiff|" \
               "Wave file|*.wav;*.wave;*.WAV;*.WAVE;*.Wav;*.Wave"
        dlg = wx.FileDialog(self, message="Choose a new soundfile...", 
                            wildcard=wildcard, style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if path != "":
                # FL 10/02/2017 START
                try:
    #                self.chooseSnd.SetLabel("Ready")
                    self.stopSnd(e)
                    self.audio.changeSnd(path)
                    self.sndDurSecs = sndinfo(path)[1] # FL 02/09/2107
                    self.chrono.SetLabel(self.secs2Time(0))
                    self.timeLeft.SetLabel("- "+ self.secs2Time(self.sndDurSecs))
                    self.sndName.SetLabel(os.path.split(path)[1])
                except:
                    self.audio.changeSnd(EMPTY_AUDIO_FILE)
                    self.chrono.SetLabel("--:--:--.--")
                    self.timeLeft.SetLabel("- --:--:--.--")
                    self.sndName.SetLabel("<WAV or AIFF soundfiles only>")
                if self.audio.noSound:
                    self.playPause.Disable()
                    self.stopBtn.Disable()
                else:
                    self.playPause.Enable()
                    self.stopBtn.Enable()
                # FL END
        dlg.Destroy()        
        self.Refresh()

    # J'ai tellement pas de mérite j'ai pris cette fonction sur Internet lol
    # FL 02/09/2017
    def secs2Time(self, secs):
        m, s = divmod(secs, 60)
        h, m = divmod(m, 60)
        pattern = '%%02d:%%02d:%%0%d.%df' % (5, 2)
        return pattern % (h, m, s)

    def changePort(self,e):
        server = vars.getVars("OSCServer")
        print threading.enumerate()
    
    #FL 02/09/2017
    def _whenPlaying(self):
        if self.isPlaying:
            self.elapsedTime = time.time() - self.initTime
            total = self.elapsedTime + self.sndOffset
            try:
                pos = total / self.sndDurSecs
            except:
                pos = 0
            if pos < 1:
                self.chrono.SetLabel(self.secs2Time(total))
                self.timeLeft.SetLabel("- "+ self.secs2Time(self.sndDurSecs-total))
                self.sndView.refreshPos(pos)
                wx.CallLater(5, self._whenPlaying)
            elif pos >= 1:
                self.sndEnd()
        
    def quit(self,e):
        if os.path.isfile(EMPTY_AUDIO_FILE):
            os.remove(EMPTY_AUDIO_FILE)
        audio = vars.getVars("Audio")
        audio.server.stop()
        try:
            self.audio.unregisterMeter()
        except:
            pass
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
        for i in range(len(speakers)):
            speakers[i].setZoneRad(x)
        self.surface.speakerAdjusted()
        self.surface.Refresh()
            
    def masterAmp(self,e):
        x = e.value
        audio = vars.getVars("Audio")
        if x == -60:
            audio.player.mul = 0
        else:
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
        