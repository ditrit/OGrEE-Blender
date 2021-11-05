import os
import modules.glovar as glovar
import modules.data_parser as dataparse
from sys import platform

def start_blender(path_blender):
    print("0. Starting Blender...")
    try:
        print("1. Making command: cd " + path_blender)
        os.chdir(path_blender)

        try:
            print("2. Starting export script...")
            if platform == "win32":
                os.system(glovar.cmd_blstart_win32)
            else:
                os.system(path_blender + "/blender --background --python " + glovar.path_project_main + "/ogree_final.py")
        except:
            print("Cannot export JSON to FBX")

        print("Starting Blender has succeed")
    except:
        print("Starting Blender has fail")