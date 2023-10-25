# Minecraft-Mapart-Generator
Creates Litematica schematics for useage in minecraft mapart (dependencies included)

# Config
- 'input_filename' and 'output_png_filename' must include an image suffix
- 'output_schematic_name' doesnt need a suffix
- 'color_swaps' contains a dict of what colors will swap to after the initial image is reduced, dithered, and generated. For instance, setting `"white" : "grey"` will set white carpets to grey carpets in the final schematic. useful for correcting errors if dithering is not enabled

# Usage
**1)** Make sure input image is within program directory
**2)** Set config options
**3)** run `mapart generator.py` 
**4)** paste output .litematic file into schematics folder in your minecraft directory
