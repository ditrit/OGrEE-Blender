# OGrEE-Blender

OgreeXporter is a custom converter from JSON to FBX.

## Requierements
+ Windows **or** Linux
+ Blender **>2.8** (version must be superior to 2.8, 2.9.3 LTS is supported and correct)
+ **FBX viewer** (or Blender >> Files/Import/Fbx), to check models

## Installation Guide

Go to this folder and make:

```sh
pip install -r requirements.txt 
```
After that, you'll be able to make, to see help:

```sh
python main.py -h
```

``-i``: (Input) root path to search JSON models.  

if arg is a directory, loops on each JSON found recursively from this dir
if arg is a JSON file, only render this file

``-o``: (Output) output directory / optional 
- if not specified, FBX are rendered into `./outputs`
- Output names are based on input JSONs.

``-r``: (Resolution) Allows to set specific resolution for the model.

``-b``: (Blender path)  full path of blender binary

- not optional

