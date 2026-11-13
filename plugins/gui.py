import wx

class gui(wx.Dialog):
    def __init__(self, parent):

        self.layers = [f"User_{i}" for i in range(1, 21)]

        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Find Trace Angle", pos = wx.DefaultPosition, size = wx.Size( 480,360 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer = wx.BoxSizer( wx.VERTICAL )


        # Static text
        self.m_staticText = wx.StaticText(self, wx.ID_ANY, u"Find Trace Angle of ", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer.Add(self.m_staticText, 0, wx.ALL, 12)

        # Data field for the trace angle
        self.angle = wx.TextCtrl(self, wx.ID_ANY, u"90.0", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer.Add(self.angle, 0, wx.ALL|wx.EXPAND, 12)

        # Data field for the angle tolerance
        ########################################################################################################

        angleTolerance = wx.BoxSizer(wx.HORIZONTAL)

        self.m_angleToleranceLabel = wx.StaticText(self, wx.ID_ANY, u"Angle Tolerance ±: ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_tolerance = wx.TextCtrl(self, wx.ID_ANY, u"3.0", wx.DefaultPosition, wx.DefaultSize, 0)
        angleTolerance.Add(self.m_angleToleranceLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        angleTolerance.Add(self.m_tolerance, 0, wx.ALL, 5)

        bSizer.Add(angleTolerance, 0, wx.ALL, 12)

        ########################################################################################################


        self.m_staticText = wx.StaticText(self, wx.ID_ANY, u"Select Layer: ", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer.Add(self.m_staticText, 0, wx.ALL, 12)
        
        self.m_layerChoice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.layers, 0)
        self.m_layerChoice.SetSelection(0) # Select "User_1" by default
        bSizer.Add(self.m_layerChoice, 0, wx.ALL|wx.EXPAND, 12)


        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.m_buttonCancel = wx.Button(self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_buttonCancel.SetDefault()
        button_sizer.Add(self.m_buttonCancel, 0, 0, 0)

        self.m_buttonClear = wx.Button(self, wx.ID_CLEAR, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_buttonClear.Bind(wx.EVT_BUTTON, lambda event: self.EndModal(wx.ID_CLEAR))
        button_sizer.Add(self.m_buttonClear, 0, 0, 0)

        button_sizer.AddStretchSpacer(1)

        
        self.m_buttonOK = wx.Button(self, wx.ID_OK, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        button_sizer.Add(self.m_buttonOK, 0, 0, 0)


        bSizer.Add(button_sizer, 0, wx.ALL | wx.EXPAND, 12)

        self.SetSizer(bSizer)
        self.Layout()
        self.Centre(wx.BOTH)

    def GetValue(self):
        return (float(self.angle.GetValue()),
                self.m_layerChoice.GetStringSelection(),
                float(self.m_tolerance.GetValue()))

    