import bpy
import bmesh
from bpy import context as C
from mathutils import Vector
import mathutils
from os.path import expanduser
import os
import platform as plat
import json

scale_modifer_diviser = 2

class custom_export(bpy.types.Operator):
    bl_label = "Export"
    bl_idname = "properties.export_fbx"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {"REGISTER", "UNDO"}
        
    def execute(self, context):
        if plat.system() == "Windows":
            import_export_json()
            return {"FINISHED"}
        else:
            print("Linux")
            os.mkdir(str(expanduser("~documents")) + "\\ogree_output")
            bpy.ops.export_scene.fbx(filepath=str(expanduser("~documents")) + '\\ogree_output\\export.fbx', axis_forward='-Z', axis_up='Y')
            return {"FINISHED"}

class ogreeManagement(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "OGREE MANAGER"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        # Create an row where the buttons are aligned to each other.
        layout.label(text=" Make two folders into MyDocuments: output_path & input_path.")
        layout.label(text=" Set your files into input_path, then export.")
        layout.label(text="")
        layout.label(text=" JSON Path (all in one folder)")
        col = self.layout.column(align = True)   
        col.prop(scene, "output_path") 
        col.prop(scene, "input_path") 
        row = layout.row()
        layout.operator("properties.export_fbx")    


def register():
    bpy.utils.register_class(ogreeManagement)
    bpy.types.Scene.input_path = bpy.props.StringProperty \
      (
        name = "MyDocuments - Input Path",
        description = "Type your input path into MyDocuments folder",
        default = "input"
      )
    bpy.types.Scene.output_path = bpy.props.StringProperty \
      (
        name = "MyDocuments - Output Path",
        description = "Type your output path into MyDocuments folder",
        default = "output"
      )
      
    bpy.utils.register_class(custom_export)


def unregister():
    bpy.utils.unregister_class(ogreeManagement)
    bpy.utils.unregister_class(custom_export)
    del bpy.types.Scene.input_path
    del bpy.types.Scene.output_path

if __name__ == "__main__":
    register()

def import_export_json():
  try:
    os.mkdir(str(expanduser("~/documents")) + "\\ogree_output\\")
  except:
    print("ERROR: ALREADY EXISTS")
  path = expanduser("~/documents") + "\\ogree_input\\"
  count_files = len(os.listdir(path))
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
  # For each files into folder
  while files_folder < count_files:
    

    #REMOVE ALL OBJECTS AT EACH OBJECT
    # Get objects in the collection if they are meshes
    for obj in [o for o in collection.objects if o.type == 'MESH']:
        # Store the internal mesh
        meshes.add( obj.data )
        # Delete the object
        bpy.data.objects.remove( obj )
    context = bpy.context
    f_name = os.listdir(path)[files_folder]

    # Open file, read it, save it
    print(files_folder)
    file_json = open(path + "\\" + f_name)
    data = json.loads(file_json.read())

    try:

       # create a new cube
      cube = bpy.ops.mesh.primitive_cube_add()
      cube = bpy.context.selected_objects[0]
      cube.name = str(os.listdir(path)[files_folder])
      # newly created cube will be automatically selected
      bpy.data.objects[str(os.listdir(path)[files_folder])].select_set(True)

      # Get objects in the collection if they are meshes
      for obj in [o for o in collection.objects if o.type == 'MESH']:
          # Store the internal mesh
          meshes.add( obj.data )  
    except:
      issue_files += os.listdir(path)[files_folder] + "\n"
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

    try:
      print (cube.name + " == " + x_size + " "  + y_size + " " + z_size)
      bpy.ops.object.mode_set(mode = 'EDIT')
      me = cube.data
      bm = bmesh.from_edit_mesh(me)
      for f in bm.faces:
          bmesh.ops.translate(bm,
                  verts=f.verts,
                  vec=mathutils.Vector((float(x_size) / scale_modifer_diviser,float(z_size) / scale_modifer_diviser, float(y_size) / scale_modifer_diviser)) * f.normal)
    
      bmesh.update_edit_mesh(me)

      bpy.ops.object.mode_set(mode = 'OBJECT')
      
      try:
        print("Test")

      except:
        print("ERROR >> NO SLOT OR COMPONENT FIELD")
      
      create_subcomponent(data, cube)
      bpy.ops.export_scene.fbx(filepath=str(expanduser("~/documents")) + '\\ogree_output\\' + f_name + '.fbx')

    except:
      print("ERROR : Cannot export.")

    
    files_folder += 1 

  print("OUTPUT : Issue with :\n" + issue_files)

def create_subcomponent(json_part, cube_base):
  print("LENS >> " + str(len(json_part)))
  value_slot = 0
  try:
    for value in json_part["slots"]:
        generate_asset(value, value_slot, cube_base)
        value_slot += 1
  except:
    print("No slots")
    
  try:
    for value in json_part["components"]:
        generate_asset(value, value_slot, cube_base)
        value_slot += 1
  except:
    print("No slots")
      

def generate_asset(value, value_slot, cube_base):
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
              vec=mathutils.Vector((float(x_size_sub) / scale_modifer_diviser,float(z_size_sub) / scale_modifer_diviser, float(y_size_sub) / scale_modifer_diviser)) * f.normal)
  bmesh.update_edit_mesh(me)
  
  bpy.ops.object.mode_set(mode = 'OBJECT')
  
  # LOCATION #
  x_pos_sub = str(total_pos_sub[0])
  x_pos_sub.replace(",", "")      
  y_pos_sub = str(total_pos_sub[1])
  y_pos_sub.replace(",", "")
  z_pos_sub = str(total_pos_sub[2])
  z_pos_sub.replace(",", "")
  cube.location = (float(x_pos_sub) / scale_modifer_diviser, float(z_pos_sub) / scale_modifer_diviser, float(y_pos_sub) / scale_modifer_diviser)
  objects = bpy.data.objects
  cube.parent = cube_base

def debug_cube():
      bpy.ops.mesh.primitive_cube_add()
      cube = bpy.context.selected_objects[0]
      cube.location = (0, 0, 0)