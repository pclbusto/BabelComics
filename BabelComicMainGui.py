from ComicBookGui import ComicBookGui
from ComicBooks import ComicBooks
from ComicVineSearcherGui import ComicCatalogerGui
from BabelComicConfigGui import *
from BabelComicsVisor import BabelComicVisor
from BabelComicScannerGui import BabelComicScannerGui
from PanelThumbnailComics import PanelThumbnailComics
import threading

class BabelComicMainGui():
    def __init__(self):
        print("")

def CheckThumbnailsGeneration():
    while panelComics.threadLoadAndCreateThumbnails.isAlive():
        if panelComics.cantidadThumnailsAGenerar>0:
            statusBar.set('Porcentaje de carga de thumnails: {1:.2f} Cantidad de Registros: {0:}'.format(comics.cantidadRegistrosConsulta,100*(panelComics.cantidadThumnailsGenerados/panelComics.cantidadThumnailsAGenerar)))

    print('generados {} totales {} porcentaje: '.format(panelComics.cantidadThumnailsGenerados, panelComics.cantidadThumnailsAGenerar))
                                                              #,100 * (panelComics.cantidadThumnailsGenerados / panelComics.cantidadThumnailsAGenerar)))
    statusBar.set('Porcentaje de carga de thumnails: {1:.2f} Cantidad de Registros: {0:}'.format(
        comics.cantidadRegistrosConsulta,
        100 * (panelComics.cantidadThumnailsGenerados / panelComics.cantidadThumnailsAGenerar)))
def statusThumbnails():

    threadCheckThumbnailsGeneration = threading.Thread(target=CheckThumbnailsGeneration)
    threadCheckThumbnailsGeneration.start()

def buscar(statusBar):
    busqueda = buscarEntry.get()
    if not busqueda:
        busqueda='%%'
        buscarEntry.insert(0,busqueda)
    panelComics.loadComics(comics.list((busqueda,),'path like ?'))

    statusThumbnails()
    statusBar.set('Cantidad de Registros: {} / {}'.format(comics.cantidadComicsPorPagina,comics.cantidadRegistrosConsulta))



def enterEventEntryBuscar(self):
    buscar(statusBar)


def openComicEditor():
    if (panelComics.comicActual):
        #comic = panelComics.getComicActual()
        comic = comics.get(panelComics.getComicActual().path)
        ventana = Toplevel()
        frameComic = ComicBookGui(ventana, comic)
        frameComic.grid()
##        frameComic.grid(padx=5, pady=5, sticky=(N, W, E, S))
##        frameComic.columnconfigure(0, weight=1)
##        frameComic.rowconfigure(0, weight=1)


def openBabelComicConfig(event):
    window = Toplevel(root)
    window.title('Babel Comics Configuración')
    config = BabelComicConfigGui(window)
    config.grid(sticky=(N, S, W, E))
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    window.grid()

def openBabelComicVisor():
    if (panelComics.comicActual):
        comic = panelComics.getComicActual()
        visor = BabelComicVisor(root, comic,height = root.winfo_screenheight(),width = root.winfo_screenwidth())
        visor.title = ('Babel Comics Visor')
        visor.wm_state('zoomed')
def openComicVine():
    if (panelComics.comicActual):
        window = Toplevel()
        window.title('Catalogador')
        window.geometry('+0+0')
        comics = ComicBooks()
        comic = panelComics.getComicActual()
        cvs = ComicCatalogerGui(window, comic)
        #cvs.grid(sticky=(N, W, S, E))
        cvs.grid()
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        root.wait_window(window)
def sortby():
    grillaSeries.heading('start_year', command=lambda col='AnioInicio': self.sortby(col))
    if desc:
        self.buscarSerie('order by ' + col + ' desc')
def openBabelComicScanner(event):
    scanner = BabelComicScannerGui(root)

def scrollupMouse(event):
    panelComics.yview_scroll(-1 * (int)(event.delta / 120), "units")

def scrollupKeyboard(event):
    print(event.keycode)
    if (event.keycode == 116) | (event.keycode == 117) | (event.keycode == 34)| (event.keycode == 40):
        panelComics.yview_scroll(1, "units")
        print('para abajo')
    if (event.keycode == 112) | (event.keycode == 111) | (event.keycode == 33)| (event.keycode == 38):
        panelComics.yview_scroll(-1, "units")
        print('para abajo')
    #el 114 es en linux y el 39 en windows
    if (event.keycode==114)|(event.keycode==39):#derecha
        panelComics.nextComic()
    # el 113 es en linux y el 37 en windows
    if (event.keycode == 113)|(event.keycode==37):  # izquierda
        panelComics.prevComic()

def on_resize(event):
    #solo refrescar cuando el tamañio sume o reste columnas
    #if cantidadColumnas!=int(event.width/(panelComics.size[0] + panelComics.space)):
    panelComics.cantidadColumnas = int(event.width/(panelComics.size[0] + panelComics.space))
    #panelComics.loadComics(comics.listaConsulta)
    #print(event.width/(panelComics.size[0] + panelComics.space))

def refrescar():
    #solo refrescar cuando el tamañio sume o reste columnas
    #if cantidadColumnas!=int(event.width/(panelComics.size[0] + panelComics.space)):
    panelComics.loadComics(comics.listaConsulta)
    #print(event.width/(panelComics.size[0] + panelComics.space))

def popupListas(event):
    # display the popup menu
    try:
        popup.tk_popup(event.x_root, event.y_root, 0)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        popup.grab_release()

def popupPanelThumbnails(event):
    try:
        popupThumbnails.tk_popup(event.x_root, event.y_root, 0)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        popupThumbnails.grab_release()
def selectVista(event):
    print(treeListas.selection())
    comics.vistaConsultas = treeListas.selection()[0]

def primero():
    comics.goto(0)
    panelComics.loadComics(comics.listaConsulta)
    statusThumbnails()

def siguiente():
    comics.goto(comics.paginaActual+1)
    panelComics.loadComics(comics.listaConsulta)
    statusThumbnails()
def anterior():
    comics.goto(comics.paginaActual-1)
    panelComics.loadComics(comics.listaConsulta)
    statusThumbnails()
def ultimo():
    comics.goto(comics.getCantidadPaginas())
    panelComics.loadComics(comics.listaConsulta)
    statusThumbnails()
if __name__ == "__main__":
    ##    babel = BabelComicMainGui()
    root = Tk()
    #root.wm_state('zoomed')
    root.title('Babel Comic Manager GitHub')
    barraHerramientas = Frame(root)
    barraHerramientas.grid(column=0, row=0, sticky=(E, W))
    barraHerramientas.config()
    barraHerramientas.columnconfigure(0, weight=1)
    barraHerramientas.rowconfigure(1, weight=1)

    #opciones de barra de tareas
    buscarEntry = ttk.Entry(barraHerramientas)
    image = PhotoImage(file='Magnifying-Glass-icon.png')
    buscarBoton = ttk.Button(barraHerramientas,width=1,compound=CENTER, image=image, command = lambda :buscar(statusBar))
    buscarEntry.grid(column=5, row=0, sticky=E)
    buscarBoton.grid(column=6, row=0, sticky=E)
    buscarEntry.bind('<Return>', enterEventEntryBuscar)

    ttk.Button(barraHerramientas,text='refrescar', command = refrescar).grid(column=4, row=0, sticky=E)
    ttk.Button(barraHerramientas, text='<<', command=primero).grid(column=0, row=0, sticky=E)
    ttk.Button(barraHerramientas, text='<', command=anterior).grid(column=1, row=0, sticky=E)
    ttk.Button(barraHerramientas, text='>', command=siguiente).grid(column=2, row=0, sticky=E)
    ttk.Button(barraHerramientas, text='>>', command=ultimo).grid(column=3, row=0, sticky=E)

    panedWindow = ttk.Panedwindow(root, orient=HORIZONTAL)
    panedWindow.grid(column=0, row=1, sticky=(E, W, S, N))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    #arbol donde tenenmos las listas de comics.
    treeListas = ttk.Treeview(panedWindow)
    treeListas.grid()
    biblioteca =''
    biblioteca = treeListas.insert('',0, 'Biblioteca', text='Biblioteca')
    treeListas.insert(biblioteca, 'end', 'BlackestNight', text='La noche mas oscura')

    #creamos menu popup para agregar vistas
    popup = Menu(treeListas, tearoff=0)
    popup.add_command(label="Agregar Lista")  # , command=next) etc...
    treeListas.bind("<Button-3>", popupListas)

    treeListas.bind("<<TreeviewSelect>>", selectVista)


    panelGrillaComics = Frame(panedWindow)
    panelGrillaComics.columnconfigure(0,weight=1)
    panelGrillaComics.rowconfigure(0, weight=1)
    panelGrillaComics.grid(sticky=(N,S,W,E))

    scrollbar = ttk.Scrollbar(panelGrillaComics)
    scrollbar.grid(column=1, row=0,sticky=(S,N))

    panelComics = PanelThumbnailComics(panelGrillaComics,yscrollcommand=scrollbar.set)
    panelComics.bind("<Configure>", on_resize)

    '''treeComics = ttk.Treeview(panelGrillaComics, columns=('serie', 'nombre', 'numero', 'archivo', 'path'),yscrollcommand = scrollbar.set,
                              displaycolumns=('serie', 'nombre', 'numero', 'archivo'))'''

    scrollbar.config(command=panelComics.yview)
    #    treeComics.grid()
    panelComics.bind('<MouseWheel>', scrollupMouse)
    root.bind('<Down>', scrollupKeyboard)
    root.bind('<Key>', scrollupKeyboard)

    # creamos menu popup para abrir el catalogador el visor el editor de info y calcular el thumnails de nuevo
    popupThumbnails = Menu(panelComics, tearoff=0)
    popupThumbnails.add_command(label="Info comic",command=openComicEditor)  # , command=next) etc...
    popupThumbnails.add_command(label="Leer comic",command=openBabelComicVisor)  # , command=next) etc...
    popupThumbnails.add_command(label="Catalogar comic",command = openComicVine)  # , command=next) etc...
    popupThumbnails.add_separator()
    popupThumbnails.add_command(label="Refresh Thumbnail", command = panelComics.recreateThumbnails)  # , command=next) etc...
    panelComics.bind("<Button-3>", popupPanelThumbnails)
    # popup.add_separator()
    # popup.add_command(label="Home")



    #treeComics.heading('serie', text='Serie',command=lambda col='serie': sortby(col))
    #treeComics.heading('numero', text='Número',command=lambda col='numero': sortby(col))
    #treeComics.heading('archivo', text='Archivo',command=lambda col='archivo': sortby(col))
    #treeComics.heading('nombre', text='Nombre', command=lambda col='nombre': sortby(col))
    #treeComics.config(show='headings')  # tree, headings

    root.bind('<Control-c>', lambda x: openComicEditor())
    root.bind('<Control-v>', lambda x: openComicVine())
    root.bind('<Control-b>', lambda x: openBabelComicVisor())

    root.bind('<Control-s>', openBabelComicConfig)
    root.bind('<Control-x>', openBabelComicScanner)

    statusBar = StringVar()
    ttk.Label(root,textvariable=statusBar,anchor="e",relief='groove').grid(column=0,row=3,sticky=(W,E))

    panelComics.grid(column=0,row=0,sticky=(N,S,W,E))
    panedWindow.add(treeListas)
    panedWindow.add(panelGrillaComics)

    #menu
    comics = ComicBooks()
    buscar(statusBar)
    cantidadColumnas = 4
    #variables globales
    desc = False
    root.mainloop()
