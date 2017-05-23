#!/usr/bin/env python
# encoding: utf-8

import wx, os
from Resources.MainFrame import *
from Resources.Audio import Audio
from Resources.OSCServer import * #JR 21 mai
import Resources.Variables as vars
from Resources.Pref import * # JR 22 mai

class MyApp(wx.App):
    
    def OnInit(self):
#        dlg = PrefDlg()
#        dlg.Show()
#        if dlg.isOk():
#            dlg.setPref()
#            dlg.Destroy()
        audio = Audio()
        vars.setVars("Audio", audio)
        oscServer = OSCServer()   #JR 21 mai
        vars.setVars("OSCServer", oscServer)   # JR 21 mai
        frame = MyFrame()
        vars.setVars("MainFrame", frame)
        self.SetTopWindow(frame)
        frame.Show()
        return True
        

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
    

# SO FUN!
