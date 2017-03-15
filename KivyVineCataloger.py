from kivy.uix.modalview import ModalView
from KivyComicGui import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import  StackLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.button import Button
from kivy.app import App
from KivyComicBooks import *
from KivyComicGui import *

class KivyVineCataloger(ModalView):

    def __init__(self, comicBook, **kwargs):
        super(KivyVineCataloger, self).__init__(**kwargs)
        self.panel = GridLayout(cols=3)
        print("Antes de dar error")
        self.original = KivySmallComicGui(comicBook,size_hint=(1,None))
        print("Despues de dar error")
        self.panel.add_widget(self.original)
        self.panelSerie=GridLayout(cols=1,size_hint=(0.3,None))
        self.panelSerie.add_widget(Button(text="Serie", size_hint=(0.5,None),size=(0,30)))
        self.panelEjemplar = GridLayout(cols=1,size_hint=(0.3,None))
        self.panelEjemplar.add_widget(Button(text="Ejemplar", size_hint=(0.5,None),size=(0,30)))
        self.panel.add_widget(self.panelSerie)
        self.panel.add_widget(self.panelEjemplar)
        self.add_widget(self.panel)

class Test(App):
    def build(self):
        comics = KivyComicBooks()
        lista = comics.list(('%Green Lantern Corps %',), 'path like ?')
        self.listaComics = comics.listaConsulta
        return KivyVineCataloger(self.listaComics[1])

if __name__ == "__main__":
    # Window.size=(1920,1080)
    Test().run()
