from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from KivyComicViewer import *

class KivyBabelComic(App):
    def __init__(self, **kwargs):
        super(KivyBabelComic,self).__init__(**kwargs)
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(KivyVisor())
        self.sm.bind(on_touch_down=self.on_touch_down)
        return self.sm


    def on_touch_down(self, obj, event):
        '''
        vamos a capturar eventos en estas zonas
        *************************
        *                       *
        *                       *
        *                       *
        *                       *
        * *                   * *
        *3*                   *4*
        * *                   * *
        *                       *
        *                       *
        *                       *
        *1*       *2*         *3*
        * *       * *         * *
        *************************
        :param widget:
        :param event:
        :return:
        '''

        if obj != self.sm: return
        #zona1 = ((0, Window.width * 0.1), (Window.height * 0.1 + Window.height * 0.5,Window.height * -0.1 + Window.height * 0.5 ))

        zona2 = ((Window.width * 0.5 - Window.width * 0.1, Window.width * 0.5 + Window.width * 0.1),
                 (0, Window.height * 0.1))
        #zona3 = ((Window.width - Window.width * 0.1, Window.width), (Window.height * 0.1 + Window.height * 0.5 , Window.height * -0.1 + Window.height * 0.5))


        if (zona2[0][0]< event.pos[0] and event.pos[0] < zona2[0][1]) and (zona2[1][0]<event.pos[1] and event.pos[1]<zona2[1][1]):
            box = GridLayout(cols=5)
            botonAncho = Button(text="nada")
            botonAncho.bind(on_press=self.nada)
            box.add_widget(botonAncho)
            botonCentrado = Button(text="nada")
            botonCentrado.bind(on_press=self.nada)
            box.add_widget(botonCentrado)
            botonSalir = Button(text="salir")
            botonSalir.bind(on_press=self.salir)
            box.add_widget(botonSalir)


            p = Popup(title='Test popup',  size_hint=(None, None), size=(400, 150))
            p.add_widget(box)

            p.open()
    def nada(self,  event):
        print("Falta implementar")

    def salir(self, event):
        self.stop()
if __name__ == "__main__":
    KivyBabelComic().run()