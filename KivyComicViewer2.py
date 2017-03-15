from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.carousel import Carousel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from KivyComicBook import *
from kivy.core.window import Window
from kivy.uix.modalview import ModalView
from kivy.input.motionevent import MotionEvent
from kivy.clock import  Clock

class KivyVisor(ModalView):
    MODO_NORMAL = 1
    MODO_AJUSTADO_ALTURA = 2
    MODO_AJUSTADO_ANCHO = 3

    def __init__(self, comicBook, **kwargs):
        super(KivyVisor, self).__init__(**kwargs)
        self.modoVisualizacion=KivyVisor.MODO_NORMAL
        self.carrusel = Carousel()
        self.bind(on_touch_down=self.on_touch)
        self.comic = comicBook
        self.comic.openCbFile()
        self.matrizTransfPagina= None
        self.listaPaginas=[]
        self.__loadComicBooks__()

        self.carrusel.bind(index=self.carruselSlide)
        self.add_widget(self.carrusel)

    def __updateCarrusell__(self,args):
        imagenPagina = self.comic.getImagePage()
        imagenPagina.size = imagenPagina.texture_size
        imagenPagina.size_hint = (None, None)
        imagenPagina.size_hint=(None,None)
        imagenPagina.keep_ratio = True
        scrollView = ScrollView()
        scrollView.add_widget(imagenPagina)
        self.carrusel.add_widget(scrollView)
        self.listaPaginas.append(imagenPagina)
        if not self.comic.gotoNextPage():
            Clock.unschedule(self.hiloCargaThumnails)
            return False
    def __loadComicBooks__(self):
        self.carrusel.clear_widgets()
        self.hiloCargaThumnails =  Clock.schedule_interval(self.__updateCarrusell__, 1)

    def carruselSlide(self,args,args2):
        self.carrusel.current_slide.scroll_y = 1
        self.carrusel.next_slide.scroll_y=1

        # if scatter.transform!=self.matrizTransfPagina:
        #     scatter.apply_transform(self.matrizTransfPagina)

    def on_transform_with_touch(self, touch,args):
        print(touch.scale)
        for slide in self.carrusel.slides:
            if slide!=touch:
                slide.scale = touch.scale
                slide.pos = touch.pos
        #         slide.apply_transform(touch.transform)
        # self.matrizTransfPagina = touch.transform
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


    def __refreshPage__(self):
        pass

    def ancho(self,event):
        self.modoVisualizacion = KivyVisor.MODO_AJUSTADO_ANCHO

        for imagen in self.listaPaginas:
            if imagen.image_ratio < 1:
                imagen.width = Window.width
                imagen.height =  Window.width/(imagen.image_ratio)
            else:
                imagen.width = Window.width
                imagen.height = Window.width * (imagen.image_ratio)
        for scroll in self.carrusel.slides:
            self.carrusel.current_slide.scroll_y = 0.5

    def ajustarAlto(self,event):

        self.modoVisualizacion = KivyVisor.MODO_AJUSTADO_ALTURA
        for imagen in self.listaPaginas:
            if imagen.image_ratio < 1:
                imagen.width = Window.height/(imagen.image_ratio)
                imagen.height = Window.height
            else:
                imagen.width = Window.height * (imagen.image_ratio)
                imagen.height = Window.height
        for scroll in self.carrusel.slides:
            self.carrusel.current_slide.scroll_x = 0

    def rotar(self,event):
        print(self.carrusel.current_slide.size)
        print(self.listaPaginas[self.carrusel.index].pos)
        self.listaPaginas[self.carrusel.index].pos[0]+=1
    def sinAjuste(self,event):
        self.listaPaginas[self.carrusel.index].height = self.listaPaginas[self.carrusel.index].originalHeight
        self.listaPaginas[self.carrusel.index].width = self.listaPaginas[self.carrusel.index].originalWidth


class Aplication(App):
    def build(self):
        comicBook = KivyComicBook('C:\\comics\\Batman\\01 - KnightFall - 1993\\01 - KnightFall - 1993\\Detective Comics V1937 #661 (1993).cbz')
        kv = KivyVisor(comicBook)
        return kv
if __name__ == "__main__":
    Aplication().run()

