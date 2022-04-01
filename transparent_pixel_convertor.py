from PIL import Image

imFile = "logo.png"
im = Image.open(imFile, 'r')

imageSizeW, imageSizeH = im.size

for i in range(1, imageSizeW):
    for j in range(1, imageSizeH):
        pixVal = im.getpixel((i, j))
        if 0 < pixVal[3] < 255:
            im.putpixel((i, j), (pixVal[0], pixVal[1], pixVal[2], 255))

im.save('logo_no_alpha.png')
