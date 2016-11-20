from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import *
from kivy.uix.button import Label
from PublishersModule import *
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage, Image
import Stuff
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from MemoryImage import *
from threading import Thread
from KivyComicBook import *
from KivyComicBooks import *
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout


from BabelComicBookManagerConfig import *
from kivy.uix.listview import ListView

class KivySmallComicGui(GridLayout):
    def __init__(self,comicBook, **kwargs):
        super(KivySmallComicGui,self).__init__(**kwargs)
        self.size_hint = (1, 1)
        self.comicBook = comicBook
        self.panelCover=GridLayout(cols=2)
        self.cover = comicBook.getImagePage()
        self.cover.size_hint = (None, )
        # self.cover.size = (1,250)
        # self.panelCover.add_widget(self.cover)
        # self.panelBotonera = GridLayout(cols=1,size_hint = (0.1, 1))
        # self.panelCover.add_widget(self.panelBotonera)
        # self.panelBotonera.add_widget(Button(text="add",size_hint=(None,None),size=(32,32)))
        self.add_widget(self.cover)
        self.cols=1
        self.panelLabel = GridLayout(cols=2,size_hint_y=.4)
        self.label = Label(text=comicBook.getNombreArchivo(),text_size = (100,None))
        self.add_widget(self.label)

class KivyAllComicsGui(Screen):
    def __init__(self, comicBooks, **kwargs):
        # make sure we aren't overriding any important functionality
        super(KivyAllComicsGui, self).__init__(**kwargs)
        self.carrusel = Carousel(direction='right')
        self.carrusel.orientation = 'vertical'
        self.carrusel.size_hint = (1, 1)
        self.listaComicBooks = comicBooks
        self.panel = GridLayout(cols=1)
        self.thumbnailWidth=100
        self.cantidadColumnas = int(Window.width/self.thumbnailWidth)
        self.cantidadFilas = 4
        self.searchText = TextInput(text='Buscar comic', multiline=False)
        self.searchText.size_hint_y = None
        self.searchText.size[1] = 30

        panelBusqueda = GridLayout(cols=self.cantidadColumnas)
        panelBusqueda.add_widget(self.searchText)

        self.btn = Button(text = "buscar")

        self.btn.size_hint = (0.1, None)
        self.btn.size = (32, 32)
        # self.btn.background_normal = "Better Search.png"
        panelBusqueda.add_widget(self.btn)

        self.btn.bind(on_press=self.evntBtnBuscar)

        panelBusqueda.size_hint_y = None

        self.panel.add_widget(panelBusqueda)

        self.panel.add_widget(self.carrusel)
        self.add_widget(self.panel)
        self.__loadComicBooks__()
        self.indice = 0

    def __tbuscar__(self):
        t = Thread(self.buscar())
        t.start()

    def evntBtnBuscar(self,evnt):
        self.__tbuscar__()

    def buscar(self):
        comicBooks = KivyComicBook()
        comicBooks.searchInComicVine(self.searchText.text)
        self.listaPublishers = publishers.listaComicVineSearch
        self.indice=0
        self.__loadComicBooks__()

    def __loadComicBooks__(self):
        self.carrusel.clear_widgets()
        panelx4 = GridLayout(cols=self.cantidadColumnas)
        indice = 0
        for comicBook in self.listaComicBooks:
            if not (indice % (self.cantidadColumnas * self.cantidadFilas) == 0):
                print("agregando a panel")
                self.panelx4.add_widget(KivySmallComicGui(comicBook))
            else:
                print("creando panel y agregando a carusel")
                self.panelx4 = GridLayout(cols=self.cantidadColumnas)
                self.panelx4.add_widget(KivySmallComicGui(comicBook))
                self.carrusel.add_widget(self.panelx4)
            indice += 1

class Test(App):
    def build(self):
        comics = KivyComicBooks()
        lista = comics.list(('%(1970)%','%(1971)%',), 'path like ? or path like ?')
        self.listaComics = comics.listaConsulta

        carousel = KivyAllComicsGui(self.listaComics)



        return carousel

if __name__ == "__main__":
    Test().run()