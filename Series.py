import codecs
import xml.etree.ElementTree as ET
import sqlite3
from Serie import Serie
from BabelComicBookManagerConfig import  BabelComicBookManagerConfig
#importamos ComicVineSearcher para poder hacer la rutina que cargue datos desde comicvine
from ComicVineSearcher import *

class Series:
    def __init__(self):
        self.conexion = sqlite3.connect('BabelComic.db')
        self.conexion.row_factory = sqlite3.Row
        self.status = 1

    def add(self, serie):
        c = self.conexion.cursor()
        c.execute('''INSERT INTO series (id,nombre,descripcion,image_url,publisherId,AnioInicio,cantidadNumeros)
Values(?,?,?,?,?,?,?)''', (
        serie.id, serie.nombre, serie.descripcion, serie.image_url, serie.publisherId, serie.AnioInicio,
        serie.cantidadNumeros))
        self.conexion.commit()
        print('insertamos')

    def rm(self, Id):
        cursor = self.conexion.cursor()
        cursor.execute('''DELETE From series where id=?''', (Id,))
        self.conexion.commit()

    def rmAll(self):
        cursor = self.conexion.cursor()
        cursor.execute('''DELETE From series''')
        self.conexion.commit()

    def get(self, Id):
        cursor = self.conexion.cursor()
        cursor.execute(
            '''SELECT id,nombre,descripcion,image_url,publisherId,AnioInicio,cantidadNumeros,name From series inner join (select id as pbis,name from publishers )as publishers on series.publisherId = publishers.pbis where id=?''',
            (Id,))
        r = cursor.fetchone()
        if (r):
            self.status = 1
            serie = Serie(r['id'], r['nombre'])
            serie.descripcion = r['descripcion']
            serie.image_url = r['image_url']
            serie.publisherId = r['publisherId']
            serie.publisherName = r['name']
            serie.AnioInicio = r['AnioInicio']
            serie.cantidadNumeros = r['cantidadNumeros']
            return serie
        else:
            self.status = 0
            return None

    def update(self, serie):
        cursor = self.conexion.cursor()
        cursor.execute('''Update series set
nombre=?,descripcion=?,image_url=?,publisherId=?,AnioInicio=?,cantidadNumeros=?
where id=?''', (
        serie.nombre, serie.descripcion, serie.image_url, serie.publisherId, serie.AnioInicio, serie.cantidadNumeros,
        serie.id))
        self.conexion.commit()

    def getSize(self):
        cursor = self.conexion.cursor()
        cursor.execute('''SELECT count * From series''')
        cursor.fetchone()
        return (c.fetchone()[0])

    def loadFromFiles(self):
        cursor = self.conexion.cursor()
        entidad = 'volumes'  # para hacer match con el nombre del archivo
        lista = [x for x in range(0, 76000, 100)]
        for off in lista:
            nombreArchivo = 'consultaComicVine' + entidad + '-' + str(off) + '.xml'
            print('procesando archvo: ' + nombreArchivo)
            ##            fr = open(nombreArchivo, 'r')
            fr = codecs.open(nombreArchivo, 'r', encoding='utf-8', errors='ignore')
            xml = fr.read()
            fr.close()
            root = ET.fromstring(xml)
            results = root.find('results')
            for item in results:
                serie = Serie(item.find('id').text, item.find('name').text)
                serie.cantidadNumeros = int(item.find('count_of_issues').text)
                serie.descripcion = item.find('description').text
                if item.find('image').find('super_url') != None:
                    serie.image_url = item.find('image').find('super_url').text
                else:
                    serie.image_url = ''
                if item.find('publisher').find('id') != None:
                    serie.publisherId = item.find('publisher').find('id').text
                else:
                    serie.publisherId = '-1'
                serie.AnioInicio = item.find('start_year').text
                cursor.execute('''INSERT INTO series (id,nombre,descripcion,image_url,publisherId,AnioInicio,cantidadNumeros)
Values(?,?,?,?,?,?,?)''', (
                serie.id, serie.nombre, serie.descripcion, serie.image_url, serie.publisherId, serie.AnioInicio,
                serie.cantidadNumeros))
            print('procesados: ' + str(off) + ' de ' + str(10000))
            self.conexion.commit()

    def getList(self, valores, filtro=None, orden=None):
        c = self.conexion.cursor()
        if not orden: orden = ''
        if filtro:
            # print('''SELECT id,nombre,descripcion,image_url,publisherId,AnioInicio,cantidadNumeros,name From series inner join (select id as pbis,name from publishers )as publishers on series.publisherId = publishers.pbis where '''+filtro+' '+orden)
            # print(valores)
            c.execute(
                '''SELECT id,nombre,descripcion,image_url,publisherId,AnioInicio,cantidadNumeros,name From series inner join (select id as pbis,name from publishers )as publishers on series.publisherId = publishers.pbis where ''' + filtro + ' ' + orden,
                valores)
        else:
            c.execute(
                '''SELECT id,nombre,descripcion,image_url,publisherId,AnioInicio,cantidadNumeros,name From series
                left join (select id as pbis,name from publishers )as publishers on series.publisherId = publishers.pbis ''' + ' ' + orden)

        rows = c.fetchall()
        lista = []
        for row in rows:
            serie = Serie(row['id'], row['nombre'])
            serie.descripcion = row['descripcion']
            serie.image_url = row['image_url']
            serie.publisherId = row['publisherId']
            serie.publisherName = row['name']
            serie.AnioInicio = row['AnioInicio']
            serie.cantidadNumeros = row['cantidadNumeros']
            lista.append(serie)
        print(len(lista))
        return lista

    def getNext(self, campo='id'):
        cursor = self.conexion.cursor()
        return None

    def close(self):
        self.conexion.close()
    def loadDataFromComicVine(self):
        config = BabelComicBookManagerConfig()
        cv = ComicVineSearcher(config.getClave())
        cv.setEntidad('volumes')
        cv.vineSearch()
        for serie in cv.listaBusquedaVine:
            self.add(serie)


if __name__ == "__main__":

    ##67600 dio error
    ##67700 dio error
    series = Series()
    #series.rmAll()
    #series.loadDataFromComicVine()
    ##
    ##    series.loadFromFiles()
    ##    series.rmAll()
    ##    serie = Serie('-1','No especificada')
    ##    series.rm('-1')
    ##    series.add(serie)
    ##   for serie in series.getList(("-1",),'id = ?'):
    for serie in series.getList(''):
        print(serie.nombre, serie.id)
    series.close()
