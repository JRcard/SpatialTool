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
        dlg.commitPrefs()
        audio = Audio(pref["NCHNLS"], pref["NUM_SPEAKERS"])
        vars.setVars("Audio", audio)
        oscServer = OSCServer()
        vars.setVars("OSCServer", oscServer)
        frame = MyFrame(numSpeakers=pref["NUM_SPEAKERS"])
        vars.setVars("MainFrame", frame)
        frame.Show()
        app.MainLoop()
    else:
        try:
            dlg.Destroy()
        except:
            pass
        raise SystemExit
