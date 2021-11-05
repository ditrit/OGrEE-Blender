import bpy
import bmesh
from bpy import context as C
from mathutils import Vector
import mathutils
from os.path import expanduser
import os
import platform as plat
import json
from sys import platform

scale_modifer_diviser = 2
path_project_main = os.path.abspath(os.path.dirname(__file__))

if platform == "win32":
    path_data = path_project_main + "\\data\\"
else:
    path_data = path_project_main + "/data/"

jsonf = json.load(open(path_data + "config.json"))

def read_data(path):
    f = open(path, "r")
    return f.read()

print("EPIC TEST >> " + path_data)

if platform == "linux":
  path_output = jsonf["paths_linux"]["output"]
  path_input = jsonf["paths_linux"]["input"]
else:
  path_output = jsonf["paths_win32"]["output"]
  path_input = jsonf["paths_win32"]["input"]


def import_export_json():
  try:
    os.mkdir(path_output)
  except:
    print("ERROR: ALREADY EXISTS")
  count_files = len(os.listdir(path_input))
  print (count_files)  
  
  #DELETE BY COLLECTION - START
  collection_name = "Collection"

  # Get the collection from its name
  collection = bpy.data.collections[collection_name]

  # Will collect meshes from delete objects
  meshes = set()

  
  #DELETE BY COLLECTION - END  

  files_folder = 0
  issue_files = ""
  cannot_read_files = ""
  # For each files into folder
  while files_folder < count_files:
    

     #REMOVE ALL OBJECTS AT EACH OBJECT
    # Get objects in the collection if they are meshes
    for obj in [o for o in collection.objects if o.type == 'LIGHT']:
        # Store the internal mesh
        meshes.add( obj.data )
        # Delete the object
        bpy.data.objects.remove( obj )
    for obj in [o for o in collection.objects if o.type == 'CAMERA']:
        # Store the internal mesh
        meshes.add( obj.data )
        # Delete the object
        bpy.data.objects.remove( obj )
    for obj in [o for o in collection.objects if o.type == 'MESH']:
        # Store the internal mesh
        meshes.add( obj.data )
        # Delete the object
        bpy.data.objects.remove( obj )
    context = bpy.context
    f_name = os.listdir(path_input)[files_folder]

    # Open file, read it, save it
    print(files_folder)
    if platform == "win32":
      file_json = open(path_input + "\\" + f_name)
    else:
      file_json = open(path_input + "/" + f_name)
    try:
      data = json.loads(file_json.read())
    except:
      cannot_read_files += f_name + "\n"
      print("ERROR >> ERROR IN JSON")

    try:
      # create a new cube
      cube = bpy.ops.mesh.primitive_cube_add()
      cube = bpy.context.selected_objects[0]
      cube.name = str(os.listdir(path_input)[files_folder])
      # newly created cube will be automatically selected
      bpy.data.objects[str(os.listdir(path_input)[files_folder])].select_set(True)

      # Get objects in the collection if they are meshes
      for obj in [o for o in collection.objects if o.type == 'MESH']:
          # Store the internal mesh
          meshes.add( obj.data )  
    except:
      issue_files += os.listdir(path_input)[files_folder] + "\n"
      print("ERROR : Cannot open file")
    
    try:
      total_size = str(data["sizeWDHmm"])
      total_size = total_size.replace("[", "")
      total_size = total_size.replace("]", "")
      total_size = total_size.split(',')
      x_size = total_size[0]
      x_size.replace(",", "")
      y_size = total_size[1]
      y_size.replace(",", "")
      z_size = total_size[2]
      z_size.replace(",", "")
      print (cube.name + " == " + x_size + " "  + y_size + " " + z_size)
    except:
      print("Cannot find the sizeWDHmm. Wrong JSON.")

    real_name = f_name.replace(".json", "")
    cube.name = real_name
    print (cube.name + " == " + x_size + " "  + y_size + " " + z_size)
    bpy.ops.object.mode_set(mode = 'EDIT')
    me = cube.data
    bm = bmesh.from_edit_mesh(me)
    for f in bm.faces:
        bmesh.ops.translate(bm,
                verts=f.verts,
              vec=mathutils.Vector((float(x_size) / scale_modifer_diviser,float(y_size) / scale_modifer_diviser, float(z_size) / scale_modifer_diviser)) * f.normal)
  
    bmesh.update_edit_mesh(me)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    

    create_subcomponent(data, cube, x_size, y_size, z_size)
    print("Making " + path_output + "\\" + f_name + '.fbx')
    if platform == "win32":
      bpy.ops.export_scene.fbx(filepath=path_output + "\\" + real_name + '.fbx')
    else:
      bpy.ops.export_scene.fbx(filepath=path_output + "/" + real_name + '.fbx')
 
    files_folder += 1

  print("OUTPUT : Issue with :\n" + issue_files)
  print("OUTPUT : Cannot read these files :\n" + cannot_read_files)
  
  print(path_output)

def create_subcomponent(json_part, cube_base, base_x, base_y, base_z):
  print("LENS >> " + str(len(json_part)))
  value_slot = 0
  """ try:
    for value in json_part["slots"]:
        generate_asset(value, cube_base)
        value_slot += 1
  except:
    print("No slots") """
  try:
    for value in json_part["components"]:
        generate_asset(value, cube_base, base_x, base_y, base_z)
        value_slot += 1
  except:
    print("No component... resuming...")
      

def generate_asset(value, cube_base, base_x, base_y, base_z):
  bpy.ops.mesh.primitive_cube_add()
  cube = bpy.context.selected_objects[0]
  
  # SIZE #
  total_size_sub = value["elemSize"]
  total_pos_sub = value["elemPos"]
  total_name_sub = value["location"]
  cube.name = total_name_sub

  # COMMENT PART #
  print("total_size_sub " + str(total_size_sub) + " " + total_name_sub)
  print("total_size_sub[value_slot/components] ==> " + str(total_size_sub))
  
  x_size_sub = str(total_size_sub[0])
  x_size_sub.replace(",", "")
  y_size_sub = str(total_size_sub[1])
  y_size_sub.replace(",", "")
  z_size_sub = str(total_size_sub[2])
  z_size_sub.replace(",", "")

  print("SIZE_SUB ==> " + x_size_sub + ", " + y_size_sub + ", " + z_size_sub)

  bpy.ops.object.mode_set(mode = 'EDIT')
  me = cube.data
  bm = bmesh.from_edit_mesh(me)
  for f in bm.faces:
      bmesh.ops.translate(bm,
              verts=f.verts,
              vec=mathutils.Vector((float(x_size_sub) / scale_modifer_diviser,float(y_size_sub) / scale_modifer_diviser, float(z_size_sub) / scale_modifer_diviser)) * f.normal)
  bmesh.update_edit_mesh(me)
  
  bpy.ops.object.mode_set(mode = 'OBJECT')
  
  # LOCATION #
  x_pos_sub = str(total_pos_sub[0])
  x_pos_sub.replace(",", "")      
  y_pos_sub = str(total_pos_sub[1])
  y_pos_sub.replace(",", "")
  z_pos_sub = str(total_pos_sub[2])
  z_pos_sub.replace(",", "")
  pos_x = float(x_pos_sub) + (float(x_size_sub) / 2)
  pos_y = float(y_pos_sub) + (float(y_size_sub) / 2)
  pos_z = float(z_pos_sub) + (float(z_size_sub) / 2)
  f_pos_x = float(base_x) / 2 - pos_x
  f_pos_y = float(base_y) / 2 - pos_y
  f_pos_z = float(base_z) / 2 - pos_z
  cube.location = (float(f_pos_x), float(f_pos_y), float(f_pos_z))
  objects = bpy.data.objects
  cube.parent = cube_base

def debug_cube():
      bpy.ops.mesh.primitive_cube_add()
      cube = bpy.context.selected_objects[0]
      cube.location = (0, 0, 0)

import_export_json()