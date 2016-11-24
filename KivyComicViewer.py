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
    MODO_NORMAL = 1
    MODO_AJUSTADO_ALTURA = 2
    MODO_AJUSTADO_ANCHO = 3

    def __init__(self, comicBook, **kwargs):
        super(KivyVisor, self).__init__(**kwargs)
        self.modoVisualizacion=KivyVisor.MODO_NORMAL
        self.scatter = Scatter()
        self.scatter.center = Window.center
        print("scatter center: {}".format(self.scatter.center))
        self.bind(on_touch_down=self.on_touch)
        self.comic = comicBook
        self.comic.openCbFile()
        self.imagenPagina = self.comic.getImagePage()
        self.imagenPagina.size = self.imagenPagina.texture_size
        self.imagenPagina.size_hint=(None,None)
        self.scatter.size_hint = (None, None)
        self.scatter.size=self.imagenPagina.texture_size
        self.scatter.center = Window.center
        print("image size: {}".format(self.imagenPagina.size))
        print("scatter center: {}".format(self.scatter.center))
        print("window center: {}".format(Window.center))
        self.scatter.pos_hint=(None, None)
        self.scatter.add_widget(self.imagenPagina)
        self.scatter.do_rotation=False

        self.scatter.center=(0,0)
        self.imagenPagina.center=(0,0)
        '''recordar que la imagen se mueve desde el centro. y la posicion es relativa al centro del contenedor en este caso es el scatter'''
        self.imagenPagina.pos = (0,Window.center[1]-self.imagenPagina.size[1]/2)


        self.add_widget(self.scatter)
        # self.scatter.x = 1111
        print("scatter center: {}".format(self.scatter.center))
        print("scatter Heiht: {}".format(self.scatter.height))
        Window.bind(on_motion=self.on_motion)
        Window.bind(on_resize=self.on_sizeWindow)
    def on_sizeWindow(self,arg1,arg2,arg3):
        self.__refreshPage__()
    def on_motion(self, etype, motionevent,other):
        if other.is_mouse_scrolling:
            if other.button=='scrolldown':
                self.scatter.y -=10
            if other.button=='scrollup':
                self.scatter.y +=10


        else:
            # print(self.scatter.pos)
            print("pos imagen :{}".format(self.imagenPagina.pos))
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
            self.scatter.remove_widget(self.imagenPagina)
            self.comic.gotoPrevPage()
            self.__refreshPage__()

        if (zona4[0][0]< event.pos[0] and event.pos[0] < zona4[0][1]) and (event.pos[1]<zona4[1][0] and event.pos[1]>zona4[1][1]):
            self.scatter.remove_widget(self.imagenPagina)
            self.comic.gotoNextPage()
            self.__refreshPage__()
        if (zona0[0][0]< event.pos[0] and event.pos[0] < zona0[0][1]) and (zona0[1][0]<event.pos[1] and event.pos[1]<zona0[1][1]):
            box = GridLayout(cols=5)
            botonAncho = Button(text="Ancho")
            botonAncho.bind(on_press=self.ancho)
            box.add_widget(botonAncho)

            botonAjustarAlto = Button(text="Alto")
            botonAjustarAlto.bind(on_press=self.ajustarAlto)
            box.add_widget(botonAjustarAlto)

            botonCentrado = Button(text="normal")
            botonCentrado.bind(on_press=self.sinAjuste)
            box.add_widget(botonCentrado)

            botonRotar = Button(text="Rotar")
            botonRotar.bind(on_press=self.rotar)
            box.add_widget(botonRotar)

            p = Popup(title='Comic View popup',  size_hint=(None, None), size=(400, 150))
            p.add_widget(box)

            p.open()

    def ancho(self,event):
        print(Window.width)
        self.modoVisualizacion = KivyVisor.MODO_AJUSTADO_ANCHO
        self.scatter.scale = Window.width / self.imagenPagina.width
        self.__refreshPage__()
        #
        # self.scatter.pos = (0, 0)

    def __refreshPage__(self):
        self.scatter.remove_widget(self.imagenPagina)
        self.imagenPagina = self.comic.getImagePage()
        self.scatter.center = self.imagenPagina.center = Window.center
        self.imagenPagina.size = self.imagenPagina.texture_size
        self.scatter.add_widget(self.imagenPagina)

        if self.modoVisualizacion == KivyVisor.MODO_NORMAL:
            self.imagenPagina.pos = (0, Window.center[1] - self.imagenPagina.size[1] / 2)
        elif self.modoVisualizacion == KivyVisor.MODO_AJUSTADO_ALTURA:
            self.imagenPagina.pos = (0, 0)
        elif self.modoVisualizacion == KivyVisor.MODO_AJUSTADO_ANCHO:

            self.imagenPagina.pos = (0,(self.scatter.scale,(Window.center[1] - (self.imagenPagina.size[1] / 2 )*self.scatter.scale)))
            print("Centro window {} size_y {} factor {} new_pos_Y {}".format(Window.center[1], self.imagenPagina.size[1], self.scatter.scale,(Window.center[1] - (self.imagenPagina.size[1] / 2 )*self.scatter.scale)))
    def ajustarAlto(self,event):
        print("alto: {}".format(Window.height))
        self.modoVisualizacion = KivyVisor.MODO_AJUSTADO_ALTURA
        self.scatter.scale = Window.height / self.imagenPagina.height
        self.__refreshPage__()
        #
        # self.scatter.pos = (0, 0)

    def rotar(self,event):
        print("rotar")
    def sinAjuste(self,event):
        self.scatter.scale = 1
        self.scatter.pos=(0,0)
        print("centrado")
        self.scatter.center = Window.center


class Test(App):
    def build(self):
        comicBook = KivyComicBook("E:\\Comics\Marvel\\Iron man comics 1963-2010\\Iron Man DVD2\\Iron-Man101-200\\Iron Man V1968 #102 (1977).cbz")
        kv = KivyVisor(comicBook)
        return kv
if __name__ == "__main__":
    Test().run()

