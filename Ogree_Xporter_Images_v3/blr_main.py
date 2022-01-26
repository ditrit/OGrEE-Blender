import bpy
from bpy import context, data, ops
import os

bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects['Camera'].select_set(True) # Blender 2.8x
bpy.data.objects['Light'].select_set(True) # Blender 2.8x
bpy.data.objects['Cube'].select_set(True) # Blender 2.8x
bpy.ops.object.delete()

bpy.ops.import_scene.fbx( filepath = os.path.dirname(__file__) + "/models/classic_disk.fbx" )

mat = bpy.data.materials.new(name="Disk")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
texImage.image = bpy.data.images.load(os.path.dirname(__file__) + "/temp/out.png")
mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

ob = bpy.data.objects['disk']

# Assign it to object
if ob.data.materials:
    ob.data.materials[0] = mat
else:
    ob.data.materials.append(mat)

nbfile = len(os.listdir(os.path.dirname(__file__) + "/outputs/"))
bpy.ops.export_scene.fbx(filepath = os.path.dirname(__file__) + "/outputs/hardisk_" + str(nbfile) + ".fbx")