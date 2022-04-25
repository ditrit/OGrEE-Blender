from email.policy import default
from platform import platform
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

def create_total_mesh(input, resolution, args):
    # Used to generate mesh, not for texturing 
    json_list = glob.glob(input + "/**/" + os.path.basename(input) + "*.json", recursive=True)
    for index in json_list:

        # Set a number to check
        file_witner = open(os.environ.get("TMP") + "/ogree_index.txt", "w")
        file_witner.write(index)
        file_witner.close()

        log.info("Looking for PNGs according to the basename of the input path")        
        # Taking image from source - end
        tex = glob.glob(input + "/**/*.png", recursive=True)
        log.info("Creating base background")
        background = PIL.Image.new(mode="RGB", size=(resolution, resolution))
        bg_w, bg_h = background.size

        log.info("Looking for images one by one")

        final_path = tex[json_list.index(index)]

        log.info("PATH IMAGE >> " + json_list[json_list.index(index)])

        if os.path.exists(final_path):
            log.info("--- NEW IMAGE CREATION ---")
            img_front = Image.open(final_path, "r")
            # Solo image - start
            offset = (0, 0)
            modifier_size =  math.ceil(bg_w / bg_h)
            size_y = math.ceil(resolution/4 * (bg_w / bg_h) / modifier_size_modifier)
            new_size = (math.ceil(resolution/4 * modifier_size * modifier_size_base), size_y * modifier_size)
            new_img = img_front.resize(new_size)
            background.paste(new_img, offset)
            log.info("Saving new image")
            background.save(os.environ.get("TMP") + '/out.png')
            # Start blender
            if platform == "linux":
                log.info("Linux OS detected")
                blender_dir = os.path.dirname(args.blender)
                log.info("Starting Blender from:", blender_dir)
                os.chdir(blender_dir)
            else:
                log.info("Other OS than Linux detected")
                log.info("Starting Blender from:", args.blender)
                os.chdir(args.blender)
            
            log.info("Starting Blender!")
            os.system("blender --background --python " + os.path.dirname(__file__) + "/blr_main.py")
            log.info("Ended texture generation and application!")
        else:
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
            
            log.info("Treatment of FRONT image...")
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
                log.warning("No front")

            log.info("Treatment of REAR image...")
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
                log.warning("No rear")

                
            log.info("Treatment of RIGHT image...")
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
                log.warning("No right")

                
            log.info("Treatment of LEFT image...")
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
                log.warning("No left")

            
            log.info("Treatment of TOP image...")
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
                log.warning("No top")

                
            log.info("Treatment of BOTTOM image...")
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
                log.warning("No bottom")
            # Recover image - end

            log.info("Saving image...")
            background.save(os.environ.get("TMP") + '/out.png')
            log.info("Image saved!")

            log.info("Generating normal map...")
            normal.generate_definitive_normal(os.environ.get("TMP") + '/out.png', os.environ.get("TMP") + '/normal.png', 0.5, 1)
            log.info("Normal map generated...")

            # Start blender
            if platform == "linux":
                log.info("Linux OS detected")
                blender_dir = os.path.dirname(args.blender)
                log.info("Starting Blender from:", blender_dir)
                os.chdir(blender_dir)
            else:
                log.info("Other OS than Linux detected")
                log.info("Starting Blender from:", args.blender)
                os.chdir(args.blender)
            
            log.info("Starting Blender!")
            os.system("blender --background --python " + os.path.dirname(__file__) + "/blr_main.py")
            log.info("Ended texture generation and application!")

#Script
parser = argparse.ArgumentParser(description='Create a mesh for OGrEE 3D.')
    
parser.add_argument('-i', '--object', default="/inputs", type=str, help='Object to build', required=True)
parser.add_argument('-o', '--output', default=os.path.dirname(__file__) + "/outputs", type=str, help='Folder base for creating mesh', required=True)
parser.add_argument('-r', '--resolution', default=512, type=int, help='Texture resolution', required=False)
parser.add_argument('-b', '--blender', type=str, help='Blender path', required=True)
parser.add_argument('-v', '--verbose',
    choices=["INFO", "WARNING", "ERROR", "DEBUG"],
    help="Verbose level",
    default="DEBUG")
args = parser.parse_args()
mesh_to_build = args.object
output_folder_mesh = args.output
resolution = args.resolution
blender_path = args.blender

numeric_level = getattr(log, args.verbose.upper())
log.basicConfig(format="[%(levelname)s][%(asctime)s]: %(message)s", level=numeric_level)

f = open(os.environ.get("TMP") + "/ogree_data.txt", "w")
f.write(mesh_to_build + "\n" + output_folder_mesh)
f.close()

create_total_mesh(mesh_to_build, resolution, args)
    

