from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import *
from kivy.uix.button import Label
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage, Image

from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from threading import Thread
from KivyComicBook import *
from KivyComicBooks import *
from kivy.core.window import Window
from KivyComicViewer import KivyVisor
import Series

from BabelComicBookManagerConfig import *
from kivy.uix.listview import ListView

class KivySmallSerieGui(GridLayout):
    def __init__(self,serie, **kwargs):
        super(KivySmallSerieGui, self).__init__(**kwargs)
        self.serie = serie
        self.size_hint = (None, None)
        self.size = (160, 320)
        if serie.hasLocalCover():
            self.cover = Image(source=serie.getCoverLocalPath(), size_hint=(None, None), size=(140, 140))
            self.add_widget(self.cover)
        elif serie.image_url:
            jpg = Stuff.convertAndDownload(serie.image_url,
                                           BabelComicBookManagerConfig().getSerieTempCoverPath())
            self.cover = Image(source=jpg, size_hint=(None, None), size=(140, 140))
            self.add_widget(self.cover)

        self.cols = 1
        self.panelLabel = GridLayout(cols=2,size_hint=(1,0.7))
        self.check = CheckBox(size_hint=(None, 1), size=(30, 30))
        self.check.bind(active=self.activeEvnt)
        self.panelLabel.add_widget(self.check)
        self.label = Label(text=serie.nombre, text_size=(100, None))
        self.label.size_hint_y=1
        if Publishers().get(serie.publisherId):
            self.labelEditorial = Label(text=Publishers().get(serie.publisherId).name, text_size=(100, None))
        else:
            self.labelEditorial = Label(text=serie.publisherId, text_size=(100, None))
        self.labelNumeros = Label(text=serie.cantidadNumeros)
        self.panelLabel.add_widget(self.label)
        self.add_widget(self.panelLabel)
        self.add_widget(self.labelEditorial)
        self.add_widget(self.labelNumeros)
    def activeEvnt(self,obj,evnt):
        if self.check.active:
            if not Series.Series().get(self.serie.id):
                Series.Series().add(self.serie)
        else:
            Series.Series().rm(self.serie.id)

    def showOptions(self,obj,evnt):
        # print(obj)
        panel = GridLayout(cols=1)
        panel.add_widget(Button(text="Catalogar usando ComicVine",size_hint_y=None,size=(0,30)))
        panel.add_widget(Button(text="ver info comic",size_hint_y=None,size=(0,30)))
        panel.add_widget(Button(text="Leer Comic",size_hint_y=None,size=(0,30), on_press=self.viewComic))

        self.popup = Popup(title='Opciones',
                           content=panel,
                           size_hint=(.6, None),size=(0,150))
        self.popup.open()
    def viewComic(self,evnt):
        self.popup.dismiss()
        self.popup = KivyVisor(self.comicBook)
        self.popup.open()
    def salir(self):
        self.popup.dismiss()

class KivyAllSeriesGui(Screen):
    BUSCAR_VINE = 1
    BUSCAR_LOCAL = 2
    def __init__(self, series, **kwargs):
        # make sure we aren't overriding any important functionality
        super(KivyAllSeriesGui, self).__init__(**kwargs)
        self.carrusel = Carousel(direction='right')
        self.carrusel.orientation = 'vertical'
        self.carrusel.size_hint = (1, 1)
        self.listaSeries = series
        self.panel = GridLayout(cols=1)
        self.thumbnailWidth=160
        self.thumbnailHeight = 280
        print(Window.size)
        self.cantidadColumnas = int(Window.width/self.thumbnailWidth)
        self.cantidadFilas = int(Window.height/self.thumbnailHeight)
        print(self.cantidadColumnas)
        print(self.cantidadFilas)

        self.searchText = TextInput(text='', multiline=False)
        self.searchText.size_hint = (0.8, None)
        self.searchText.size = (0, 30)

        panelBusqueda = GridLayout(cols=4)
        panelBusqueda.add_widget(self.searchText)

        self.btnVine = Button(text="Vine", size_hint=(0.1, None), size=(0, 30))
        self.btnLocal = Button(text="Local", size_hint=(0.1, None), size=(0, 30))
        self.btnSalir = Button(text="Salir", size_hint=(0.1, None), size=(0, 30))
        panelBusqueda.add_widget(self.btnVine)
        panelBusqueda.add_widget(self.btnLocal)
        panelBusqueda.add_widget(self.btnSalir)

        self.btnVine.bind(on_press=self.evntBtnBuscarVine)
        self.btnLocal.bind(on_press=self.evntBtnBuscarLocal)
        self.btnLocal.bind(on_press=self.evntBtnBuscarSalir)

        panelBusqueda.size_hint_y = None

        self.panel.add_widget(panelBusqueda)

        self.panel.add_widget(self.carrusel)
        self.add_widget(self.panel)

        self.__loadSeries__()
        self.indice = 0

    def evntBtnBuscarSalir(self, evnt):
        pass

    def evntBtnBuscarVine(self,evnt):
        self.__tbuscar__(KivyAllSeriesGui.BUSCAR_VINE)

    def evntBtnBuscarLocal(self, evnt):
        self.__tbuscar__(KivyAllSeriesGui.BUSCAR_LOCAL)


    def __tbuscar__(self,dondeBuscar):
        t = Thread(self.buscar(dondeBuscar))
        t.start()

    def buscar(self,dondeBuscar):
        series = Series.Series()

        if dondeBuscar == KivyAllSeriesGui.BUSCAR_VINE:
            series.searchInComicVine(self.searchText.text)
            self.listaSeries = series.listaComicVineSearch
            self.indice = 0
        elif dondeBuscar == KivyAllSeriesGui.BUSCAR_LOCAL:
            self.listaSeries = series.getList(("%" + self.searchText.text + "%",), "name like ?")
            self.indice = 0
        self.__loadSeries__()

    def __loadSeries__(self):
        self.carrusel.clear_widgets()
        panelx4 = GridLayout(cols=self.cantidadColumnas)
        indice = 0
        for serie in self.listaSeries:
            if not (indice % (self.cantidadColumnas * self.cantidadFilas) == 0):
                print("agregando a panel")
                print(serie.nombre)
                self.panelx4.add_widget(KivySmallSerieGui(serie))
            else:
                print("creando panel y agregando a carusel")
                self.panelx4 = GridLayout(cols=self.cantidadColumnas)
                self.panelx4.add_widget(KivySmallSerieGui(serie))
                self.carrusel.add_widget(self.panelx4)
            indice += 1

class Test(App):
    def build(self):
        series = Series.Series()
        # series.searchInComicVine('Green Arrow')
        # self.listaComics = series.listaComicVineSearch
        carousel = KivyAllSeriesGui([])
        return carousel

if __name__ == "__main__":
    # Window.size=(1920,1080)
    Test().run()