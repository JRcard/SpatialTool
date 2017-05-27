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
        # Start JR 23 mai 2017
        dlg = PrefDlg()
        dlg.CenterOnScreen() # FL 26/05/2017
        if dlg.ShowModal() == wx.ID_OK:
            # FL START 26/05/17
            dlg.commitPrefs()
            audio = Audio()
            vars.setVars("Audio", audio)
            oscServer = OSCServer()   #JR 21 mai
            vars.setVars("OSCServer", oscServer)   # JR 21 mai
            frame = MyFrame()
            vars.setVars("MainFrame", frame)
            self.SetTopWindow(frame)
            frame.Show()
            return True
#            dlg.Destroy()
            # FL END 26/05/17
        else:
            try: #FL 26/05/17
                dlg.Destroy()
            except: #FL 26/05/17
                pass #FL 26/05/17
        raise SystemExit #FL 26/05/17
        # End JR 23 mai 2017

        


if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
