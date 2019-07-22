import numpy as np
import math, sys, random, argparse

from PIL import Image, ImageEnhance
gscale = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "


def convert_to_ascii(imgpath, cols):
    global gscale
    image = Image.open(imgpath).convert("L")

    
    W, H = image.size[0], image.size[1]
    w = W/cols
    h = w/0.43
    rows = int(H/h)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)

    aimg = []
    min_val, max_val = get_val_bounds(image)
    brightness_range = 255 - min_val - (256 - max_val)


    for row in range(rows):
        y1 = int (row*h)
        y2 = int ((row+1)*h)

        if row == rows-1:
            y2 = H
        
        aimg.append('')
        for i in range(cols):
            x1 = int (i*w)
            x2 = int((i+1)*w)

            if i == cols-1:
                x2 = W
            
            img = image.crop((x1, y1, x2, y2))
            avg = int(getAverageBrightness(img)) - min_val 
            gsval = gscale[int((avg*(len(gscale) -1))/ brightness_range)]

            aimg[row] += gsval

    return aimg

def getAverageBrightness(image):
    im = np.array(image)
    w,h = im.shape
    # reshape the array to one dimension, so that we can take the average.
    return np.average(im.reshape(w*h))


def get_val_bounds(image):
    im = np.array(image)
    w,h = im.shape
    arr = im.reshape(w*h)    
    return np.amin(arr), np.amax(arr)


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


