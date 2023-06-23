'''
Resize image using python
Reference:
1. https://opensource.com/life/15/2/resize-images-python
'''

from PIL import Image

src_img_path = './image/0.jpg'

img = Image.open(src_img_path)
## specify size
# size = (800, 400)
## scaling by width
basewidth = 300
wpercent = (basewidth / float(img.size[0]))
hsize = int(float(img.size[1]) * float(wpercent))
size = (basewidth, hsize)

## scaling by height
# baseheight = 560
# hpercent = (baseheight / float(img.size[1]))
# wsize = int((float(img.size[0]) * float(hpercent)))
# size = (wsize, baseheight)

img = img.resize(size, Image.ANTIALIAS)

img.save('resized_image1.jpg')

