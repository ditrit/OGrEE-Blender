import json
import bpy
import bmesh
from mathutils import Vector
import mathutils
from bpy import context, data, ops
import os


def resize_model(obj):
    f = open(os.environ.get("TMP") + "/ogree_index.txt", "r").read()
    file = f.splitlines()
    obj_name = file[0]
    json_f = open(obj_name, "r")
    loaded_json = json.load(json_f)
    try:
      total_size = str(loaded_json["sizeWDHmm"])
      total_size = total_size.replace("[", "")
      total_size = total_size.replace("]", "")
      total_size = total_size.split(',')
      x_size = total_size[0]
      x_size.replace(",", "")
      y_size = total_size[1]
      y_size.replace(",", "")
      z_size = total_size[2]
      z_size.replace(",", "")
    except:
      print("Cannot find the sizeWDHmm. Wrong JSON.")
    
    obj.name = os.path.basename(obj_name)
    print (obj.name + " == " + x_size + " "  + y_size + " " + z_size)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode = 'EDIT')
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    bpy.ops.transform.resize(value=(float(x_size)/100, float(y_size)/100, float(z_size)/100), orient_type='LOCAL')

    obj = context.object
    mb = obj.matrix_basis
    if hasattr(ob.data, "transform"):
      obj.data.transform(mb)
    for c in ob.children:
      c.matrix_local = mb @ c.matrix_local
        
    obj.matrix_basis.identity()

    bmesh.update_edit_mesh(me)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    return obj

bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects['Camera'].select_set(True) # Blender 2.8x
bpy.data.objects['Light'].select_set(True) # Blender 2.8x
bpy.data.objects['Cube'].select_set(True) # Blender 2.8x
bpy.ops.object.delete()

bpy.ops.import_scene.fbx( filepath = os.path.dirname(__file__) + "/models/classic_disk.fbx" )

# - - - TEXTURE PART - - -
mat = bpy.data.materials.new(name="Disk")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
texImage.image = bpy.data.images.load(os.environ.get("TMP") + "/out.png")
mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

# - - - NORMAL PART - - -
# Creating normal map
##norm = mat.node_tree.nodes.new["Normal Map"]

# Creating image for normal map
norm = mat.node_tree.nodes.new('ShaderNodeTexImage')
norm.image = bpy.data.images.load(os.environ.get("TMP") + "/normal.png")
mat.node_tree.links.new(bsdf.inputs['Normal'], norm.outputs['Color'])


ob = bpy.data.objects['disk']


resize_model(ob)

# Assign it to object
if ob.data.materials:
    ob.data.materials[0] = mat
else:
    ob.data.materials.append(mat)

file_name = open(os.environ.get("TMP") + "/ogree_index.txt", "r").read()

f = open(os.environ.get("TMP") + "/ogree_data.txt", "r").read()
file = f.splitlines()
obj_name = file[0]
output = file[1]

bpy.ops.export_scene.fbx(filepath = file[1] + "/" + os.path.basename(file_name).replace(".json", "") + ".fbx", path_mode="COPY", embed_textures=True)
