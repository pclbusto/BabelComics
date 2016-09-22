from tkinter import *
from tkinter import Tk, ttk
from ComicBooks import ComicBooks
from BabelComicBookManagerConfig import BabelComicBookManagerConfig
from BabelComicsScanner import BabelComicBookScanner
import threading



class BabelComicScannerGui():
    def __init__(self,master=None):
        ventanaPrincipal = Toplevel(master)
        ventanaPrincipal.title('Babel Comics  Scanner')
        panelPrincipal = ttk.Frame(ventanaPrincipal)
        panelBajo = ttk.Frame(ventanaPrincipal)
        panelPrincipal.grid(sticky=(W,E))
        panelBajo.grid()
        panelPrincipal.columnconfigure(0,weight=1)
        self.progresBar = ttk.Progressbar(panelPrincipal)
        self.progresBar.grid(sticky =(W,E),columnspan=2)
        self.progreso = ''
        self.progresBar.setvar(self.progreso)
        ttk.Label(panelPrincipal,text='Procesando archivo: ...').grid()
        ttk.Button(panelBajo,text= 'iniciar',command=self.initScanner).grid(column=1,row=0)
        ttk.Button(panelBajo,text= 'borrar registros de comics',command =  self.borrarComics).grid(column=0,row=0)
    def borrarComics(self):
        comics = ComicBooks()
        comics.rmAll()

    def initScanner(self):
        self.config = BabelComicBookManagerConfig()
        self.manager = BabelComicBookScanner(self.config.listaDirectorios, self.config.listaTipos)
        self.manager.iniciarScaneo()
        t = threading.Thread(target=self.testScanning)
        t.start()

    def testScanning(self):
        while (self.manager.scanerDir.isAlive()):
            self.progresBar['value']  = self.manager.porcentajeCompletado
if __name__ == "__main__":
    ##    babel = BabelComicMainGui()
    root = Tk()
    scanner = BabelComicScannerGui(root)
    root.mainloop()
