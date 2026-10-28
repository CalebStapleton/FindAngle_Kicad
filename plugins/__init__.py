import os
import pcbnew
from .action_find90 import find_angle
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

        parent_window = pcbnew.GetWindow() # fix this
        dlg = gui(parent_window)

        if dlg.ShowModal() == wx.ID_OK:
            userInput = dlg.get_user_input()

            find_angle(userInput)

        dlg.Destroy()


# Register the plugin object natively within KiCad 10
AngleDetectorPlugin().register()