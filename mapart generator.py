from litemapy import Schematic, Region, BlockState
from PIL import Image;
import nbtlib;
import os;
import json;
import math;

here = os.path.dirname(os.path.abspath(__file__));
f = open(os.path.join(here,"config.txt"),"r");
config = json.loads(f.read());
f.close();

colorKeysFw = {
    "white"      : "255, 255, 255",
    "orange"     : "216, 127, 51",
    "magenta"    : "178, 76, 216",
    "light_blue" : "102, 153, 216",
    "yellow"     : "229, 229, 51",
    "lime"       : "127, 204, 25",
    "pink"       : "242, 127, 165",
    "gray"       : "76, 76, 76",
    "light_gray" : "153, 153, 153",
    "cyan"       : "76, 127, 153",
    "purple"     : "127, 63, 178",
    "blue"       : "51, 76, 178",
    "brown"      : "102, 76, 51",
    "green"      : "102, 127, 51",
    "red"        : "153, 51, 51",
    "black"      : "25, 25, 25"
}

colorKeysRv = {
    "255, 255, 255" : "white",
    "216, 127, 51"  : "orange",
    "178, 76, 216"  : "magenta",
    "102, 153, 216" : "light_blue",
    "229, 229, 51"  : "yellow",
    "127, 204, 25"  : "lime",
    "242, 127, 165" : "pink",
    "76, 76, 76"    : "gray",
    "153, 153, 153" : "light_gray",
    "76, 127, 153"  : "cyan",
    "127, 63, 178"  : "purple",
    "51, 76, 178"   : "blue",
    "102, 76, 51"   : "brown",
    "102, 127, 51"  : "green",
    "153, 51, 51"   : "red",
    "25, 25, 25"    : "black"
}

dith = Image.Dither.NONE
if (config['enable_dither']) : dith = Image.Dither.ORDERED

im = Image.open(os.path.join(here, config['input_filename']));
im = im.convert(mode = "RGB"); #sometimes line 13 will throw an error due to bad mode

palette = Image.open(os.path.join(here, "carpetPalette.png"));
palette = palette.quantize(colors = 256,dither = None);

im = im.resize((128, 128));
im = im.quantize(colors = 16, palette = palette, dither = dith);
im = im.convert(colors = 16, mode = "RGB");
if (config['enable_color_swap']) :
    for x in range(128) :
        for y in range(128) :
            p = im.getpixel((x,y));
            if (p == (0, 0, 0)) : p = (25, 25, 25)
            rgb = tuple([int(x) for x in colorKeysFw[config['color_swaps'][colorKeysRv[f"{p[0]}, {p[1]}, {p[2]}"]]].split(", ")]);
            im.putpixel((x,y), rgb);
            #i couldnt think of a better way sorry
im.save(os.path.join(here,config['output_png_filename']));

colorDict = {
    "255, 255, 255" : BlockState(blockid = "minecraft:white_carpet"),
    "216, 127, 51"  : BlockState(blockid = "minecraft:orange_carpet"),
    "178, 76, 216"  : BlockState(blockid = "minecraft:magenta_carpet"),
    "102, 153, 216" : BlockState(blockid = "minecraft:light_blue_carpet"),
    "229, 229, 51"  : BlockState(blockid = "minecraft:yellow_carpet"),
    "127, 204, 25"  : BlockState(blockid = "minecraft:lime_carpet"),
    "242, 127, 165" : BlockState(blockid = "minecraft:pink_carpet"),
    "76, 76, 76"    : BlockState(blockid = "minecraft:gray_carpet"),
    "153, 153, 153" : BlockState(blockid = "minecraft:light_gray_carpet"),
    "76, 127, 153"  : BlockState(blockid = "minecraft:cyan_carpet"),
    "127, 63, 178"  : BlockState(blockid = "minecraft:purple_carpet"),
    "51, 76, 178"   : BlockState(blockid = "minecraft:blue_carpet"),
    "102, 76, 51"   : BlockState(blockid = "minecraft:brown_carpet"),
    "102, 127, 51"  : BlockState(blockid = "minecraft:green_carpet"),
    "153, 51, 51"   : BlockState(blockid = "minecraft:red_carpet"),
    "25, 25, 25"    : BlockState(blockid = "minecraft:black_carpet")
}

if (config['enable_schem_generation']):
    reg = Region(0, 0, 0, 128, 2, 128);
    schem = reg.as_schematic(name = config['output_schematic_name'], author = config['schematic_author'], description = config['schematic_description']);

    for x in range(128):
        for y in range(128):
            reg.setblock(x,0,y, BlockState(blockid = "minecraft:deepslate"));
            
    for x in range(128):
        for y in range(128):
            rgb = im.getpixel((x, y))
            lookup = f"{str(rgb[0])}, {str(rgb[1])}, {str(rgb[2])}";
            if (lookup not in colorDict) : col = colorDict[colorKeysFw[config['error_color']]]; #set to error color if weird rgb
            if (lookup == "0, 0, 0") : col = colorDict["25, 25, 25"];
            else : col = colorDict[lookup];
            reg.setblock(x,1,y, col);
     
    schem.save(os.path.join(here,f"{config['output_schematic_name']}.litematica"));



