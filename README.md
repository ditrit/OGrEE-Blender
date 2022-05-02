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

## How does it works?

[![Image](https://i.goopics.net/ci3ola.png)](https://goopics.net/i/ci3ola)

This tool is working within Blender (in background mode) and Python 3.

### On Linux

Set full path, also in Blender path.

### On Windows
Set shortpath for Blender path.

**Example:** 
``PROGRA~1/BLENDE~1/BLENDE~1.0/BLENDE~1.EXE``