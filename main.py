from PIL import Image
import PIL
import os
import normal_map_generator as normal
import glob
import argparse
import logging



def create_total_mesh(input):
    background = PIL.Image.new(mode="RGB", size=(args['resolution'],args['resolution']))
    logging.info("Looking for PNGs according to the basename of the input path %s",input)    # input = /OGrEE/data/huawei/huawei-tnf6dwss9.json
    basefile = os.path.basename(input)                                                       # huawei-tnf6dwss9.json
    basename = os.path.splitext(input)[0]                                                    # /OGrEE/data/huawei/huawei-tnf6dwss9
    dirname = os.path.dirname(input)
    logging.debug(dirname + "/**/" + basefile.replace(".json","*.png"))
    image_background = os.environ.get("TMP") + "/" + basefile.replace(".json",".out.png")    # /tmp/huawei-tnf6dwss9.out.png
    image_normalmap = os.environ.get("TMP") + "/" + basefile.replace(".json",".normal.png")  # /tmp/huawei-tnf6dwss9.normal.png
    
    offsetY = args['resolution'] // 6
    faces_offset = { 'front':0, 'rear':1, 'right':2, 'left':3, 'top':4, 'bottom':5 }
    textures = glob.glob(dirname + "/**/" + basefile.replace(".json","*.png"), recursive=True)
    logging.debug(textures)    
    if not textures:
       logging.warning("No texture for %s, skip it", input)
       return 
    
    logging.debug("Looping over textures")
    for item in textures:
        logging.debug(" loop: %s", item)
        filename, file_extension = os.path.splitext(item)
        print("ext", file_extension)
        img = Image.open(item, "r")
        if item.endswith(basefile.replace("json","png")):
            offset = (0, 0)
        if item.endswith("front.png"):
            offset = (0, 0)
        if item.endswith("rear.png"):
            offset = (0, offsetY)
        if item.endswith("top.png"):
            offset = (0, 4 * offsetY)
        if item.endswith("bottom.png"):
            offset = (0, 5 * offsetY)
        if item.endswith("left.png"):
            offset = (0, 3 * offsetY)
        if item.endswith("right.png"):
            offset = (0, 2 * offsetY)
        logging.info("Image %s size is %s", item, (img.size))
        new_img = img.resize(new_size)
        background.paste(new_img, offset)
 
    background.save(image_background)
    logging.info("Background image saved %s ", image_background)
    normal.generate_definitive_normal(image_background, image_normalmap, 0.5, 1)
    logging.info("Normal map generated... %s ", image_normalmap)

    logging.info("Starting Blender from: %s", blender_dir)
    os.system(args['blender'] + " --background --python " + os.path.dirname(__file__) + "/blr_main.py -- " + input + " " + args['outdir'])
    logging.info("Ended texture generation and application!")

#
# Main Script
# 
parser = argparse.ArgumentParser(description='Create a mesh for OGrEE 3D.')

parser.add_argument('--mode',
                        choices=['file', 'dir'],
                        help="""Specify if we use a single file or an directory as input""",
                        required=True)

parser.add_argument('--path',
                        help="""Specify the path of the input""",
                        required=True)

parser.add_argument('-o', '--outdir', default=os.path.dirname(__file__) + "/outputs", type=str, help='Folder base for creating mesh', required=True)
parser.add_argument('-r', '--resolution', default=512, type=int, help='Texture resolution', required=False)
parser.add_argument('-b', '--blender', type=str, help='Blender path', required=True)
parser.add_argument('--verbose',
                        choices=["INFO", "WARNING", "ERROR", "DEBUG"],
                        help="""Specify the verbose level""",
                        default="DEBUG")

args = vars(parser.parse_args())

blender_dir = os.path.dirname(args['blender'])
logging.basicConfig(format="[%(levelname)s][%(asctime)s]: %(message)s", level=args['verbose'].upper())

logging.info("Creating empty background from resolution parameter")  

new_size = args['resolution'] , args['resolution'] // 6

if args['mode'] == 'file':
    logging.info("Processing JSON in file mode : %s",args['path'])
    create_total_mesh(os.path.abspath(args['path']))

if args['mode'] == 'dir':
     for json in glob.glob(args['path'] + '/*.json'):
         logging.info("Processing JSON in dir mode %s", json)
         create_total_mesh(os.path.abspath(json))

    

