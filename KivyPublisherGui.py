from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import *
from kivy.uix.button import Label
from Publishers import *
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage
import Stuff

class KivyPublisherGui(GridLayout):
    def __init__(self,publisher, **kwargs):
        super(KivyPublisherGui,self).__init__(**kwargs)
        self.publisher = publisher
        jpg = Stuff.convertAndDownload(publisher.logoImagePath)
        # self.logo = AsyncImage(source=jpg)
        self.label = Label(text=publisher.name)
        self.cols=1
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
class Test(App):
    def build(self):
        publishers = Publishers()
        publishers.searchInComicVine("Marvel")
        carousel = KivyAllPublishersGui(publishers.listaComicVineSearch,direction='right')
        return carousel

if __name__ == "__main__":
    Test().run()