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

from threading import Thread

class KivyPublisherGui(GridLayout):
    def __init__(self,publisher, **kwargs):
        super(KivyPublisherGui,self).__init__(**kwargs)
        self.publisher = publisher
        if publisher.logoImagePath:
             jpg = Stuff.convertAndDownload(publisher.logoImagePath, "publishers\\temp\\")
             print(jpg)
             self.logo = Image(source=jpg)
             self.add_widget(self.logo)
        self.cols=1
        self.panelLabel = GridLayout(cols=2)
        self.check = CheckBox()
        self.check.bind(active=self.activeEvnt)
        self.panelLabel.add_widget(self.check)
        self.label = Label(text=publisher.name,text_size = (self.width,None))
        self.panelLabel.add_widget(self.label)
        self.add_widget(self.panelLabel)

    def activeEvnt(self,obj,evnt):
        if self.check.active:
            Publishers().add(self.publisher)
        else:
            Publishers().rm(self.publisher.id)

class KivyAllPublishersGui(Screen):
    def __init__(self, publishers, **kwargs):
        # make sure we aren't overriding any important functionality
        super(KivyAllPublishersGui, self).__init__(**kwargs)
        self.carrusel = Carousel(direction='right')
        self.carrusel.orientation='vertical'
        self.carrusel.size_hint=(1,1)
        self.listaPublishers = publishers
        self.panel = GridLayout(cols=1)
        self.cantidadColumnas = 4
        self.cantidadFilas = 4
        self.searchText = TextInput(text='Buscar editorial',multiline=False)
        self.searchText.size_hint_y =None
        self.searchText.size[1]=30

        panelBusqueda = GridLayout(cols=self.cantidadColumnas)
        panelBusqueda.add_widget(self.searchText)

        self.btn = Button()

        self.btn.size_hint=(None,None)
        self.btn.size = (32,32)
        self.btn.background_normal = "Better Search.png"
        panelBusqueda.add_widget(self.btn)

        self.btn.bind(on_press = self.evntBtnBuscar)

        panelBusqueda.size_hint_y = None

        self.panel.add_widget(panelBusqueda)

        self.panel.add_widget(self.carrusel)
        self.add_widget(self.panel)
        self.__loadPublishers__()
        self.indice = 0

    def __tbuscar__(self):
        t = Thread(self.buscar())
        t.start()

    def evntBtnBuscar(self,evnt):
        self.__tbuscar__()

    def buscar(self):
        publishers = Publishers()
        publishers.searchInComicVine(self.searchText.text)
        self.listaPublishers = publishers.listaComicVineSearch
        self.indice=0
        self.__loadPublishers__()

    def __loadPublishers__(self):
        self.carrusel.clear_widgets()
        panelx4 = GridLayout(cols=self.cantidadColumnas)
        indice = 0
        for publisher in self.listaPublishers:
            if not (indice % (self.cantidadColumnas*self.cantidadFilas) == 0):
                print("agregand a panel")
                self.panelx4.add_widget(KivyPublisherGui(publisher))
            else:
                print("creando oanel y agregando a carusel")
                self.panelx4 = GridLayout(cols=self.cantidadColumnas)
                self.panelx4.add_widget(KivyPublisherGui(publisher))
                self.carrusel.add_widget(self.panelx4)
            indice += 1

class Test(App):
    def build(self):
        publishers = Publishers()
        publishers.searchInComicVine("Marvel")

        carousel = KivyAllPublishersGui(publishers.listaComicVineSearch)



        return carousel

if __name__ == "__main__":
    Test().run()