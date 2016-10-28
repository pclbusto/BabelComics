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
        with self.canvas:
            self.texture = im.texture




