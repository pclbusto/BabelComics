from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import *
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scatterlayout import ScatterLayout

class KivyPublisherGui(Screen):
    def __init__(self,**kwargs):
        self.layout = GridLayout()

class Test(App):

    def build(self):
        #layout2 = ScatterLayout(do_rotation = False, rotation =90,pos_hint= {'center_x': 0.5, 'center_y': 0.5})
        layout = GridLayout(cols=4,pos=(0,0))
        layout.add_widget(Button(text="boton1"))
        layout.add_widget(Button(text="boton2"))
        layout.add_widget(Button(text="boton3"))
        layout.add_widget(Button(text="boton4"))
        layout.add_widget(Button(text="boton1"))
        layout.add_widget(Button(text="boton2"))
        layout.add_widget(Button(text="boton3"))
        layout.add_widget(Button(text="boton4"))
        #layout2.add_widget(layout)
        return layout
        #return KivyPublisherGui()



if __name__ == "__main__":
    test =Test()
    test.run()
    #Test().run()