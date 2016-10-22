from kivy.app import App
from kivy.uix.scatter import Scatter
from KivyComicBook import KivyComicBook

class KivyVisor(App):
    def build(self):
        comic = KivyComicBook("C:\\Users\\pclbu\Pictures\Red Hood and the Outlaws 003 (2016) (2 covers) (Digital) (Zone-Empire).cbr")
        comic.openCbFile()
        scatter = Scatter()
        scatter.add_widget(comic.getPage())
        return Scatter()

if __name__ == "__main__":
    KivyVisor().run()
