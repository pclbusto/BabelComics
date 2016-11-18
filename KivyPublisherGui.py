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


class KivyPublisherGui(GridLayout):
    def __init__(self,publisher, **kwargs):
        super(KivyPublisherGui,self).__init__(**kwargs)
        self.publisher = publisher
        if publisher.logoImagePath:
            jpg = Stuff.convertAndDownload(publisher.logoImagePath, "publishers\\temp\\")
            print(jpg)
            # self.logo = AsyncImage(source=jpg)
            self.logo = Image(source=jpg)
            self.add_widget(self.logo)
        self.label = Label(text=publisher.name)
        self.cols=1
        self.add_widget(self.label)

class KivyAllPublishersGui(Screen):
    def __init__(self, publishers, **kwargs):
        # make sure we aren't overriding any important functionality
        super(KivyAllPublishersGui, self).__init__(**kwargs)
        self.carrusel = Carousel(direction='right')
        self.carrusel.orientation='vertical'
        self.carrusel.size_hint=(1,1)
        self.listaPublishers = publishers
        self.panel = GridLayout(cols=1)

        self.searchText = TextInput(text='Buscar editorial',multiline=False)
        self.searchText.size_hint_y =None
        self.searchText.size[1]=30
        panelBusqueda = GridLayout(cols=2)
        panelBusqueda.add_widget(self.searchText)
        self.btn = Button(text="Buscar")
        self.btn.size_hint=(None,None)
        self.btn.size = (32,32)
        panelBusqueda.add_widget(self.btn)
        self.btn.bind(on_press = self.buscar)
        panelBusqueda.size_hint_y = None

        self.panel.add_widget(panelBusqueda )

        self.panel.add_widget(self.carrusel)
        self.add_widget(self.panel)
        self.__loadPublishers__()

    def buscar(self,evnt):
        publishers = Publishers()
        publishers.searchInComicVine(self.searchText.text)
        self.listaPublishers = publishers.listaComicVineSearch
        self.__loadPublishers__()

    def __loadPublishers__(self):
        self.carrusel.clear_widgets()
        panelx4 = GridLayout(cols=2)
        indice = 1
        for publisher in self.listaPublishers:
            if not (indice%5==0):
                panelx4.add_widget(KivyPublisherGui(publisher))
            else:
                self.carrusel.add_widget(panelx4)
                panelx4 = GridLayout(cols=2)
            indice += 1
        if not (indice%5==0):
            self.carrusel.add_widget(panelx4)

class Test(App):
    def build(self):
        publishers = Publishers()
        publishers.searchInComicVine("Marvel")

        carousel = KivyAllPublishersGui(publishers.listaComicVineSearch)



        return carousel

if __name__ == "__main__":
    Test().run()