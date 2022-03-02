from PIL import Image
import math
import os
import modules.normal_map_generator as normal
import json
import requests
import modules.normal_map_generator as normal
import glob

# Variable part - Start
size_max_x = 128
modifier_size_base = 4
modifier_size_modifier = 1.5
# Variable part - End

json_config = json.load(open('resources/config.json', 'r'))
name_image = json_config["selectedModel"]
potential_json = glob.glob("resources/**/" + str(name_image) + ".json", recursive=True)
for item in potential_json:
    if item.endswith(".json"):
        json_component_path = item
json_component =  json.load(open(json_component_path, 'r'))


# Taking image from source - start
try:
    img_front = json_component["textures"]["front"]
    if img_front.startswith('http') or img_front.startswith('https'):
        img_dwnd = requests.get(img_front).content
        file = open("resources/" +  str(name_image) + "/textures/front.png", "wb")
        file.write(img_dwnd)
except:
    print("No front texture")

try:
    img_top = json_component["textures"]["top"]
    if img_top.startswith('http') or img_top.startswith('https'):
        img_dwnd = requests.get(img_top).content
        file = open("resources/" +  str(name_image) + "/textures/top.png", "wb")
        file.write(img_dwnd)
except:
    print("No top texture")

try:
    img_rear = json_component["textures"]["rear"]
    if img_rear.startswith('http') or img_rear.startswith('https'):
        img_dwnd = requests.get(img_rear).content
        file = open("resources/" +  str(name_image) + "/textures/rear.png", "wb")
        file.write(img_dwnd)
except:
    print("No rear texture")
try:
    img_bottom = json_component["textures"]["bottom"]
    if img_bottom.startswith('http') or img_bottom.startswith('https'):
        img_dwnd = requests.get(img_bottom).content
        file = open("resources/" +  str(name_image) + "/textures/bottom.png", "wb")
        file.write(img_dwnd)
except:
    print("No bottom texture")
try:
    img_right = json_component["textures"]["right"]
    if img_right.startswith('http') or img_right.startswith('https'):
        img_dwnd = requests.get(img_right).content
        file = open("resources/" +  str(name_image) + "/textures/right.png", "wb")
        file.write(img_dwnd)
except:
    print("No right texture")
try:
    img_left = json_component["textures"]["left"]
    if img_left.startswith('http') or img_left.startswith('https'):
        img_dwnd = requests.get(img_left).content
        file = open("resources/" +  str(name_image) + "/textures/left.png", "wb")
        file.write(img_dwnd)
except:
    print("No left texture")
# Taking image from source - end


tex = glob.glob("resources/"+  str(name_image) + "/**/*.png", recursive=True)
print(tex)

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
except:
    print("No rear")
try:
    img_rear = Image.open(img_rear_path, "r")
except:
    print("No rear")
try:
    img_top = Image.open(img_top_path, "r")
except:
    print("No top")
try:
    img_bottom = Image.open(img_bottom_path, "r")
except:
    print("No bottom")
try:
    img_right = Image.open(img_right_path, "r")
except:
    print("No right")
try:
    img_left = Image.open(img_left_path, "r")
except:
    print("No left")
# Recover image - end

img_w, img_h = img_front.size
background = Image.open('resources/base.png', 'r')

bg_w, bg_h = background.size

# Front - start
offset = (0, 0)
modifier_size =  math.ceil(bg_w / bg_h)
size_y = math.ceil(size_max_x * (bg_w / bg_h) / modifier_size_modifier)
new_size = (size_max_x * modifier_size * modifier_size_base, size_y * modifier_size)
new_img = img_front.resize(new_size)
background.paste(new_img, offset)
# Front - end

# Back - start
img_x_rear, img_y_rear = new_size
offset = (0, img_y_rear)
modifier_size =  math.ceil(bg_w / bg_h)
size_y = math.ceil(size_max_x * (bg_w / bg_h) / modifier_size_modifier)
new_size = (size_max_x * modifier_size * modifier_size_base, size_y * modifier_size)
new_img = img_rear.resize(new_size)
background.paste(new_img, offset)
# Back - end

# Right - start
img_x_right, img_y_right = new_size
offset = (0, img_y_right + img_y_rear)
modifier_size =  math.ceil(bg_w / bg_h)
size_y = math.ceil(size_max_x * (bg_w / bg_h) / modifier_size_modifier)
new_size = (size_max_x * modifier_size * modifier_size_base, size_y * modifier_size)
new_img = img_right.resize(new_size)
background.paste(new_img, offset)
# Right - end

# Left - start
img_x_left, img_y_left = new_size
offset = (0, img_y_left + img_y_right + img_y_rear)
modifier_size =  math.ceil(bg_w / bg_h)
size_y = math.ceil(size_max_x * (bg_w / bg_h) / modifier_size_modifier)
new_size = (size_max_x * modifier_size * modifier_size_base, size_y * modifier_size)
new_img = img_left.resize(new_size)
background.paste(new_img, offset)
# Left - end

# Top - start
img_x_top, img_y_top = new_size
offset = (0, img_y_left + img_y_right + img_y_rear + img_y_top)
modifier_size =  math.ceil(bg_w / bg_h)
size_y = math.ceil(size_max_x * (bg_w / bg_h) / modifier_size_modifier)
new_size = (size_max_x * modifier_size * modifier_size_base, size_y * modifier_size)
new_img = img_top.resize(new_size)
background.paste(new_img, offset)
# Top - end

# Bottom - start
img_x_right, img_y_right = new_size
offset = (0, img_y_left + img_y_right + img_y_rear + img_y_top + img_y_right)
modifier_size =  math.ceil(bg_w / bg_h)
size_y = math.ceil(size_max_x * (bg_w / bg_h) / modifier_size_modifier)
new_size = (size_max_x * modifier_size * modifier_size_base, size_y * modifier_size)
new_img = img_bottom.resize(new_size)
background.paste(new_img, offset)
# Bottom - end

background.save('temp/out.png')

normal.generate_definitive_normal('temp/out.png', 'temp/normal.png', 0.5, 1)

# Start blender
os.chdir("C:\\Program Files\\Blender Foundation\\Blender 3.0")
print("CMD >> cd " + os.path.dirname(__file__) + "\\blr_main.py")
os.system("blender --background --python " + os.path.dirname(__file__) + "\\blr_main.py")
