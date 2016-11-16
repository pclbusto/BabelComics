import urllib.request
from PIL import Image
#import os, sys
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def convertAndDownload(url,path):
    # url = "http://static4.comicvine.com/uploads/original/1/19151/412843-dkhlogo.gif"
    file_name = url.split('/')[-1]
    u = urllib.request.urlopen(url)
    f = open(path+file_name, 'wb')
    meta = u.info()
    print("info Foto")
    print(meta)

    #     file_size = int(meta.get("Content-Length"))
    # print("Downloading:{0} Bytes: {1}".format(file_name, file_size))
    # file_size_dl = 0
    block_sz = 8192
    while True:
        # print("leyendo")
        buffer = u.read(block_sz)
        buffer = u.read()
        if not buffer:
            break
        file_name_no_ext = (file_name[:-4])
        outfile =file_name_no_ext + ".jpg"
        if file_name != outfile:
            try:
                gif = Image.open(file_name)
                new_im = Image.new("RGBA", gif.size, (255, 255, 255))
                new_im.paste(gif)
                new_im.save(outfile, 'jpeg')
            except IOError as err:
                print(err)
                print("cannot convert", file_name)
    f.close()
    return outfile