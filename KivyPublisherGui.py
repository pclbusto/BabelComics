from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import *
from kivy.uix.button import Label
from PublishersModule import *
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage, Image
import Stuff

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

class KivyAllPublishersGui(Carousel):
    def __init__(self, publishers, **kwargs):
        # make sure we aren't overriding any important functionality
        super(KivyAllPublishersGui, self).__init__(**kwargs)
        self.orientation='vertical'
        self.size_hint=(1,1)
        self.listaPublishers = publishers

        panelx4 = GridLayout(cols=2)
        indice = 1

        for publisher in self.listaPublishers:
            if not (indice%5==0):
                panelx4.add_widget(KivyPublisherGui(publisher))
            else:
                self.add_widget(panelx4)
                panelx4 = GridLayout(cols=2)
            indice += 1
            # self.add_widget(KivyPublisherGui(publisher))
class Test(App):
    def build(self):
        publishers = Publishers()
        publishers.searchInComicVine("Dark")
        carousel = KivyAllPublishersGui(publishers.listaComicVineSearch,direction='right')
        return carousel

if __name__ == "__main__":
    Test().run()