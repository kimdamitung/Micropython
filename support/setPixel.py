#!/usr/bin/env python

# vim: set ai et ts=4 sw=4:

from PIL import Image
import sys
import os

if len(sys.argv) < 2:
    print("Usage: {} <image-file> <output-file>".format(sys.argv[0]))
    sys.exit(1)

fname = sys.argv[1]
output_file = sys.argv[2] if len(sys.argv) > 2 else "src/package/__init__.py"

img = Image.open(fname)
img = img.convert('RGB')

if img.width != 128 or img.height != 160:
    print("Error: 128x160 image expected")
    sys.exit(2)

with open(output_file, 'w') as f:
    f.write("data = [\n")
    for y in range(0, img.height):
        s = "\t["
        for x in range(0, img.width):
            (r, g, b) = img.getpixel((x, y))
            color565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | ((b & 0xF8) >> 3)
            s += "0x{:04X}".format(color565)
            if x < img.width - 1:
                s += "," 
        s += "]"
        if y < img.height - 1:
            s += "," 
        f.write(s + "\n")
    f.write("]\n")

print(f"Data written to {output_file}")
