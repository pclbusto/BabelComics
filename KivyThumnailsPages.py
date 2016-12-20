from kivy.uix.scrollview import ScrollView
from KivyComicGui import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout

from kivy.uix.stacklayout import  StackLayout
from kivy.uix.boxlayout import BoxLayout
from MemoryImage import *
from kivy.uix.button import Button
from kivy.app import App
from KivyComicBooks import *


class KivyThumnail(RelativeLayout):
    def __init__(self, pagina, numeroValor, **kwargs):
        super(KivyThumnail,self).__init__(**kwargs)
        self.add_widget(pagina)
        self.numero = numeroValor
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
            print(obj.numero)
            return True
        else:
            pass



class KivyThumnailsPages(Screen):
    def __init__(self, comicBook, **kwargs):
        super(KivyThumnailsPages, self).__init__(**kwargs)
        listaPaneles=[]
        lista = GridLayout(cols=comicBook.getCantidadPaginas())
        lista.size_hint_x = None
        lista.size_hint_x = 5
        for n in range(1, comicBook.getCantidadPaginas()):
            pagina = comicBook.getImagePage()
            comicBook.gotoNextPage()
            # panel = RelativeLayout()
            # panel.add_widget(pagina)
            # numero = Label(text="[ref="+str(n)+"]"+str(n)+"[/ref]",markup=True, font_size='20sp')
            # numero = Label(text=str(n), font_size='20sp')
            # numero.bold=True
            # numero.color=[0.4,0.8,0.4,0.7]
            # numero.pos_hints=(None,None)
            # numero.pos=(90,0)
            # numero.size_hint=(None,None)
            # numero.size=(20,20)
            # panel.add_widget(numero)
            # listaPaneles.append(panel)
            # panel.bind(on_touch_down=self.referencia)
            # # /panel.name = str(numero)
            # panel.bind(on_press =self.referencia)
            panel = KivyThumnail(pagina,n)
            lista.add_widget(panel)
        self.sb = scroll = ScrollView()
        scroll.size_hint_y = None
        scroll.size[1] = 150
        scroll.add_widget(lista)
        # scroll.bind(on_touch_down=self.referencia)
        self.add_widget(scroll)

class Test(App):
    def build(self):
        comic = KivyComicBook("C:\\comics\\Alex Ross\\JLA_ Secret Origins V2002 #1 (2002).cbz",'Origenes Secretros', 1, 1)
        comic.openCbFile()
        print(comic.getCantidadPaginas())
        return KivyThumnailsPages(comic)


if __name__ == "__main__":
    # Window.size=(1920,1080)
    Test().run()