from PIL import Image
import math
import os
import modules.normal_map_generator as normal

# Variable part - Start
size_max_x = 128
modifier_size_base = 4
# Variable part - End

print("Name of image, format included: ", end="")
name_image = input()
try:
    img = Image.open('resources/' + str(name_image), 'r')
    img_w, img_h = img.size
    background = Image.open('resources/base.png', 'r')

    bg_w, bg_h = background.size

    offset = (0, 0)
    modifier_size =  math.ceil(bg_w / bg_h)
    size_y = math.ceil(size_max_x * (bg_w / bg_h))
    new_size = (size_max_x * modifier_size * modifier_size_base, size_y * modifier_size)
    new_img = img.resize(new_size)
    print("Current size = " + str(new_img))
    background.paste(new_img, offset)
    background.save('temp/out.png')

    # Start blender
    os.chdir("C:\\Program Files\\Blender Foundation\\Blender 3.0")
    print("CMD >> cd " + os.path.dirname(__file__) + "\\blr_main.py")
    os.system("blender --background --python " + os.path.dirname(__file__) + "\\blr_main.py")
except:
    print("Image do not exists in /resources/. Exiting with code 1.")