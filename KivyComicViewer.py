from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from KivyComicBook import *
from kivy.core.window import Window

class KivyVisor(App):
    def on_touch_down(self,widget, event):
        '''
        vamos a capturar eventos en estas zonas
        *************************
        *1*                   *2*
        ***                   ***
        *                       *
        *                       *
        * *                   * *
        *3*                   *4*
        * *                   * *
        *                       *
        *                       *
        *                       *
        ***                   ***
        *5*                   *6*
        *************************
        :param widget:
        :param event:
        :return:
        '''
        #zona1 = ((0, Window.width * 0.1), (Window.height, (Window.height - Window.height * 0.1)))
        #zona2 = ((Window.width - Window.width * 0.1, Window.width), (Window.height, (Window.height - Window.height * 0.1)))
        zona3 = ((0, Window.width * 0.1), (Window.height * 0.1 + Window.height * 0.5,Window.height * -0.1 + Window.height * 0.5 ))
        zona4 = ((Window.width - Window.width * 0.1, Window.width), (Window.height * 0.1 + Window.height * 0.5 , Window.height * -0.1 + Window.height * 0.5))
        print(zona4[0][0]< event.pos[0])
        print(event.pos[0] < zona4[0][1])
        print(event.pos[1]<zona4[1][0], zona4[1][0])
        print(event.pos[1]>zona4[1][1])

        print( event.pos[1])
        if (zona3[0][0]< event.pos[0] and event.pos[0] < zona3[0][1]) and (event.pos[1]<zona3[1][0] and event.pos[1]>zona3[1][1]):
            self.comic.gotoPrevPage()
            self.imagenPagina = self.comic.getImagePage()
            self.scatter.add_widget(self.imagenPagina)
        if (zona4[0][0]< event.pos[0] and event.pos[0] < zona4[0][1]) and (event.pos[1]<zona4[1][0] and event.pos[1]>zona4[1][1]):
            self.comic.gotoNextPage()
            self.imagenPagina = self.comic.getImagePage()
            self.scatter.add_widget(self.imagenPagina)
    def build(self):
        flow = FloatLayout()
        flow.bind(on_touch_down=self.on_touch_down)
        self.comic = KivyComicBook("E:\\Comics\\DC\\Green Lantern\\144 Blackest Night\\Blackest Night_ Tales of the Corps V2009 #1 (of 3) (2009).cbz")
        self.comic.openCbFile()
        self.scatter = Scatter(scale_min=.5)
        self.imagenPagina = self.comic.getImagePage()
        self.scatter.add_widget(self.imagenPagina)
        print(Window.center)
        #centrar la imagen
        self.scatter.pos=(Window.center[0]-(self.imagenPagina.width/2),Window.center[1]-(self.imagenPagina.height/2))
        #ajustar tamañio a altura
        #alturaactual    1
        #altura venta    x
        self.scatter.scale=Window.height/self.imagenPagina.height
        flow.add_widget(self.scatter)
        return flow

if __name__ == "__main__":
    KivyVisor().run()
