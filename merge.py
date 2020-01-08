from __future__ import division
import os
import shutil
import glob
import argparse
from fpdf import FPDF
from PIL import Image

ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-s", "--source", required=True,
help="Source directory")
ap.add_argument("-o", "--output", required=True,
help="Output directory")
ap.add_argument("-n", "--name", required=True,
help="Name of output file")
args = vars(ap.parse_args())

imgdir = args['source']
outdir = args['output']
filename = args['name']

if not os.path.exists(outdir):
    os.mkdir(outdir)

DPI = 96
MM_IN_INCH = 25.4
MAX_WIDTH = 6400
MAX_HEIGHT = 3200

pdf = FPDF('P','pt','A4')

basename = '*.*'
imagelist = sorted(glob.glob(os.path.join(imgdir,basename)))
    
for image in imagelist:
    im = Image.open(image)
    imgwidth, imgheight = im.size
    
    widthScale = MAX_WIDTH / imgwidth
    heightScale = MAX_HEIGHT / imgheight
    scale = min(widthScale, heightScale)

    scaledWidth = scale * imgwidth * MM_IN_INCH / DPI
    scaledHeight = scale * imgheight * MM_IN_INCH / DPI

    pdf.add_page()
    pdf.image(image,0,0,scaledWidth,scaledHeight)
pdf.output(os.path.join(outdir, filename), "F")