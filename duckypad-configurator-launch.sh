#!/bin/bash
# Launch duckyPad Configurator
# Called by Better Touch Tool or directly

cd /Users/erhei/Tools/duckyPad-Configurator
osascript -e 'tell application "Terminal"
    activate
    do script "cd /Users/erhei/Tools/duckyPad-Configurator && sudo .venv/bin/python3 src/duckypad_config.py"
end tell'
