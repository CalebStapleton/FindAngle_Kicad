import os
import pcbnew
from .find_90_v10 import find_90_v10

class AngleDetectorPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        # Human-readable button properties
        self.name = "90° Track Junction Detector"
        self.category = "Design Review"
        self.description = "Scans PCB tracks to find risky 90-degree trace intersections."
        
        # UI visibility settings
        self.show_on_toolbar = True 
        
        # Absolute path calculation to find the icon file relative to this script
        plugin_dir = os.path.dirname(os.path.dirname(__file__))
        self.icon_file_name = os.path.join(plugin_dir, "resources", "icon.png")

    def Run(self):
        # Executes your refactored geometric calculation function
        find_90_v10()

# Register the plugin object natively within KiCad 10
AngleDetectorPlugin().register()
