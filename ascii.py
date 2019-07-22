import numpy as np
import math, sys, random, argparse

from PIL import Image, ImageEnhance
gscale = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "


def convert_to_ascii(imgpath, cols):
    global gscale
    image = Image.open(imgpath).convert("L")
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)
    
    W, H = image.size[0], image.size[1]
    w = W/cols
    h = w/0.43
    rows = int(H/h)
    
    aimg = []

    for j in range(rows):
        y1 = int (j*h)
        y2 = int ((j+1)*h)

        if j == rows-1:
            y2 = H
        
        aimg.append('')
        for i in range(cols):
            x1 = int (i*w)
            x2 = int((i+1)*w)

            if i == cols-1:
                x2 = W
            
            img = image.crop((x1, y1, x2, y2))
            avg = int(getAverageBrightness(img))
            gsval = gscale[int((avg*69)/255)]

            aimg[j] += gsval

    return aimg

def getAverageBrightness(image):
    im = np.array(image)
    w,h = im.shape
    # reshape the array to one dimension, so that we can take the average.
    return np.average(im.reshape(w*h))


def main(): 
    # create parser 
    descStr = "Generate ascii art string from image"
    parser = argparse.ArgumentParser(description=descStr) 
    # add expected arguments 
    parser.add_argument('--file', dest='input_file', required=True, help='path/to/image/file') 
    parser.add_argument('--out', dest='out_file', required=False, help='path/to/output/file') 
    parser.add_argument('--cols', dest='cols', required=False, help='columns in outut image') 
  
    # parse args 
    args = parser.parse_args() 
    
    input_file = args.input_file 
  
    # set output file 
    out_file = 'out.txt'
    if args.out_file: 
        out_file = args.out_file

    # set cols 
    cols = 80
    if args.cols: 
        cols = int(args.cols) 
  
    # convert image to ascii txt 
    aimg = convert_to_ascii(input_file, cols) 
  
    # open file 
    f = open(out_file, 'w') 
  
    # write to file 
    for row in aimg: 
        f.write(row + '\n') 
  
    # cleanup 
    f.close()

    print("ASCII art written to %s" % out_file) 



if __name__ == "__main__":
    main()


