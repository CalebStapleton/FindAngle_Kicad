import os
import pcbnew
import wx
from .action_findAngle import find_angle, clear_layer
from .gui import gui

class AngleDetectorPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        # Human-readable button properties
        self.name = "90° Track Junction Detector"
        self.category = "Design Review"
        self.description = "Scans PCB tracks to find 90 degree bends"
        
        # UI visibility settings
        self.show_toolbar_button = True 
        
        # Absolute path calculation to find the icon file relative to this script
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "icon.png")

    def Run(self):

        dlg = gui(None)

        result = dlg.ShowModal()
        if result == wx.ID_OK:
            userInput = list(dlg.GetValue())
            angle = userInput[0]
            layer = userInput[1]
            checkPads = userInput[2]
            checkVias = userInput[3]
                
            find_angle(angle, layer, checkPads, checkVias)

        elif result == wx.ID_CLEAR:
            userInput = list(dlg.GetValue())
            layer = userInput[1]
            clear_layer(layer)

        dlg.Destroy()


# Register the plugin object natively within KiCad 10
AngleDetectorPlugin().register()