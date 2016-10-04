from tkinter import *
from tkinter import Tk, ttk
from ComicBook import ComicBook
from Series import Series
from Serie import Serie
from SeriesLookup import SeriesLookupGui
from ComicBooks import ComicBooks
from ComicVineSearcher import *
from PIL import Image, ImageTk
import urllib.request
import os
from  BabelComicBookManagerConfig import *


class ComicCatalogerGui(Frame):
    '''muestra un panel con una info de comic resumida
    |------| serie nº /de
    |      | titulo
    |      | arco
    |      | nº arco / de
    |------|
    '''

    def __createPanelComic__(self, parent, comicbook, comicCoverImage, **kw):
        panelComic = ttk.LabelFrame(parent, **kw)
        self.comicCovers.append(ImageTk.PhotoImage(comicCoverImage))
        print(comicbook.getNombreArchivo())
        comicCoverLabel = ttk.Label(panelComic, image=self.comicCovers[len(self.comicCovers) - 1], compound='top')
        comicCoverLabel.grid(column=0, row=0, sticky=(W))
        panelInfo = ttk.LabelFrame(panelComic, text='--')
        panelInfo.grid(column=1, row=0, sticky=(W, E, N))
        series = Series()
        serie = series.get(comicbook.serieId)
        if (series.status == 0):
            print('No se pudo recueperar la serie')
            nombreSerie = ttk.Label(panelInfo, text='Serie: ' + "")
            numerode = ttk.Label(panelInfo, text='Número: ' + str(comicbook.numero) + ' de ' + str(0))
        else:
            nombreSerie = ttk.Label(panelInfo, text='Serie: ' + serie.nombre)
            numerode = ttk.Label(panelInfo,text='Número: ' + str(comicbook.numero) + ' de ' + str(serie.cantidadNumeros))
        archivo = ttk.Label(panelInfo, text='Archivo: ' + comicbook.getNombreArchivo())
        tituloEjemplar = ttk.Label(panelInfo, text='Título: ' + comicbook.titulo)

        arcoAlternativo = ttk.Label(panelInfo, text='Fecha Tapa: ' + comicbook.fechaTapa)
        archivo.grid(sticky=(W), padx=5)
        nombreSerie.grid(sticky=(W), padx=5)
        tituloEjemplar.grid(sticky=(W), padx=5)
        numerode.grid(sticky=(W), padx=5)
        arcoAlternativo.grid(sticky=(W), padx=5)
        return panelComic

    def openSerieLookup(self):
        window = Toplevel()
        serieRetorno = Serie(1880, '')
        lk = SeriesLookupGui(window, serieRetorno)
        lk.grid(sticky=(E, W, S, N))
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        window.geometry("+0+0")
        window.wm_title(string="Series")
        self.wait_window(window)
        serieRetorno = lk.getSerie()
        self.entrySerie.set(serieRetorno.id)

    def __init__(self, parent, comicbook, *cnf, **kw):
        Frame.__init__(self, parent, *cnf, **kw)
        self.rowconfigure(0, weight=1)
        self.parent = parent
        self.rowconfigure(1, weight=1)
        self.comicCovers = []
        # representa lo que vamos a catalogar. tomando como fuente de datos ComicVine
        self.comicbook = comicbook

        self.comicbook.openCbFile()
        self.comicbook.goto(0)
        self.size = (160, 248)
        self.panelSourceComic = self.__createPanelComic__(self, comicbook,
                                                          self.comicbook.getImagePage().resize(self.size),
                                                          text='Comic info')
        self.panelSourceComic.grid(sticky=(N, W, S, E))
        ##Panel opciones busqueda

        self.panelBusqueda = LabelFrame(self)
        self.panelBusqueda.grid(column=1, row=0, sticky=(N, W, S, E))
        self.entryTitulo = StringVar()
        self.entrySerie = StringVar()
        self.spinNumero = IntVar()
        self.spinAnio = IntVar()

        self.seriesLookupFrame = ttk.Frame(self.panelBusqueda)
        self.seriesLookupFrame.grid(column=1, row=0, sticky=(W), pady=5)
        ttk.Label(self.panelBusqueda, text='Serie: ').grid(column=0, row=0, sticky=(W), pady=5)
        self.lookupImage = PhotoImage(file='Magnifying-Glass-icon.png')

        ttk.Label(self.panelBusqueda, text='Título: ').grid(column=2, row=0, sticky=(W), pady=5)
        ttk.Entry(self.panelBusqueda, textvariable=self.entryTitulo).grid(column=3, row=0, sticky=(W), pady=5)

        ttk.Button(self.seriesLookupFrame, image=self.lookupImage, command=self.openSerieLookup).grid(column=1, row=0,
                                                                                                      sticky=(N, S),
                                                                                                      pady=5)

        ttk.Entry(self.seriesLookupFrame, textvariable=self.entrySerie).grid(column=0, row=0, sticky=(W), pady=5)
        ttk.Label(self.panelBusqueda, text='Número: ').grid(column=4, row=0, sticky=(W), pady=5)
        Spinbox(self.panelBusqueda, textvariable=self.spinNumero, from_=0, to=9999).grid(column=5, row=0, sticky=(W),
                                                                                         pady=5)

        botonBuscar = ttk.Button(self.panelBusqueda, text='Buscar ejemplar', command=self.buscarSerie)
        botonBuscar.grid(column=6, row=0, pady=5, columnspan=6)

        ##config grilla comics
        self.grillaComics = ttk.Treeview(self.panelBusqueda,
                                         columns=('fecha', 'titulo', 'descripcion', 'idExterno', 'numero',
                                                  'api_detail_url', 'thumb_url', 'volumeName', 'volumeId'),
                                         displaycolumns=('titulo', 'numero', 'volumeName'))

        self.grillaComics.heading('titulo', text='Título')
        self.grillaComics.heading('fecha', text='Fecha Cover')
        self.grillaComics.heading('descripcion', text='Descripcion')
        self.grillaComics.heading('idExterno', text='Id Vine')
        self.grillaComics.heading('numero', text='Número')
        self.grillaComics.heading('api_detail_url', text='api_detail_url')
        self.grillaComics.heading('thumb_url', text='thumb_url')
        self.grillaComics.heading('volumeName', text='Serie')
        self.grillaComics.heading('volumeId', text='SserieID')

        self.grillaComics.config(show='headings')  # tree, headings
        self.grillaComics.grid(column=0, row=1, columnspan=10, sticky=(N, E, S, W))
        self.grillaComics.bind('<<TreeviewSelect>>', self.itemClicked)  # the item clicked can be found via tree.focus()
        # boton copiar datos
        ttk.Button(self, text='copiar info', command=self.copiarInfo).grid(column=0, row=1)
        print('------------------------------------')

    def copiarInfo(self):
        cnf = BabelComicBookManagerConfig()
        print('clave: ' + cnf.getClave())
        cv = ComicVineSearcher(cnf.getClave())
        cv.setEntidad('issue')
        completComicInfo = cv.getVineEntity(self.comicBookVine.idExterno)
        completComicInfo.path = self.comicbook.path
        # como lo que traje de vine tiene toda la data directamente actualizo la base de datos
        ComicBooks().update(completComicInfo)
        self.parent.destroy()

    def itemClicked(self, event):
        if (self.grillaComics.selection):

            item = self.grillaComics.item(self.grillaComics.selection())
            webImage = item['values'][6]
            nombreImagen = item['values'][6][item['values'][6].rindex('/') + 1:]

            if not (os.path.isfile('searchCache\\' + nombreImagen)):
                print('no existe')
                print(nombreImagen)
                jpg = urllib.request.urlopen(webImage)
                jpgImage = jpg.read()
                fImage = open('searchCache\\' + nombreImagen, 'wb')
                fImage.write(jpgImage)
                fImage.close()
            fImage = open('searchCache\\' + nombreImagen, 'rb')
            im = Image.open(fImage)

        # print(item['values'][8],item['values'][4])
        self.comicBookVine = ComicBook('Path', str(item['values'][1]), item['values'][8], item['values'][4])
        self.comicBookVine.fechaTapa = item['values'][0]
        self.comicBookVine.resumen = item['values'][2]
        self.comicBookVine.idExterno = item['values'][3]

        self.panelVineComic = self.__createPanelComic__(self, self.comicBookVine, im.resize(self.size),
                                                        text='Vine Info')
        self.panelVineComic.grid(column=0, row=2, sticky=(N, S, E, W))

    def buscarSerie(self):
        # recuperarla de la configuracion
        config = BabelComicBookManagerConfig()


        buscador = ComicVineSearcher(config.getClave("issues"))

        buscador.setEntidad('issues')
        if (self.entrySerie.get()):
            buscador.addFilter('volume:' + self.entrySerie.get())
        if (self.entryTitulo.get()):
            buscador.addFilter('name:' + self.entryTitulo.get())
        if (str(self.spinNumero.get()) != '0'):
            buscador.addFilter('issue_number:' + str(self.spinNumero.get()))

        buscador.vineSearch()
        for item in self.grillaComics.get_children():
            self.grillaComics.delete(item)
        for issue in buscador.listaBusquedaVine:
            self.grillaComics.insert('', 0, '', values=(issue['fecha'],
                                                        issue['titulo'],
                                                        issue['descripcion'],
                                                        issue['idExterno'],
                                                        issue['numero'],
                                                        issue['api_detail_url'],
                                                        issue['thumb_url'],
                                                        issue['volumeName'],
                                                        issue['volumeId']
                                                        ))


##        lista = []
##        lista.append({'count_of_issues':15,'description':'description','Id':'Id000015','image':'https://cdn1.iconfinder.com/data/icons/UltraBuuf/512/capo.png','name':'Batman','publisher':'DC-publisher','start_year':1970})
##        lista.append({'count_of_issues':1,'description':'description','Id':'Id000017','image':'https://cdn1.iconfinder.com/data/icons/UltraBuuf/512/Hellboy.png','name':'The Flash','publisher':'DC-publisher','start_year':1990})
##        lista.append({'count_of_issues':135,'description':'description','Id':'Id000005','image':'https://cdn1.iconfinder.com/data/icons/UltraBuuf/512/Magneto.png','name':'X-men','publisher':'Marvel-publisher','start_year':1940})
##        lista.append({'count_of_issues':55,'description':'description','Id':'Id0000978','image':'https://cdn1.iconfinder.com/data/icons/UltraBuuf/512/Lantern.png','name':'Green Lantern','publisher':'DC-publisher','start_year':1956})
##        for comic in lista:
##            self.grillaSeries.insert('', 0, '', text=comic['name'], values=(comic['count_of_issues'],
##                                                                            comic['description'],
##                                                                            comic['Id'],
##                                                                            comic['image'],
##                                                                            comic['name'],
##                                                                            comic['publisher'],
##                                                                            comic['start_year']))
##


##(count_of_issues,description,Id,image,name,publisher,start_year)

if __name__ == '__main__':
    root = Tk()
    comics = ComicBooks()
    comic = comics.get('/home/pedro/Descargas/ftp/DC/2GLR4/Green Lantern_ Rebirth V2004 #1 (2004).cbz')
    cvs = ComicCatalogerGui(root, comic)
    cvs.grid(sticky=(N, W, S, E))
    cvs.grid()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    root.mainloop()
