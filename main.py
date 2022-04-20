from email.policy import default
from PIL import Image
import PIL
import math
import os
import normal_map_generator as normal
import json
import requests
import glob
import math
import argparse
import logging as log

# Variable part - Start
modifier_size_base = 4
modifier_size_modifier = 1.5
# Variable part - End

def create_total_mesh(input, output, resolution, blender_path, args):
    name_image = input
    potential_json = glob.glob("inputs/**/" + input + ".json", recursive=True)
    for item in potential_json:
        if item.endswith(".json"):
            json_component =  json.load(open(item, 'r'))
            
    # Taking image from source - end
    tex = glob.glob("inputs/" + input + "/**/*.png", recursive=True)
    background = PIL.Image.new(mode="RGB", size=(resolution, resolution))
    bg_w, bg_h = background.size

    for item in tex:
        if item.endswith("front.png"):
            img_front_path = item
        if item.endswith("rear.png"):
            img_rear_path = item
        if item.endswith("top.png"):
            img_top_path = item
        if item.endswith("bottom.png"):
            img_bottom_path = item
        if item.endswith("right.png"):
            img_right_path = item
        if item.endswith("left.png"):
            img_left_path = item
    
    try:
        img_front = Image.open(img_front_path, "r")
        # Front - start
        offset = (0, 0)
        modifier_size =  math.ceil(bg_w / bg_h)
        size_y = math.ceil(resolution/4 * (bg_w / bg_h) / modifier_size_modifier)
        new_size = (math.ceil(resolution/4 * modifier_size * modifier_size_base), size_y * modifier_size)
        new_img = img_front.resize(new_size)
        background.paste(new_img, offset)
        # Front - end
    except:
        print("No front")
    try:
        img_rear = Image.open(img_rear_path, "r")
        # Back - start
        img_x_rear, img_y_rear = new_size
        offset = (0, img_y_rear)
        modifier_size =  math.ceil(bg_w / bg_h)
        size_y = math.ceil(resolution/4 * (bg_w / bg_h) / modifier_size_modifier)
        new_size = (math.ceil(resolution/4 * modifier_size * modifier_size_base), size_y * modifier_size)
        new_img = img_rear.resize(new_size)
        background.paste(new_img, offset)
        # Back - end
    except:
        print("No rear")
    try:
        img_right = Image.open(img_right_path, "r")
        # Right - start
        img_x_right, img_y_right = new_size
        offset = (0, img_y_right + img_y_rear)
        modifier_size =  math.ceil(bg_w / bg_h)
        size_y = math.ceil(resolution/4 * (bg_w / bg_h) / modifier_size_modifier)
        new_size = (math.ceil(resolution/4 * modifier_size * modifier_size_base), size_y * modifier_size)
        new_img = img_right.resize(new_size)
        background.paste(new_img, offset)
        # Right - end
    except:
        print("No right")
    try:
        img_left = Image.open(img_left_path, "r")
        # Left - start
        img_x_left, img_y_left = new_size
        offset = (0, img_y_left + img_y_right + img_y_rear)
        modifier_size =  math.ceil(bg_w / bg_h)
        size_y = math.ceil(resolution/4 * (bg_w / bg_h) / modifier_size_modifier)
        new_size = (math.ceil(resolution/4 * modifier_size * modifier_size_base), size_y * modifier_size)
        new_img = img_left.resize(new_size)
        background.paste(new_img, offset)
        # Left - end
    except:
        print("No left")
    try:
        img_top = Image.open(img_top_path, "r")
        # Top - start
        img_x_top, img_y_top = new_size
        offset = (0, img_y_left + img_y_right + img_y_rear + img_y_top)
        modifier_size =  math.ceil(bg_w / bg_h)
        size_y = math.ceil(resolution/4 * (bg_w / bg_h) / modifier_size_modifier)
        new_size = (math.ceil(resolution/4 * modifier_size * modifier_size_base), size_y * modifier_size)
        new_img = img_top.resize(new_size)
        background.paste(new_img, offset)
        # Top - end
    except:
        print("No top")
    try:
        img_bottom = Image.open(img_bottom_path, "r")
        # Bottom - start
        img_x_bottom, img_y_bottom = new_size
        offset = (0, img_y_left + img_y_right + img_y_rear + img_y_top + img_y_right)
        modifier_size =  math.ceil(bg_w / bg_h)
        size_y = math.ceil(resolution/4 * (bg_w / bg_h) / modifier_size_modifier)
        new_size = (math.ceil(resolution/4 * modifier_size * modifier_size_base), size_y * modifier_size)
        new_img = img_bottom.resize(new_size)
        background.paste(new_img, offset)
        # Bottom - end
    except:
        print("No bottom")
    # Recover image - end

    background.save('temp/out.png')

    normal.generate_definitive_normal(os.environ + '/out.png', os.environ + '/normal.png', 0.5, 1)

    # Start blender
    os.chdir(blender_path)
    print("CMD >> cd " + os.path.dirname(__file__) + "/blr_main.py")
    os.system("blender --background --python " + os.path.dirname(__file__) + "/blr_main.py")

#Script
parser = argparse.ArgumentParser(description='Create a mesh for OGrEE 3D.')
    
parser.add_argument('-i', '--object', default="/inputs", type=str, help='Object to build')
parser.add_argument('-o', '--output', default=os.path.dirname(__file__) + "/outputs", type=str, help='Folder base for creating mesh')
parser.add_argument('-r', '--resolution', default=512, type=int, help='Texture resolution')
parser.add_argument('-b', '--blender', type=str, help='Blender path')
args = parser.parse_args()
mesh_to_build = args.object
output_folder_mesh = args.output_folder_mesh
resolution = args.resolution
blender_path = args.blender
create_total_mesh(mesh_to_build, output_folder_mesh, resolution, blender_path, args)
    

