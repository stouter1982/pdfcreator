import os
import shutil
import glob
import argparse
from PIL import Image

def crop(im,height,width):
    # im = Image.open(infile)
    imgwidth, imgheight = im.size
    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            # print (i,j)
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)

if __name__=='__main__':
    # Construct the argument parser
    ap = argparse.ArgumentParser()

    # Add the arguments to the parser
    ap.add_argument("-s", "--source", required=True,
    help="Source directory")
    ap.add_argument("-o", "--output", required=True,
    help="Output directory")
    args = vars(ap.parse_args())

    # change the path and the base name of the image files 
    imgdir = args['source']
    outdir = args['output']

    if os.path.exists(outdir):
        shutil.rmtree(outdir)
        os.mkdir(outdir)

    basename = '*.*'
    filelist = glob.glob(os.path.join(imgdir,basename))
    for filenum,infile in enumerate(sorted(filelist)):
        print(infile)
        
        im = Image.open(infile)
        imgwidth, imgheight = im.size
        print('Image size is: w %d x h %d ' % (imgwidth, imgheight))
        height = imgheight
        width =  imgwidth/2
        start_num = 0
        for k,piece in enumerate(crop(im,height,width),start_num):
            # print k
            # print piece
            img=Image.new('L', (width,height), 255)
            # print img
            img.paste(piece)
            path = os.path.join(outdir, "temp%d_1%05d.png" % (filenum,int(k+1)))
            print(path)
            img.save(path)
            #os.rename(path,os.path.join("temp%d.1%05d" % (int(k+1),filenum)))