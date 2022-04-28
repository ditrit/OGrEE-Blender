import json
import bpy
import bmesh
#from mathutils import Vector
#import mathutils
from bpy import context, data, ops
import os
import logging
import sys

argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"

json_file       = argv[0]
output_dir      = argv[1]
basefile        = os.path.basename(json_file)                                            # huawei-tnf6dwss9.json
background_file = os.environ.get("TMP") + "/" + basefile.replace(".json",".out.png")     # /tmp/huawei-tnf6dwss9.out.png
normalmap_file  = os.environ.get("TMP") + "/" + basefile.replace(".json",".normal.png")  # /tmp/huawei-tnf6dwss9.normal.png
fbx_file        = argv[1] + "/" +basefile.replace(".json",".fbx")

def resize_model(obj):

    json_f = open(json_file, "r")
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
    
    obj.name = os.path.basename(json_file)
    print (obj.name + " == " + x_size + " "  + y_size + " " + z_size)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode = 'EDIT')
    me = obj.data
    #bm = bmesh.from_edit_mesh(me)
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

#
# Blender parameters 
#
bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects['Camera'].select_set(True) # Blender 2.8x
bpy.data.objects['Light'].select_set(True) # Blender 2.8x
bpy.data.objects['Cube'].select_set(True) # Blender 2.8x
bpy.ops.object.delete()

bpy.ops.import_scene.fbx( filepath = os.path.dirname(__file__) + "/models/model.fbx" )

#
# - - - TEXTURE PART - - -
#
mat = bpy.data.materials.new(name="Main")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
texImage.image = bpy.data.images.load(background_file)
mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

# - - - NORMAL PART - - -
# Creating normal map
##norm = mat.node_tree.nodes.new["Normal Map"]

# Creating image for normal map
norm = mat.node_tree.nodes.new('ShaderNodeTexImage')
norm.image = bpy.data.images.load(normalmap_file)
mat.node_tree.links.new(bsdf.inputs['Normal'], norm.outputs['Color'])

ob = bpy.data.objects['model']

resize_model(ob)

# Assign it to object
if ob.data.materials:
    ob.data.materials[0] = mat
else:
    ob.data.materials.append(mat)

bpy.ops.export_scene.fbx(filepath = fbx_file, path_mode = "COPY", embed_textures = True)
