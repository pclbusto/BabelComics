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
from kivy.uix.carousel import Carousel

class KivyPublisherGui(Screen):
    def __init__(self,**kwargs):
        self.layout = GridLayout()
        self.label = Label(text="Cover Title test")
        self.layout.add_widget(self.label)

class PublisherPanel(BoxLayout):
    def __init__(self, coverFileName, **kwargs):
        # make sure we aren't overriding any important functionality
        super(PublisherPanel, self).__init__(**kwargs)
        self.orientation='vertical'
        self.size_hint=(1,1)
        logo = Image(source=coverFileName)
        self.add_widget(logo)
        self.add_widget(Label(text="test label de publisher",size_hint=(1,0.1)))
        self.size_hint_y=None
        self.height=140
        self.width = 80

class Test(App):
    def build(self):
        carousel = Carousel(direction='right')

        grid = GridLayout(cols=4)
        grid.size_hint_y = None
        grid.height= 140
        grid.size_hint_x=None
        listaImagenes = []
        for i in range(1,9):
            print(i)
            listaImagenes.append(str(i)+".jpg")
        box=BoxLayout()
        box.orientation='horizontal'
        l =  list(range(5,9))
        print(listaImagenes[0])
        for i in range(0,4):
            box.add_widget(PublisherPanel(listaImagenes[i]))
        carousel.add_widget(box)
        box = BoxLayout()
        box.orientation = 'horizontal'
        for i in range(4, 8):
            box.add_widget(PublisherPanel(listaImagenes[i]))
        carousel.add_widget(box)
        return carousel

if __name__ == "__main__":
    test =Test()
    test.run()
    #Test().run()