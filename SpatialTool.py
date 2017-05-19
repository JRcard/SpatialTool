#!/usr/bin/env python
# encoding: utf-8

import wx, os
from Resources.MainFrame import *
from Resources.Audio import Audio
import Resources.Variables as vars

class MyApp(wx.App):
    
    def OnInit(self):
        audio = Audio()
        vars.setVars("Audio", audio)
        frame = MyFrame()
        vars.setVars("MainFrame", frame)
        self.SetTopWindow(frame)
        frame.Show()
        return True
        

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
    

# SO FUN!
