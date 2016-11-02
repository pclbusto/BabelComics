import codecs
from BabelComicBookManagerConfig import *
import xml.etree.ElementTree as ET
import sqlite3
from ComicVineSearcher import *



class Publisher():
    def __init__(self,id,name):
        self.id = id
        self.name = name
        self.deck = ""
        self.description=""
        self.logoImagePath=""



class Publishers():
    def __init__(self):
        self.conexion = sqlite3.connect('BabelComic.db')
        self.conexion.row_factory = sqlite3.Row
        self.status = 1
        self.listaComicVineSearch = []
    def add(self,publisher):
        c=self.conexion.cursor()
        c.execute('''INSERT INTO publishers (id, name, deck, description, logoImagePath)
Values(?,?,?,?,?)''', (publisher.id,publisher.name,publisher.deck,publisher.description,publisher.logoImagePath))
        self.conexion.commit()
    def rm(self,Id):
        cursor=self.conexion.cursor()
        cursor.execute('''DELETE From publishers where id=?''', (Id,))
        self.conexion.commit()
    def rmAll(self):
        cursor=self.conexion.cursor()
        cursor.execute('''DELETE From publishers''')
        self.conexion.commit()
    def __loadRowToObject__(self,row):
        Publisher(row['id'], row['name'])
        publisher = Publisher(row['id'], row['name'])
        publisher.descripcion = row['description']
        publisher.deck = row['deck']
        publisher.publisherId = row['logoImagePath']
        return publisher
    def get(self,Id):
        cursor=self.conexion.cursor()
        cursor.execute('''SELECT id, name, deck, description, logoImagePath From publishers where id=?''', (Id,))
        row = cursor.fetchone()
        if (row):
            self.status=1
            return self.__loadRowToObject__(row)
        else:
            self.status=0
            return None


    def update(self,publisher):
        cursor=self.conexion.cursor()
        cursor.execute('''Update publishers set
name=?,description=?,deck=?,logoImagePath=? where id=?''', (publisher.name,publisher.description,publisher.deck, publisher.logoImagePath,publisher.id))
        self.conexion.commit()
    def getSize(self):
        cursor=self.conexion.cursor()
        cursor.execute('''SELECT count * From publishers''')
        cursor.fetchone()
        return(c.fetchone()[0])
    def loadFromFiles(self):
        cursor = self.conexion.cursor()
        entidad = 'publishers'#para hacer match con el nombre del archivo
        lista =[x for x in range(0,76000,100)]
        for off in lista:
            nombreArchivo ='consultaComicVine'+entidad+'-'+str(off)+'.xml'
            print ('procesando archvo: '+nombreArchivo)
##            fr = open(nombreArchivo, 'r')
            fr = codecs.open(nombreArchivo,'r',encoding='utf-8', errors='ignore')
            xml = fr.read()
            fr.close()
            root = ET.fromstring(xml)
            results = root.find('results')
            for item in results:
                publisher = Publisher(item.find('id').text, item.find('name').text)
                publisher.descripcion = item.find('description').text
                publisher.deck = item.find('deck').text
                if item.find('image').find('super_url')!=None:
                    publisher.logoImagePath = item.find('image').find('super_url').text
                else:
                    publisher.logoImagePath = ''
                self.add(publisher)
            print('procesados: '+str(off)+' de '+str(10000))
            self.conexion.commit()
    def getList(self,valores,filtro=None,orden=None):
        c=self.conexion.cursor()
        if not orden: orden=''
        if filtro!='':
            c.execute('''SELECT id, name, deck, description, logoImagePath From publishers where '''+filtro+' '+orden, valores)
        else:
            c.execute('''id, name, deck, description, logoImagePath From publishers'''+' '+orden)
        rows=c.fetchall()
        lista=[]
        for row in rows:
            publisher = self.__loadRowToObject__(row)
            lista.append(publisher)
        print(len(lista))
        return lista

    def getNext(self, campo='id'):
        print('falta implementar')

    def close(self):
        self.conexion.close()

    def searchInComicVineComicVine(self, filtro):
        config = BabelComicBookManagerConfig()
        clave = config.getClave('publishers')
        comic_searcher = ComicVineSearcher(clave)
        comic_searcher.setEntidad('publishers')
        comic_searcher.addFilter("name:"+filtro.replace(" ","%20"))
        comic_searcher.vineSearch(0)
        self.listaComicVineSearch = comic_searcher.listaBusquedaVine

        #for publisher in comic_searcher.listaBusquedaVine:
        #    print(publisher.name)
            #self.add(serie)
        #print('porcentaje completado: ' + str((100 * (len(lista_series) / comic_searcher.cantidadResultados))))


if __name__ == "__main__":


##67600 dio error
##67700 dio error
    publishers = Publishers()
    p = Publisher(12134,"pedro")
    publishers.searchInComicVineComicVine("Marvel")

##    publishers.rmAll()
##    series.loadFromFiles()
##    series.rmAll()
##    publisher = Publisher('0','Sin Editoriaasa')
##    publishers.add(publisher)
##    series.rm('-1')
##    series.add(serie)
    for publisher in publishers.getList(("0",),'id = ?'):
        print(publisher.name,publisher.id)
    publishers.close()
    print(p)