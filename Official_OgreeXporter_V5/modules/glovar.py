import os
from sys import platform

path_project_glovar = os.path.abspath(__file__)
path_project_main = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
path_project_modules = path_project_main + "\\modules\\"

if platform == "win32":
    path_data = path_project_main + "\\data\\"
else:
    path_data = path_project_main + "/data/"

path_blender = "C:\\Program Files\\Blender Foundation\\blender-2.93.4-windows-x64"

cmd_blstart_win32 = "blender --background --python " + path_project_main + "\\ogree_final.py"
cmd_blstart_linux = "blender --background --python " + path_project_main + "/ogree_final.py"