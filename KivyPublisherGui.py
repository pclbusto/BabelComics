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
from PublishersModule import *

from kivy.uix.image import Image, AsyncImage


from kivy.uix.carousel import Carousel

class KivyPublisherGui(GridLayout):
    def __init__(self,publisher, **kwargs):
        super(KivyPublisherGui,self).__init__(**kwargs)
        self.publisher = publisher
        self.logo = Image(source=publisher.logoImagePath)
        self.label = Label(text=publisher.name)
        self.cols=1
        self.add_widget(self.logo)
        self.add_widget(self.label)


class KivyAllPublishersGui(Carousel):
    def __init__(self, publishers, **kwargs):
        # make sure we aren't overriding any important functionality
        super(KivyAllPublishersGui, self).__init__(**kwargs)
        self.orientation='vertical'
        self.size_hint=(1,1)
        self.listaPublishers = publishers
        for publisher in self.listaPublishers:
            self.add_widget(KivyPublisherGui(publisher))
        #self.add_widget(KivyPublisherGui(publishers[0]))
class Test(App):
    def build(self):
        publishers = Publishers()
        # publishers.searchInComicVineComicVine("Marvel")
        # for publisher in publishers.listaComicVineSearch:
        #     print(publisher.name, publisher.id)
        # publishers.close()
        dc = Publisher(1,"dc")
        dc.logoImagePath="dcComics.jpg"
        publishers.listaComicVineSearch.append(dc)
        # marvel = Publisher(1, "marvel")
        # marvel.logoImagePath = "marvel.gif"
        # publishers.listaComicVineSearch.append(marvel)
        # darkhorse = Publisher(1, "Dark Horse")
        # darkhorse.logoImagePath = "darkhorse.gif"
        # publishers.listaComicVineSearch.append(darkhorse)
        idw = Publisher(1, "idw")
        idw.logoImagePath = "idw.jpg"
        publishers.listaComicVineSearch.append(idw)
        image = Publisher(1, "Image")
        image.logoImagePath = "image.jpg"
        publishers.listaComicVineSearch.append(image)
        carousel = KivyAllPublishersGui(publishers.listaComicVineSearch,direction='right')
        return carousel

if __name__ == "__main__":
    test =Test()
    test.run()
    #Test().run()