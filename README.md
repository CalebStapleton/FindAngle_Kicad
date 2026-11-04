## Supported Versions
This project supports KiCad 10.0.0 and later

## Platforms
This project has only been tested on Windows 11

## Setup
 - Download the zip file from the releases
 - Open KiCad Plugin and Content Manager
 - Press the Install from File button and select the zip file
 - Exit Plugin and Content Manager and open project

## Project Structure

``` text
├── FindAngle.zip
└── plugins
    └── init.py
    ├── action_findAngle.py
    ├── gui.py
    ├── icon.png
└── resources
    └── icon.png
└── metadata.json
```
- The project must follow this structure or the PCM will not recognize the json file
- Additionally there cannot be a folder above the main FindAngle folder
