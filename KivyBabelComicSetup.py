from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import *
from kivy.uix.button import Label
from PublishersModule import *
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.treeview import TreeView,TreeViewLabel
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from BabelComicBookManagerConfig import *

class KivyPanelABM(GridLayout):
    def __init__(self, lista, nombreABM, **kwargs):
        # make sure we aren't overriding any important functionality
        super(KivyPanelABM, self).__init__(**kwargs)
        self.cols=2
        self.nombreABM = nombreABM
        self.lista = TreeView(hide_root=True)
        self.add_widget(self.lista)
        self.panelbotoneraAcciones = GridLayout(cols=1, size_hint_y=None, size=(0, 27))
        self.panelbotoneraAcciones.padding=[100,10,10,10]
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
class KivyConfigGui(Screen):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(KivyConfigGui, self).__init__(**kwargs)
        babelComicConfig = BabelComicBookManagerConfig()
        self.grilla = GridLayout(cols=2)


        self.listaDirectorios = TreeView(hide_root=True)
        self.listaTipos = TreeView(hide_root=True)

        self.grilla.add_widget(KivyPanelABM(babelComicConfig.listaClaves,"Clave"))
        self.grilla.add_widget(KivyPanelABM(babelComicConfig.listaDirectorios,"Directorio"))
        self.grilla.add_widget(KivyPanelABM(babelComicConfig.listaTipos,"Tipo Archivo"))

        self.add_widget(self.grilla)

class Test(App):
    def build(self):


        configScreen = KivyConfigGui()



        return configScreen

if __name__ == "__main__":
    Test().run()