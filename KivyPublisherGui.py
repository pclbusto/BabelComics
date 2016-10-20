from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import *
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scatter import ScatterPlane
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.button import Label


class KivyPublisherGui(Screen):
    def __init__(self,**kwargs):
        self.layout = GridLayout()
        self.label = Label(text="Cover Title test")
        self.layout.add_widget(self.label)

class PublisherPanel(GridLayout):
    def __init__(self,**kwargs):
        super(Widget, self).__init__(**kwargs)
        self.add_widget(GridLayout(cols=1))
        l1 = Image(source='8.jpg', size=(256, 256))

class Test(App):
    def build(self):
        #layout2 = ScatterLayout(do_rotation = False, rotation =90,pos_hint= {'center_x': 0.5, 'center_y': 0.5})

        layout = GridLayout(cols=1,pos=(0,0))
        layout.add_widget(PublisherPanel())
        #s = ScatterPlane(scale=.5)

        #s.add_widget(l1)
        #layout.add_widget(l1)
        #layout2.add_widget(layout)
        return layout
        #return KivyPublisherGui()



if __name__ == "__main__":
    test =Test()
    test.run()
    #Test().run()