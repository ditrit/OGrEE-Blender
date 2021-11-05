import modules.init as ogree_init
from sys import platform
import modules.init as blinit
import json
import modules.glovar as glovar
from sys import platform

def start_config():
    jsonf = json.load(open(glovar.path_data + "config.json"))
    if platform == "linux":
        cmd_path_blender = jsonf["paths_linux"]["blender"]
        cmd_path_input = jsonf["paths_linux"]["input"]
        cmd_path_output = jsonf["paths_linux"]["output"]
    else:
        cmd_path_blender = jsonf["paths_win32"]["blender"]
        cmd_path_input = jsonf["paths_win32"]["input"]
        cmd_path_output = jsonf["paths_win32"]["output"]

    print("Starting dependance...")
    blinit.start_blender(cmd_path_blender)
    input()

if platform == "win32" or platform == "linux":   
    print("Start as config")
    start_config()
else:
    print("ERROR >> YOUR OPERATING SYSTEM IS NOT SUPPORTED")
