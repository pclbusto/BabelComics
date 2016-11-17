import urllib.request
from PIL import Image
#import os, sys
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import os

def convertAndDownload(url,path):
    # url = "http://static4.comicvine.com/uploads/original/1/19151/412843-dkhlogo.gif"
    file_name = url.split('/')[-1]
    file_name_no_ext = (file_name[:-4])
    print(url)
    u = urllib.request.urlopen(url)
    if os.path.exists(path+file_name_no_ext + ".jpg"):
        return path + file_name_no_ext + ".jpg"
    f = open(path+file_name, 'wb')
    meta = u.info()
    outfile = file_name_no_ext + ".jpg"
    while True:
        buffer = u.read()
        if not buffer:
            break
        if file_name != outfile:
            try:
                f.write(buffer)
                f.close()
                gif = Image.open(path+file_name)
                new_im = Image.new("RGBA", gif.size, (255, 255, 255))
                new_im.paste(gif)
                new_im.save(path + outfile, 'jpeg')
                os.remove(path+file_name)
            except IOError as err:
                print(err)
                print("cannot convert", file_name)
        else:
            f.write(buffer)

    f.close()
    return path + outfile

if __name__ == "__main__":
    convertAndDownload("http://comicvine.gamespot.com/api/image/scale_large/1272643-marvel_music.jpg", "publishers\\temp\\")
