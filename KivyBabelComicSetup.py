from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import *
from kivy.uix.button import Label
from PublishersModule import *
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.treeview import TreeView,TreeViewLabel
from kivy.uix.scrollview import ScrollView

from BabelComicBookManagerConfig import *

class KivyConfigGui(Screen):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(KivyConfigGui, self).__init__(**kwargs)
        babelComicConfig = BabelComicBookManagerConfig()
        self.grilla = GridLayout(cols=2)

        self.listaClaves = TreeView(hide_root=True)
        self.listaDirectorios = TreeView(hide_root=True)
        self.listaTipos = TreeView(hide_root=True)

        self.panelClaves=GridLayout(cols=1)
        self.panelbotoneraAccionesClaves = GridLayout(cols=3,size_hint_y=None,size = (32,32))
        self.btnAddClave = Button(background_normal = "Add.png",size_hint=(None,None),size = (32,32))
        self.btnEditClave = Button(background_normal = "Edit.png",size_hint=(None,None),size = (32,32))
        self.btnDelClave = Button(background_normal = "Delete.png",size_hint=(None,None),size = (32,32))
        self.panelbotoneraAccionesClaves.add_widget(self.btnAddClave)
        self.panelbotoneraAccionesClaves.add_widget(self.btnEditClave)
        self.panelbotoneraAccionesClaves.add_widget(self.btnDelClave)
        self.panelClaves.add_widget(self.panelbotoneraAccionesClaves)
        self.panelClaves.add_widget(self.listaClaves)
        self.grilla.add_widget(self.panelClaves)

        self.panelDirectorios=GridLayout(cols=1)
        self.panelbotoneraAccionesDirectorios = GridLayout(cols=3,size_hint_y=None,size = (32,32))
        self.btnAddClave = Button(background_normal = "Add.png",size_hint=(None,None),size = (32,32))
        self.btnEditClave = Button(background_normal = "Edit.png",size_hint=(None,None),size = (32,32))
        self.btnDelClave = Button(background_normal = "Delete.png",size_hint=(None,None),size = (32,32))
        self.panelbotoneraAccionesDirectorios.add_widget(self.btnAddClave)
        self.panelbotoneraAccionesDirectorios.add_widget(self.btnEditClave)
        self.panelbotoneraAccionesDirectorios.add_widget(self.btnDelClave)
        self.panelDirectorios.add_widget(self.panelbotoneraAccionesDirectorios)
        self.panelDirectorios.add_widget(self.listaDirectorios)
        self.grilla.add_widget(self.panelDirectorios)

        self.panelTipos=GridLayout(cols=1)
        self.panelbotoneraAccionesTipos = GridLayout(cols=3,size_hint_y=None,size = (32,32))
        self.btnAddClave = Button(background_normal = "Add.png",size_hint=(None,None),size = (32,32))
        self.btnEditClave = Button(background_normal = "Edit.png",size_hint=(None,None),size = (32,32))
        self.btnDelClave = Button(background_normal = "Delete.png",size_hint=(None,None),size = (32,32))
        self.panelbotoneraAccionesTipos.add_widget(self.btnAddClave)
        self.panelbotoneraAccionesTipos.add_widget(self.btnEditClave)
        self.panelbotoneraAccionesTipos.add_widget(self.btnDelClave)
        self.panelTipos.add_widget(self.panelbotoneraAccionesTipos)
        self.panelTipos.add_widget(self.listaTipos)
        self.grilla.add_widget(self.panelTipos)



        for clave in babelComicConfig.listaClaves:
            self.listaClaves.add_node( TreeViewLabel (text =clave))
        for direcctorio in babelComicConfig.listaDirectorios:
            self.listaDirectorios.add_node( TreeViewLabel (text =direcctorio))
        for tipo in babelComicConfig.listaTipos:
            self.listaTipos.add_node(TreeViewLabel(text=tipo))
        self.add_widget(self.grilla)

class Test(App):
    def build(self):


        configScreen = KivyConfigGui()



        return configScreen

if __name__ == "__main__":
    Test().run()