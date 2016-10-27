from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Label, Button
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from zipfile import ZipFile
from io import BytesIO

class MemoryImage(Image):
    """Display an image already loaded in memory."""
    memory_data = ObjectProperty(None)

    def __init__(self,memoryFile, ext, **kwargs):
        super(MemoryImage, self).__init__(**kwargs)
        data = BytesIO(memoryFile.read())
        im = CoreImage(data,ext=ext)
        print(ext)
        with self.canvas:
            self.texture = im.texture




