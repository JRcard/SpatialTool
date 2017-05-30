#!/usr/bin/env python
# encoding: utf-8

import wx, os
from Resources.MainFrame import *
from Resources.Audio import Audio
from Resources.OSCServer import *
import Resources.Variables as vars
from Resources.Pref import *

if __name__ == "__main__":  
    app = wx.App(False)

    dlg = PrefDlg()
    dlg.CenterOnScreen()
    val = dlg.ShowModal()
    
    if val == wx.ID_OK:
        # Si on crée une nouvelle configuration
        if dlg.radioNew.GetValue() == 1:
            dlg.commitPrefs()
            pref = vars.getVars("Pref") # FL 29/05/2017
            
            audioIndex = dlg.getOutputDriverIndexFromString(pref["AUDIO_DRIVER"])
            audio = Audio(audioIndex, pref["NCHNLS"], pref["NUM_SPEAKERS"])
            vars.setVars("Audio", audio)
            
            oscServer = OSCServer()
            vars.setVars("OSCServer", oscServer)
            
            frame = MyFrame(numSpeakers=pref["NUM_SPEAKERS"])
            vars.setVars("MainFrame", frame)
            
        # Si on ouvre une configuration existante (TO DO)
        elif dlg.radioOpen.GetValue() == 1:
            try:
                dlg.Destroy()
            except:
                pass
            raise SystemExit
            
        frame.Show()
        app.MainLoop()
    else:
        try:
            dlg.Destroy()
        except:
            pass
        raise SystemExit
