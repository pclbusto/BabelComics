from kivy.uix.scrollview import ScrollView
from KivyComicGui import *
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty
from kivy.event import EventDispatcher

from kivy.uix.boxlayout import BoxLayout
from MemoryImage import *
from kivy.uix.button import Button
from kivy.app import App
from KivyComicBooks import *


class KivyThumnail(GridLayout):
    def __init__(self, pagina, numeroValor, padre, **kwargs):
        super(KivyThumnail,self).__init__(**kwargs)
        self.cols=1
        self.padre = padre
        self.add_widget(pagina)
        self.seleccionada = False
        self.numeroValor = numeroValor
        numero = Label(text=str(numeroValor), font_size='20sp')
        numero.bold = True
        numero.color = [0.4, 0.8, 0.4, 0.7]
        numero.pos_hints = (None, None)
        numero.pos = (90, 0)
        numero.size_hint = (None, None)
        numero.size = (20, 20)
        self.add_widget(numero)
        self.bind(on_touch_down=self.referencia)

    def referencia(self, obj, arg):
        if self.collide_point(arg.pos[0],arg.pos[1]):
            self.padre.selectedPage = self.numeroValor
            self.seleccionada = True
            print("referencia")
            return True
        else:
            pass

class KivyThumnailsPages(ModalView, EventDispatcher):
    selectedPage = NumericProperty(-1)

    def __init__(self, comicBook, **kwargs):
        super(KivyThumnailsPages, self).__init__(**kwargs)

        self.listaThumnails=[]
        lista = GridLayout(cols=comicBook.getCantidadPaginas())
        lista.size_hint_x = None
        print(comicBook.getCantidadPaginas())
        lista.size=(120*comicBook.getCantidadPaginas(),0)
        for n in range(1, comicBook.getCantidadPaginas()):
            # pagina = comicBook.getImagePage()
            pagina = comicBook.getThumnail()
            comicBook.gotoNextPage()
            panel = KivyThumnail(pagina,n,self)
            lista.add_widget(panel, index=0)
            self.listaThumnails.append(panel)
        self.sb = scroll = ScrollView()
        scroll.size_hint_y = None
        scroll.size[1] = 150
        scroll.add_widget(lista)
        # scroll.bind(on_touch_down=self.callback)
        self.add_widget(scroll)
        scroll.bind(on_scroll_stop=self.scrollStop)
    def on_selectedPage(self,obj,arg):
        print(self.selectedPage)
    # def callback(self,obj,args):
    #     for panel in self.listaThumnails:
    #         if panel.seleccionada:
    #             self.selectedPage = panel.numeroValor
    #             panel.seleccionada = False
    #
    #     print(self.selectedPage)

    def scrollStop(self,obj,args):
        # print(obj.hbar)
        pass
class Test(App):
    def build(self):
        boton = Button(text="test")
        boton.bind(on_press=self.callback)
        return boton
    def callback(self,args):
        # comic = KivyComicBook(
        #     "C:\\comics\\Batman - Knightfall Volume 1 to 3 (2012) (DC) (Digital) (TheHand-Empire)\\Batman_ Knightfall V2012 #1 (2012).cbz",
        #     'Batman - Knightfalls', 1, 1)
        comic = KivyComicBook("C:\\comics\\Alex Ross\\JLA_ Secret Origins V2002 #1 (2002).cbz", 'Origenes Secretros', 1,
                             1)
        comic.openCbFile()
        print(comic.getCantidadPaginas())
        self.th =  thums = KivyThumnailsPages(comic)
        thums.bind(on_dismiss=self.salida)
        thums.size_hint_y=None
        thums.size=(0,160)
        thums.open()
    def salida(self,args):
        print(self.th.selectedPage)

if __name__ == "__main__":
    # Window.size=(1920,1080)
    Test().run()