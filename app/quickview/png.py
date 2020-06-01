from PIL import Image

def ToPng8(directory,pngName):
    im = Image.open(directory+"\\"+pngName+".png")

    # PIL complains if you don't load explicitly


    # Get the alpha band
    alpha = im.split()[-1]

    im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=8)
    pix = im.load()
    print(pix[90,180])

    # Set all pixel values below 128 to 255,
    # and the rest to 0
    #mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    #mask = Image.eval(alpha, lambda a: int(a/16)*16)
    mask = Image.eval(alpha, lambda a: 255 if a>=255 else 0)

    # Paste the color of index 255 and use alpha as a mask
    im.paste(255, mask)

    # The transparency index is 255
    im.save(directory+"\\"+pngName+"_8.png", transparency=255)

def ToWebp(directory,pngName):
    im = Image.open(directory + "\\" + pngName + ".png")
    im.save(directory + "\\" + pngName + ".webp", "WEBP", transparency=255)



#ToPng8(r"C:\inetpub\wwwroot\test\picturelayer","bigphoto1")