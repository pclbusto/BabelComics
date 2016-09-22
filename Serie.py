from PIL import Image, ImageTk
from tkinter import Tk, ttk
import math
import os
import urllib.request


class Serie():
    def __init__(self, Id, nombre):
        self.id = Id  # idExterno-por cuestiones de como lo tabaja comicVine vamos a hacerlo clave.
        self.nombre = nombre
        self.descripcion = ''
        self.image_url = ''  # la mas grande. Las chicas las hacemos locales.
        self.publisherId = '0'
        self.publisherName = ''
        self.AnioInicio = ''
        self.cantidadNumeros = 0

    def getImageCover(self):
        nombreImagen = self.image_url[self.image_url.rindex('/') + 1:]
        fullPath = 'coverImagesCache' + os.sep + self.image_url[self.image_url.rindex('/') + 1:]
        size = (320, 496)
        if not (os.path.isfile(fullPath)):
            print('no existe')
            jpg = urllib.request.urlopen(self.image_url)
            jpgImage = jpg.read()
            fImage = open(fullPath, 'wb')
            fImage.write(jpgImage)
            fImage.close()
        fImage = open(fullPath, 'rb')
        return (Image.open(fImage))


##        serie.lb = ImageTk.PhotoImage(im.resize(size))
##        root.coverSerie = ttk.Label(root,text='imagenimagenimagen',image=serie.lb).grid(column=1,row=1,rowspan=2)

if (__name__ == '__main__'):
    serie = Serie('79149', 'La Guerra de los Sinestro Corps')
    serie.image_url = 'http://static4.comicvine.com/uploads/scale_large/11120/111202620/4299024-6489227567-1578..jpg'
    root = Tk()

    imagen = serie.getImageCover()
    lb = ImageTk.PhotoImage(imagen)
    coverSerie = ttk.Label(root, text='imagenimagenimagen', image=lb).grid(column=1, row=1, rowspan=2)
    root.grid()
    root.mainloop()


