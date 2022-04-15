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

``-in``: (Input) Only set the name of the model, not the entier path. Absolute path is coming soon.

``-out``: (Output) Do not works yet. Will allow to set the output path.

``-r``: (Resolution) Allows to set specific resolution for the model.

``-b``: (Blender path) Allows to set specific path to use to start Blender.

