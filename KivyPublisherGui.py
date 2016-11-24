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
from BabelComicBookManagerConfig  import *
from kivy.core.window import Window

class KivyPublisherGui(GridLayout):
    def __init__(self,publisher, **kwargs):
        super(KivyPublisherGui,self).__init__(**kwargs)
        self.publisher = publisher
        self.size_hint=(None,None)
        self.size=(160,320)
        if publisher.hasLocalLogo():
            self.logo = Image(source=publisher.getLogoLocalPath(), size_hint=(None, None), size=(140, 140))
            self.add_widget(self.logo)
        elif publisher.logoImagePath:
            jpg = Stuff.convertAndDownload(publisher.logoImagePath, BabelComicBookManagerConfig().getPublisherTempLogoPath())
            self.logo = Image(source=jpg,size_hint=(None,None),size=(140,140))
            self.add_widget(self.logo)

        self.cols=1
        self.panelLabel = GridLayout(cols=2)
        self.check = CheckBox(size_hint=(None,None),size=(30,30))
        self.check.bind(active=self.activeEvnt)
        self.panelLabel.add_widget(self.check)
        self.label = Label(text=publisher.name,text_size = (100,None))


        self.panelLabel.add_widget(self.label)
        self.add_widget(self.panelLabel)

    def activeEvnt(self,obj,evnt):
        if self.check.active:
            if not Publishers().get(self.publisher.id):
                Publishers().add(self.publisher)
        else:
            Publishers().rm(self.publisher.id)

class KivyAllPublishersGui(Screen):
    BUSCAR_LOCAL=1
    BUSCAR_VINE=2

    def __init__(self, publishers, **kwargs):
        # make sure we aren't overriding any important functionality
        super(KivyAllPublishersGui, self).__init__(**kwargs)
        self.carrusel = Carousel(direction='right')
        self.carrusel.orientation='vertical'
        self.carrusel.size_hint=(1,1)
        self.listaPublishers = publishers
        self.panel = GridLayout(cols=1)
        self.thumbnailWidth=160
        self.thumbnailHeight = 320

        self.cantidadColumnas = int(Window.width / self.thumbnailWidth)
        self.cantidadFilas = int(Window.height / self.thumbnailHeight)
        # self.searchText = TextInput(text='Buscar editorial ',multiline=False)
        self.searchText = TextInput(text='', multiline=False)
        self.searchText.size_hint =(0.8,None)
        self.searchText.size=(0,30)

        panelBusqueda = GridLayout(cols=3)
        panelBusqueda.add_widget(self.searchText)

        self.btnVine = Button(text="Vine",size_hint = (0.1,None),size = (0,30))
        self.btnLocal = Button(text="Local",size_hint = (0.1,None),size = (0,30))
        panelBusqueda.add_widget(self.btnVine)
        panelBusqueda.add_widget(self.btnLocal)

        self.btnVine.bind(on_press=self.evntBtnBuscarVine)
        self.btnLocal.bind(on_press=self.evntBtnBuscarLocal)

        panelBusqueda.size_hint_y = None

        self.panel.add_widget(panelBusqueda)

        self.panel.add_widget(self.carrusel)
        self.add_widget(self.panel)
        self.__loadPublishers__()
        self.indice = 0

    def __tbuscar__(self,dondeBuscar):
        t = Thread(self.buscar(dondeBuscar))
        t.start()

    def evntBtnBuscarVine(self,evnt):
        self.__tbuscar__(KivyAllPublishersGui.BUSCAR_VINE)

    def evntBtnBuscarLocal(self, evnt):
        self.__tbuscar__(KivyAllPublishersGui.BUSCAR_LOCAL)

    def buscar(self, dondeBuscar):
        publishers = Publishers()

        if dondeBuscar==KivyAllPublishersGui.BUSCAR_VINE:
            publishers.searchInComicVine(self.searchText.text)
            self.listaPublishers = publishers.listaComicVineSearch
            self.indice=0
        elif dondeBuscar==KivyAllPublishersGui.BUSCAR_LOCAL:
            self.listaPublishers = publishers.getList(("%"+self.searchText.text+"%",), "name like ?")
            self.indice = 0
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
        # publishers = Publishers()
        # publishers.searchInComicVine("comics")

        carousel = KivyAllPublishersGui([])



        return carousel

if __name__ == "__main__":
    Test().run()