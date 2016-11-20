from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import *
from kivy.uix.button import Label
from PublishersModule import *
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from ComicBooks import *
from kivy.uix.treeview import TreeView,TreeViewLabel
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from BabelComicsScanner import BabelComicBookScanner
import threading
import time

from BabelComicBookManagerConfig import *

class KivyPanelABM(GridLayout):
    def __init__(self, lista, nombreABM, **kwargs):
        # make sure we aren't overriding any important functionality
        super(KivyPanelABM, self).__init__(**kwargs)
        self.cols=2
        self.nombreABM = nombreABM
        self.lista = TreeView(hide_root=True,size_hint_x=0.9)
        self.add_widget(self.lista)
        self.panelbotoneraAcciones = GridLayout(cols=1, size_hint_x=0.1, size_hint_y=None, size=(0, 27))
        # self.panelbotoneraAcciones.padding=[100,10,10,10]
        self.btnAdd = Button(background_normal="Add.png",  size_hint=(None,None), size=(21, 27))
        self.btnAdd.bind(on_press=self.btnEventAdd)
        self.btnEdit = Button(background_normal="Edit.png", size_hint=(None,None), size=(21, 27))
        self.btnEdit.bind(on_press=self.btnEventEdit)
        self.btnDel = Button(background_normal="Delete.png", size_hint=(None,None), size=(21, 27))
        self.btnDel.bind(on_press=self.btnEventDel)

        self.panelbotoneraAcciones.add_widget(self.btnAdd)
        self.panelbotoneraAcciones.add_widget(self.btnEdit)
        self.panelbotoneraAcciones.add_widget(self.btnDel)
        self.add_widget(self.panelbotoneraAcciones)

        for elemento in lista:
            self.lista.add_node(TreeViewLabel(text=elemento))

    def getLista(self):
        list = []
        print("arbol: "+str(self.lista))
        for nodo in self.lista.iterate_all_nodes(node=None):
            list.append(nodo.text)
        return list[1:]
    def btnEventAdd(self, value):
        panel = GridLayout(cols=1)
        self.text = TextInput()
        panel.add_widget(self.text)
        # botonGuardar = Button(text="guardar")uardar)
        panel.add_widget(Button(text="guardar",on_press=self.guardar))
        self.popup = Popup(title='Agregar '+self.nombreABM,
                      content=panel,
                      size_hint=(1, 0.6))
        self.popup.open()
    def guardar(self,value):
        self.lista.add_node(TreeViewLabel(text=self.text.text))
        self.popup.dismiss()

    def __deleteItem__(self):
        if  self.lista.selected_node:
            self.lista.remove_node(self.lista.selected_node)

    def btnEventDel(self, value):
        self.__deleteItem__()

    def btnEventEdit(self, value):
        panel = GridLayout(cols=1)
        self.text = TextInput(text=self.lista.get_selected_node().text)
        panel.add_widget(self.text)
        panel.add_widget(Button(text="guardar", on_press=self.modificar))
        self.popup = Popup(title='Editar ' + self.nombreABM,
                           content=panel,
                           size_hint=(1, 0.6))
        self.popup.open()

    def modificar(self,value):
        self.lista.get_selected_node().text=self.text.text
        # self.lista.add_node(TreeViewLabel(text=self.text.text))
        self.popup.dismiss()

class KivyPanelScanner(GridLayout):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(KivyPanelScanner, self).__init__(**kwargs)
        self.cols=1
        self.progressBar = ProgressBar(max=100,size_hint_y=None,size=(0,20))
        self.panelBotones=GridLayout(cols=2,size_hint_y=None, size=(0,20))
        btnLimpiarComics = Button(text="Limpiar base de comics")
        btnLimpiarComics.bind(on_press=self.borrarComics)
        btnScanear = Button(text="Iniciar scaneo de comics")
        btnScanear.bind(on_press=self.initScanner)
        self.panelBotones.add_widget(btnLimpiarComics)
        self.panelBotones.add_widget(btnScanear)
        self.add_widget(self.progressBar)
        self.add_widget(self.panelBotones)
        self.statusText = Label(size_hint_y=None, size=(0, 20))
        self.add_widget(self.statusText)

    def mostrarMensajeStatus(self,mensaje):
        self.textoStatus = mensaje
        t = threading.Thread(target=self.__cargaMensajeyBorrar)
        t.start()

    def __cargaMensajeyBorrar(self):
        self.statusText.text = self.textoStatus
        time.sleep(5)
        self.statusText.text = self.textoStatus = ""

    def borrarComics(self,value):
        comics = ComicBooks()
        comics.rmAll()
        self.mostrarMensajeStatus("Base de comics limpia.")

    def initScanner(self,value):
        self.config = BabelComicBookManagerConfig()
        self.manager = BabelComicBookScanner(self.config.listaDirectorios, self.config.listaTipos)
        self.manager.iniciarScaneo()
        t = threading.Thread(target=self.checkScanning)
        t.start()

    def checkScanning(self):
        while (self.manager.scanerDir.isAlive()):
            self.statusText.text  = "porcentanje scannig {:.2%}".format(self.manager.porcentajeCompletado/100)
            self.progressBar.value  = self.manager.porcentajeCompletado

class KivyConfigGui(Screen):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(KivyConfigGui, self).__init__(**kwargs)
        self.babelComicConfig = babelComicConfig = BabelComicBookManagerConfig()
        self.panelPrincipal = GridLayout(cols=1)
        self.grilla = GridLayout(cols=2)
        self.panelPrincipal.add_widget(self.grilla)

        self.abmClaves=KivyPanelABM(babelComicConfig.listaClaves,"Clave")
        self.abmDirectorios = KivyPanelABM(babelComicConfig.listaDirectorios,"Directorio")
        self.abmTipos = KivyPanelABM(babelComicConfig.listaTipos,"Tipo Archivo")

        self.grilla.add_widget(self.abmClaves)
        self.grilla.add_widget(self.abmDirectorios)
        self.grilla.add_widget(self.abmTipos)
        self.grilla.add_widget(KivyPanelScanner())

        self.btnGuardar=Button(text="Guardar",size_hint_y=None, size=(0,20))
        self.panelPrincipal.add_widget(self.btnGuardar)
        self.btnGuardar.bind(on_press=self.btnGuardarEvnt)
        self.statusText = Label(size_hint_y=None, size=(0,20))
        self.panelPrincipal.add_widget(self.statusText)
        self.add_widget(self.panelPrincipal)



    def btnGuardarEvnt(self, value):
        self.babelComicConfig.setListaDirectorios(self.abmDirectorios.getLista())
        self.babelComicConfig.setListaTipos(self.abmTipos.getLista())
        self.babelComicConfig.setListaClaves(self.abmClaves.getLista())
        self.statusText.text='Status: Gurdado exitosamente'

class Test(App):
    def build(self):


        configScreen = KivyConfigGui()



        return configScreen

if __name__ == "__main__":
    Test().run()