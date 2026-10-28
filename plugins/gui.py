import wx

class gui(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Find Trace Angle", pos = wx.DefaultPosition, size = wx.Size( 326,496 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer = wx.BoxSizer( wx.VERTICAL )


        # Static text
        self.m_staticText = wx.StaticText(self, wx.ID_ANY, u"Find Trace Angle of ", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer.Add(self.m_staticText, 0, wx.ALL, 12)

        # Data field for the trace angle
        self.m_dataField = wx.TextCtrl(self, wx.ID_ANY, u"90.0", (self.m_staticText.GetPosition().x + 100, self.m_staticText.GetPosition().y), wx.DefaultSize, 0)
        bSizer.Add(self.m_dataField, 0, wx.ALL|wx.EXPAND, 12)

        self.m_buttonOK = wx.Button(self, wx.ID_OK, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_buttonOK.SetDefault()
        bSizer.Add(self.m_buttonOK, 0, wx.ALL|wx.ALIGN_RIGHT, 12)

        self.SetSizer(bSizer)
        self.Layout()
        self.Centre(wx.BOTH)

    def GetValue(self):
        return self.m_dataField.GetValue()

    