#!/usr/bin/env python
# encoding: utf-8

#from __future__ import absolute_import
#from ._widgets import PYO_USE_WX
import wx, sys, math

#if not PYO_USE_WX:
#    NO_WX_MESSAGE = "WxPython must be installed on the system to use pyo's wx widgets."
#    class PyoGuiSndView:

#        def __init__(self, *args, **kwargs):
#            raise Exception(NO_WX_MESSAGE)
#else:
#    import wx
#    import wx.lib.newevent
#    from ._wxwidgets import ControlSlider, VuMeter, Grapher, DataMultiSlider
#    from ._wxwidgets import SndViewTablePanel, HRangeSlider

#    if "phoenix" not in wx.version():
#        wx.QueueEvent = wx.PostEvent

#    # Custom events
#    PyoGuiSndViewMousePositionEvent, EVT_PYO_GUI_SNDVIEW_MOUSE_POSITION = wx.lib.newevent.NewEvent()
#    PyoGuiSndViewSelectionEvent, EVT_PYO_GUI_SNDVIEW_SELECTION = wx.lib.newevent.NewEvent()
    
# Classe de base importée de _wxwidgets (distribution Pyo)
class SndViewTablePanel(wx.Panel):

    def __init__(self, parent, obj=None, mouse_callback=None, select_callback=None):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.refresh_from_selection = False
        self.background_bitmap = None
        self.obj = obj
        self.selstart = self.selend = self.movepos = None
        self.moveSelection = False
        self.createSelection = False
        self.begin = 0
        if self.obj is not None:
            self.chnls = len(self.obj)
            self.end = self.obj.getDur(False)
        else:
            self.chnls = 1
            self.end = 1.0
        self.img = [[]]
        self.mouse_callback = mouse_callback
        self.select_callback = select_callback
        if sys.platform == "win32" or sys.platform.startswith("linux"):
            self.dcref = wx.BufferedPaintDC
        else:
            self.dcref = wx.PaintDC
        self.setImage()
        #FL 02/10/2017
        self.playCursorPos = 0

    def getDur(self):
        if self.obj is not None:
            return self.obj.getDur(False)
        else:
            return 1.0

    def resetSelection(self):
        self.selstart = self.selend = None
        if self.background_bitmap is not None:
            self.refresh_from_selection = True
        self.Refresh()
        if self.select_callback is not None:
            self.select_callback((0.0, 1.0))

    def setSelection(self, start, stop):
        self.selstart = start
        self.selend = stop
        if self.background_bitmap is not None:
            self.refresh_from_selection = True
        self.Refresh()
        if self.select_callback is not None:
            self.select_callback((self.selstart, self.selend))

    def setBegin(self, x):
        self.begin = x

    def setEnd(self, x):
        self.end = x

    def setImage(self):
        if self.obj is not None:
            self.img = self.obj.getViewTable(self.GetSize(), self.begin, self.end)
            wx.CallAfter(self.Refresh)

    def clipPos(self, pos):
        if pos[0] < 0.0: x = 0.0
        elif pos[0] > 1.0: x = 1.0
        else: x = pos[0]
        if pos[1] < 0.0: y = 0.0
        elif pos[1] > 1.0: y = 1.0
        else: y = pos[1]
        if self.obj is not None:
            x = x * ((self.end - self.begin) / self.obj.getDur(False)) + (self.begin / self.obj.getDur(False))
        return (x, y)

    def OnMouseDown(self, evt):
        size = self.GetSize()
        pos = evt.GetPosition()
        if pos[1] <= 0:
            pos = (float(pos[0]) / size[0], 1.0)
        else:
            pos = (float(pos[0]) / size[0], 1. - (float(pos[1]) / size[1]))
        pos = self.clipPos(pos)
        if self.mouse_callback is not None:
            self.mouse_callback(pos)
        self.CaptureMouse()

    def OnRightDown(self, evt):
        size = self.GetSize()
        pos = evt.GetPosition()
        if pos[1] <= 0:
            pos = (float(pos[0]) / size[0], 1.0)
        else:
            pos = (float(pos[0]) / size[0], 1. - (float(pos[1]) / size[1]))
        pos = self.clipPos(pos)
        if evt.ShiftDown():
            if self.selstart is not None and self.selend is not None:
                self.moveSelection = True
                self.movepos = pos[0]
        elif evt.CmdDown():
            self.selstart = self.selend = None
            self.refresh_from_selection = True
            self.Refresh()
            if self.select_callback is not None:
                self.select_callback((0.0, 1.0))
        else:
            self.createSelection = True
            self.selstart = pos[0]
        self.CaptureMouse()

    def OnMotion(self, evt):
        if self.HasCapture():
            size = self.GetSize()
            pos = evt.GetPosition()
            if pos[1] <= 0:
                pos = (float(pos[0]) / size[0], 1.0)
            else:
                pos = (float(pos[0]) / size[0], 1. - (float(pos[1]) / size[1]))
            pos = self.clipPos(pos)
            if evt.LeftIsDown():
                if self.mouse_callback is not None:
                    self.mouse_callback(pos)
            elif evt.RightIsDown():
                refresh = False
                if self.createSelection:
                    self.selend = pos[0]
                    refresh = True
                elif self.moveSelection:
                    diff = pos[0] - self.movepos
                    self.movepos = pos[0]
                    self.selstart += diff
                    self.selend += diff
                    refresh = True
                if refresh:
                    self.refresh_from_selection = True
                    self.Refresh()
                    if self.select_callback is not None:
                        self.select_callback((self.selstart, self.selend))

    def OnMouseUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()
        self.createSelection = self.moveSelection = False

    def create_background(self):
        w,h = self.GetSize()
        self.background_bitmap = wx.EmptyBitmap(w, h)
        dc = wx.MemoryDC(self.background_bitmap)
        gc = wx.GraphicsContext_Create(dc)
        dc.SetBrush(wx.Brush("#FFFFFF"))
        dc.Clear()
        dc.DrawRectangle(0,0,w,h)

        off = h // self.chnls // 2
        gc.SetPen(wx.Pen('#000000', width=1, style=wx.SOLID))
        gc.SetBrush(wx.Brush("#FFFFFF", style=wx.TRANSPARENT))
        dc.SetTextForeground("#444444")
        if sys.platform in "darwin":
            font, ptsize = dc.GetFont(), dc.GetFont().GetPointSize()
            font.SetPointSize(ptsize - 3)
            dc.SetFont(font)
        else:
            font = dc.GetFont()
            font.SetPointSize(8)
            dc.SetFont(font)
        tickstep = w // 10
        if tickstep < 40:
            timelabel = "%.1f"
        elif tickstep < 80:
            timelabel = "%.2f"
        elif tickstep < 120:
            timelabel = "%.3f"
        else:
            timelabel = "%.4f"
        timestep = (self.end - self.begin) * 0.1
        for i, samples in enumerate(self.img):
            y = h // self.chnls * i
            if len(samples):
                gc.DrawLines(samples)
            dc.SetPen(wx.Pen('#888888', width=1, style=wx.DOT))
            dc.DrawLine(0, y+off, w, y+off)
#            for j in range(10):
#                dc.SetPen(wx.Pen('#888888', width=1, style=wx.DOT))
#                dc.DrawLine(j*tickstep, 0, j*tickstep, h)
#                dc.DrawText(timelabel % (self.begin+j*timestep), j*tickstep+2, h-y-12)
            dc.SetPen(wx.Pen('#000000', width=1))
            dc.DrawLine(0, h-y, w, h-y)

        dc.SelectObject(wx.NullBitmap)

    def OnPaint(self, evt):
        w,h = self.GetSize()
        dc = self.dcref(self)
        gc = wx.GraphicsContext_Create(dc)
        dc.SetBrush(wx.Brush("#FFFFFF"))
        dc.Clear()
        dc.DrawRectangle(0,0,w,h)

        if not self.refresh_from_selection:
            self.create_background()

        dc.DrawBitmap(self.background_bitmap, 0, 0)

        if self.selstart is not None and self.selend is not None:
            gc.SetPen(wx.Pen(wx.Colour(0, 0, 0, 64)))
            gc.SetBrush(wx.Brush(wx.Colour(0, 0, 0, 64)))
            if self.obj is not None:
                dur = self.obj.getDur(False)
            else:
                dur = 1.0
            selstartabs = min(self.selstart, self.selend) * dur
            selendabs = max(self.selstart, self.selend) * dur
            if selstartabs < self.begin:
                startpix = 0
            else:
                startpix = ((selstartabs - self.begin) / (self.end - self.begin)) * w
            if selendabs > self.end:
                endpix = w
            else:
                endpix = ((selendabs - self.begin) / (self.end - self.begin)) * w
            gc.DrawRectangle(startpix, 0, endpix - startpix, h)

        # FL 02/10/2017
        if self.playCursorPos <= w and self.playCursorPos >= 0:
            dc.SetPen(wx.Pen('#FF0000', width=2))
            dc.DrawLine(self.playCursorPos,0,self.playCursorPos,h)
        self.refresh_from_selection = False

    # FL 02/10/2017
    def updatePlayCursorPos(self, pos):
        w,h = self.GetSize()
        # Function receives value between 0 and 1.0. This value needs to be converted into absolute pixels.
        pos = math.floor(pos * w)
        self.playCursorPos = pos
        wx.CallAfter(self.Refresh)

    def OnSize(self, evt):
        wx.CallAfter(self.setImage)
        

class GuiSndViewPlayHead(wx.Panel):
    """
    Soundfile display.

    This widget should be used with the SndTable object, which keeps
    soundfile in memory and computes the waveform to display on the GUI.

    To create the bridge between the audio memory and the display, the
    SndTable object must be registered in the PyoGuiSndView object with
    the setTable(object) method.

    The SndTable object will automatically call the update() method to
    refresh the display when the table is modified.
    
    This object is an adaptation of the PyoGuiSndView object from the original Pyo release by Olivier Bélanger.

    :Parent: wx.Panel

    :Args:

        parent: wx.Window
            The parent window.
        pos: wx.Point, optional
            Window position in pixels. Defaults to (0, 0).
        size: wx.Size, optional
            Window size in pixels. Defaults to (300, 200).
        style: int, optional
            Window style (see wx.Window documentation). Defaults to 0.

    """
    def __init__(self, parent, pos=(0, 0), size=(300, 200), style=0):
        wx.Panel.__init__(self, parent, pos=pos, size=size, style=style)
        box = wx.BoxSizer(wx.VERTICAL)
        self._curzoom = (0.0, 1.0)
        self.sndview = SndViewTablePanel(self, None)
        box.Add(self.sndview, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.SetSizer(box)

    def __del__(self):
        if self.sndview.obj is not None:
            self.sndview.obj._setViewFrame(None)
            
    def _setZoom(self, values=None):
            if values is None:
                values = self._curzoom
            dur = self.sndview.getDur()
            self.sndview.setBegin(dur * values[0])
            self.sndview.setEnd(dur * values[1])
            self._curzoom = values
            self.update()

    def update(self):
        """
        Display updating method.

        This method is automatically called by the audio memory
        object (SndTable) when the table is modified.

        The method setTable(obj) must be used to register the audio
        memory object.

        """
        wx.CallAfter(self.sndview.setImage)

    def setTable(self, object):
        """
        Register an audio memory object (SndTable).

        :Args:

            object: SndTable object
                The audio table keeping the sound in memory.

        """
        object._setViewFrame(self)
        self.sndview.obj = object
        self.sndview.setBegin(0.0)
        self.sndview.setEnd(object.getDur(False))
        self.sndview.chnls = len(object)
        self.update()

    # Function that updates the play head position
    def refreshPos(self, pos):
        self.sndview.updatePlayCursorPos(pos)