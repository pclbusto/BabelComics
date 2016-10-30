from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import *
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scatter import ScatterPlane
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from Publishers import *

from kivy.uix.image import Image, AsyncImage


from kivy.uix.carousel import Carousel

class KivyPublisherGui(Screen):
    def __init__(self,publisher, **kwargs):
        self.layout = GridLayout()
        self.publisher = publisher
        self.logo = AsyncImage(publisher.logoImagePath)
        self.label = Label(text=publisher.name)
        self.layout.add_widget(self.label)

class KivyAllPublishersGui(Carousel):
    def __init__(self, publishers, **kwargs):
        # make sure we aren't overriding any important functionality
        super(KivyAllPublishersGui, self).__init__(**kwargs)
        self.orientation='vertical'
        self.size_hint=(1,1)
        self.listaPublishers = publishers
        for publisher in self.listaPublishers:
            self.add_widget(publisher)
class Test(App):
    def build(self):
        publishers = Publishers()
        publishers.searchInComicVineComicVine("Marvel")
        for publisher in publishers.listaComicVineSearch:
            print(publisher.name, publisher.id)
        publishers.close()

        carousel = KivyAllPublishersGui(direction='right')
        return carousel

if __name__ == "__main__":


    test =Test()
    test.run()
    #Test().run()