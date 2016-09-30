from Serie import Serie
import sqlite3
import codecs
import xml.etree.ElementTree as ET

def testGetSerie(cursor,Id):
    """
    Esto es una prueba de comentario

    """
    print('di para consulta:' + str(Id))
    cursor.execute('''SELECT id,nombre,descripcion,image_url,publisherId,AnioInicio,cantidadNumeros From series where id=?''',(Id,))
        #inner join (select id as pbis,name from publishers )as publishers on series.publisherId = publishers.pbis where id=?''',
        #(Id,))
    r = cursor.fetchone()
    if (r):
        print(r['nombre'])
        '''self.status = 1
        serie = Serie(r['id'], r['nombre'])
        serie.descripcion = r['descripcion']
        serie.image_url = r['image_url']
        serie.publisherId = r['publisherId']
        serie.publisherName = r['name']
        serie.AnioInicio = r['AnioInicio']
        serie.cantidadNumeros = r['cantidadNumeros']
        return serie'''
    else:
        print('Nada')
        return None

def testSeriesTable(cursor):
    #cursor.execute('''INSERT INTO series (id,nombre,descripcion,image_url,publisherId,AnioInicio,cantidadNumeros)
    #Values(1,"test","Test","dsada",1,1,101)''')
    #conn.commit()
    cursor.execute('''SELECT id, nombre, descripcion, image_url,publisherId,AnioInicio, cantidadNumeros, date_added,name From series
                left join (select id as pbis,name from publishers )as publishers on series.publisherId = publishers.pbis  order by date_added''')
    rows = cursor.fetchall()
    for row in rows:
        print(row['nombre'])


def testComicsTable(cursor):
    cursor.execute('''SELECT NombreArchivo,titulo,rowid from comics where path like ?''',('%Flash%',))
    rows = cursor.fetchall()
    for row in rows:
        print(row['rowid'],row['NombreArchivo'])

def testArcosArgumentales(cursor):
    cursor.execute('''select id, nombre, descripcion, ultimaFechaActualizacion from ArcosArgumentales where id = 55766''')
    rows = cursor.fetchall()
    printAllColumns(rows)

def testArcosArgumentalesComics(cursor):
    cursor.execute('''SELECT idComic , idArco, orden , rowid from  ArcosArgumentalesComics ''')
    rows = cursor.fetchall()
    for row in rows:
        print(row['rowid'], row['idArco'], row['idComic'], row['orden'])
def testVineKeys(cursor):
    cursor.execute('''SELECT key from  config_VineKeys''')
    rows = cursor.fetchall()
    for row in rows:
        print(row['id'], row['key'])

def testKeyStatusTable(cursor):
    cursor.execute('''SELECT * from config_VineKeysStatus''')
    rows = cursor.fetchall()
    printAllColumns(rows)

def testPublisherTable(cursor):
    cursor.execute('''SELECT * from Publishers where name like ?''',('%DC%',))
    rows = cursor.fetchall()
    printAllColumns(rows)
    #for row in rows:
    #    print(row['name'],row['id'])

def testQuery(cursor):
    valores = ['superman', 'dc', 'comics']
    cursor.execute('''SELECT id,nombre,descripcion,image_url,publisherId,AnioInicio,cantidadNumeros,name From series inner join (select id as pbis,name from publishers )as publishers
    on series.publisherId = publishers.pbis where nombre like ? and name like ? or name like ?''',valores)
    rows = cursor.fetchall()
    for row in rows:
        print(row['name'], row['id'])
def testListaTable(cursor):
    cursor.execute('''SELECT nombreLista, sublistaDe, descripcion, nombreVista, sqlText from Listas''')
    rows = cursor.fetchall()
    for row in rows:
        print(row['nombreLista'], row['sublistaDe'], row['descripcion'], row['nombreVista'], row['sqlText'])

def printAllColumns(rows):
    if len(rows) > 0:
        titulo = ""
        for columna in rows[0].keys():
            titulo += columna + "      "
        print(titulo)
    for row in rows:
        fila = ""
        for columna in rows[0].keys():
            fila += str(row[columna]) + "|"
        print(fila)
    print("cantidad de filas: "+str(len(rows)))

def alterTableComics(cursor):
    #cursor.execute('''ALTER TABLE  comics ADD COLUMN NombreArchivo text''')
    cursor.execute('''UPDATE comics set NombreArchivo = '' ''')
def testVista(cursor,vista):
    cursor.execute('''SELECT * from '''+vista)
    rows = cursor.fetchall()
    printAllColumns(rows)

def createTables(cursor):
    cursor.execute('''DROP TABLE IF EXISTS series''')
    cursor.execute('''CREATE TABLE series (id text PRIMARY KEY, nombre text, descripcion text, image_url text, publisherId text, AnioInicio text, cantidadNumeros int,date_added integer)''')
    cursor.execute('''DROP TABLE IF EXISTS comics''')
    cursor.execute('''CREATE TABLE comics (path text PRIMARY KEY, titulo text, serieId text, numero int, fechaTapa text, AnioInicio text, volumen text, idExterno text, resumen text, notas text, anio int, mes int, dia int, direccionWeb text, cantidadPaginas int, rating real, ratingExterno real, tipo text, fechaIngresoSistema text, fechaultimaActualizacion text, fechaultimaActualizacionSistemaExterno text)''')

    cursor.execute('''DROP TABLE IF EXISTS config_directorios''')
    cursor.execute('''CREATE TABLE config_Directorios (pathDirectorio text, PRIMARY KEY (pathDirectorio)) ''')
    cursor.execute('''DROP TABLE IF EXISTS config_TipoArchivo''')
    cursor.execute('''CREATE TABLE config_TipoArchivo (tipo text, PRIMARY KEY (tipo)) ''')
    cursor.execute('''DROP TABLE IF EXISTS config_VineKeys''')
    cursor.execute('''CREATE TABLE config_VineKeys (key text, PRIMARY KEY (key)) ''')
    cursor.execute('''DROP TABLE IF EXISTS config_VineKeysStatus''')
    ##  hora en la que se inicia el contador de consultas de vine. Si la diferencia entre fechaUltimaConsulta y fechaInicio es mas de una hora hay que reiniciar el contador de consultas y las fechas
    cursor.execute('''CREATE TABLE config_VineKeysStatus (key text, recurso integer, cantidadTotalConsultas integer, horaUltimaConsulta, PRIMARY KEY (key,recurso)) ''')

    cursor.execute('''DROP TABLE IF EXISTS Publishers''')
    cursor.execute('''CREATE TABLE Publishers (id text, name text, deck text, description text, logoImagePath, PRIMARY KEY (id)) ''')
    cursor.execute('''DROP TABLE IF EXISTS ArcosArgumentales''')
    cursor.execute('''CREATE TABLE ArcosArgumentales (id integer, nombre text, descripcion text,  ultimaFechaActualizacion integer, PRIMARY KEY (id)) ''')
    cursor.execute('''DROP TABLE IF EXISTS ArcosArgumentalesComics''')
    cursor.execute('''CREATE TABLE ArcosArgumentalesComics (idArco integer, idComic integer , orden integer, PRIMARY KEY (idArco,idComic))''')

    cursor.execute('''DROP TABLE IF EXISTS Listas''')
    cursor.execute('''CREATE TABLE Listas (nombreLista text, sublistaDe text, descripcion text, nombreVista text, sqlText text, PRIMARY KEY (nombreLista))''')


conn = sqlite3.connect('BabelComic.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()
#testArcosArgumentales(cur)
# createTables(cur)

testKeyStatusTable(cur)

#testSeriesTable(cur)
#testGetSerie(cur,486667)
#alterTableComics(cur)

#conn.execute('''insert into  listas (nombreLista, sublistaDe,descripcion,nombreVista, sqlText)
#values ('biblioteca', '','','biblioteca','create view biblioteca as select * from comics')''')
# conn.execute('''drop view  IF EXISTS biblioteca''')
#
# conn.execute('''create view biblioteca as select distinct *,comics.rowid as comicRowId from comics as comics
# join series as series on serieId = series.id
# join Publishers on Publishers.id= publisherId
# left join ArcosArgumentalesComics on ArcosArgumentalesComics.idComic = idExterno
# left join ArcosArgumentales on ArcosArgumentales.id = ArcosArgumentalesComics.idArco''')
#
# conn.execute('''drop view  IF EXISTS BlackestNight''')
# conn.execute('''create view BlackestNight as select distinct * from biblioteca
# where [nombre:1] = 'Blackest Night' order by orden''')
#
# testVista(cur,'BlackestNight')

conn.commit()
conn.close()

