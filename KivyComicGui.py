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
from ComicBooks import *
from BabelComicBookManagerConfig import *
from kivy.uix.listview import ListView

# class KivySmallComicGui(GridLayout):
#     def __init__(self,comicBook, **kwargs):
#         super(KivySmallComicGui,self).__init__(**kwargs)
#         self.comicBook = comicBook
#         self.cover = comicBook.getImagePage()
#         self.add_widget(self.logo)
#         self.cols=1
#         self.panelLabel = GridLayout(cols=2)
#         self.label = Label(text=comicBook.name,text_size = (self.width,None))
#         self.add_widget(self.label)

class KivyConfigGui(Screen):
    def __init__(self, babelComicConfig, **kwargs):
        # make sure we aren't overriding any important functionality
        super(KivyConfigGui, self).__init__(**kwargs)
        self.grilla = GridLayout(cols=2)
        self.listaClaves = ListView()
        self.listaClaves.item_strings = babelComicConfig.listaClaves
        self.add_widget(self.panel)

                self.panelx4.add_widget(KivySmallComicGui(comic))
                self.carrusel.add_widget(self.panelx4)
            indice += 1


class Test(App):
    def build(self):
        comics = ComicBooks()
        comics.list("path like'" +  + "'")
        self.listaComics = comics.listaConsulta

        carousel = KivyAllComicssGui(publishers.listaComicVineSearch)



        return carousel

if __name__ == "__main__":
    Test().run()