import os
import pcbnew
import wx
from .action_findAngle import find_angle
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
        plugin_dir = os.path.dirname(os.path.dirname(__file__))
        self.icon_file_name = os.path.join(plugin_dir, "resources", "icon.png")

    def Run(self):

        dlg = gui(None)

        if dlg.ShowModal() == wx.ID_OK:
            userInput = dlg.GetValue()

            find_angle(userInput)

        dlg.Destroy()


# Register the plugin object natively within KiCad 10
AngleDetectorPlugin().register()