from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from KivyComicBook import *
from kivy.core.window import Window
from kivy.uix.modalview import ModalView
from kivy.input.motionevent import MotionEvent

class KivyVisor(ModalView):

    def __init__(self, comicBook, **kwargs):
        super(KivyVisor, self).__init__(**kwargs)
        self.scatter = Scatter()
        self.bind(on_touch_down=self.on_touch)
        self.comic = comicBook
        self.comic.openCbFile()
        self.imagenPagina = self.comic.getImagePage()
        self.imagenPagina.size = self.imagenPagina.texture_size
        print(self.imagenPagina.texture_size)
        self.scatter.size_hint = (None, None)
        self.scatter.size=self.imagenPagina.texture_size

        self.scatter.pos_hint=(None, None)
        # self.imagenPagina.center = self.scatter.center
        # self.scatter.center = Window.center
        #self.scatter.size =self.imagenPagina.size
        # self.scatter.size_hint = (None,None)
        self.scatter.add_widget(self.imagenPagina)
        self.scatter.do_rotation=False
        self.add_widget(self.scatter)
        self.scatter.pos=(0,0)
        # Window.center[1]-(self.imagenPagina.height/2)
        #ajustar tamañio a altura
        #alturaactual/#altura venta (regla de tres simple)
        # self.scatter.scale=Window.height/self.imagenPagina.height
        #centrar la imagen

        # Window.center[0]-(self.imagenPagina.width/2)
        Window.bind(on_motion=self.on_motion)

    def on_motion(self, etype, motionevent,other):
        if other.is_mouse_scrolling:
            if other.button=='scrolldown':
                self.scatter.y -=10
            if other.button=='scrollup':
                self.scatter.y +=10


        else:
            # print(self.scatter.pos)
            print("tamaño imagen :{}".format(self.imagenPagina.size))
            print("tamaño scatter :{}".format(self.scatter.size))
        # help(other)
        # print(motionevent)
        # print(other)
        # print("Capturan scroll")



    def on_touch(self, obj, event):
        '''
        vamos a capturar eventos en estas zonas
        *************************
        *1*       *0*         *2*
        ***       ***         ***
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
        zona0 = ((Window.width*0.5-Window.width*0.1,Window.width*0.5+Window.width*0.1),(Window.height - Window.height * 0.1,Window.height))
        zona3 = ((0, Window.width * 0.1), (Window.height * 0.1 + Window.height * 0.5,Window.height * -0.1 + Window.height * 0.5 ))
        zona4 = ((Window.width - Window.width * 0.1, Window.width), (Window.height * 0.1 + Window.height * 0.5 , Window.height * -0.1 + Window.height * 0.5))

        if (zona3[0][0]< event.pos[0] and event.pos[0] < zona3[0][1]) and (event.pos[1]<zona3[1][0] and event.pos[1]>zona3[1][1]):
            self.comic.gotoPrevPage()
            self.scatter.remove_widget(self.imagenPagina)
            self.imagenPagina = self.comic.getImagePage()
            self.imagenPagina.size = self.imagenPagina.texture_size
            self.scatter.add_widget(self.imagenPagina)
        if (zona4[0][0]< event.pos[0] and event.pos[0] < zona4[0][1]) and (event.pos[1]<zona4[1][0] and event.pos[1]>zona4[1][1]):
            self.scatter.remove_widget(self.imagenPagina)
            self.comic.gotoNextPage()
            self.imagenPagina = self.comic.getImagePage()
            self.imagenPagina.size = self.imagenPagina.texture_size
            self.scatter.add_widget(self.imagenPagina)
        if (zona0[0][0]< event.pos[0] and event.pos[0] < zona0[0][1]) and (zona0[1][0]<event.pos[1] and event.pos[1]<zona0[1][1]):
            box = GridLayout(cols=5)
            botonAncho = Button(text="Ancho")
            botonAncho.bind(on_press=self.ancho)
            box.add_widget(botonAncho)

            botonAjustarAlto = Button(text="Alto")
            botonAjustarAlto.bind(on_press=self.ajustarAlto)
            box.add_widget(botonAjustarAlto)

            botonCentrado = Button(text="Centrar")
            botonCentrado.bind(on_press=self.centrado)
            box.add_widget(botonCentrado)

            botonRotar = Button(text="Rotar")
            botonRotar.bind(on_press=self.rotar)
            box.add_widget(botonRotar)

            p = Popup(title='Comic View popup',  size_hint=(None, None), size=(400, 150))
            p.add_widget(box)

            p.open()
    def ancho(self,event):
        print(Window.width)
        self.scatter.scale = Window.width / self.imagenPagina.width
        self.scatter.pos = (0, 0)

    def ajustarAlto(self,event):
        print(Window.height)
        self.scatter.scale = Window.height / self.imagenPagina.height
        self.scatter.pos = (0, 0)

    def rotar(self,event):
        print("rotar")
    def centrado(self,event):
        # print( Window.center)
        # print(Window.center[0] - (self.imagenPagina.width / 2), Window.center[1] - (self.imagenPagina.height / 2))
        self.scatter.scale = Window.height / self.imagenPagina.height
        self.scatter.pos=(0,0)
        #Window.center[0] - (self.imagenPagina.width ), 0)
        print("centrado")
        self.scatter.center = Window.center


class Test(App):
    def build(self):
        comicBook = KivyComicBook("C:\\Comics\\Green Lanterns 009 (2016) (2 covers) (digital) (Minutemen-Thoth).cbz")
        return KivyVisor(comicBook)
if __name__ == "__main__":
    Test().run()

