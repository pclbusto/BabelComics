import sqlite3

'''

configuracion->lista de directorios
    \
     \
      \->lista de extensiones
esta clase gestiona todo. mas alla que use tres tablas.
la tabla principal no tiene ningun atributo por ahora
se deja por uso futuo cuando surjan necesidades.


'''


class BabelComicBookManagerConfig():
    def __init__(self):
        self.conexion = sqlite3.connect('BabelComic.db')
        self.conexion.row_factory = sqlite3.Row
        self.listaTipos = []
        self.listaDirectorios = []
        self.listaClaves = []

        cursor = self.conexion.cursor()
        # recuperamos la lista de tipos
        cursor.execute('''SELECT tipo From config_TipoArchivo where id=?''', (1,))
        rows = cursor.fetchall()
        for row in rows:
            self.listaTipos.append(row['tipo'])
        # recuperamos la lista de directorios
        cursor.execute('''SELECT pathDirectorio From config_Directorios where id=?''', (1,))
        rows = cursor.fetchall()
        for row in rows:
            self.listaDirectorios.append(row['pathDirectorio'])
        # recuperamos la lista de claves
        cursor.execute('''SELECT key  From config_VineKeys where id=?''', (1,))
        rows = cursor.fetchall()
        for row in rows:
            print(row['key'])
            self.listaClaves.append(row['key'])

    def addClave(self, clave):
        cursor = self.conexion.cursor()
        cursor.execute('''INSERT INTO config_VineKeys (id,key) values (?,?)''', (1, clave,))
        self.listaClaves.append(clave)
        self.conexion.commit()

    def addTipo(self, tipo):
        cursor = self.conexion.cursor()
        cursor.execute('''INSERT INTO config_TipoArchivo (id,tipo) values (?,?)''', (1, tipo,))
        self.listaTipos.append(tipo)
        self.conexion.commit()

    def addDirectorio(self, directorio):
        cursor = self.conexion.cursor()
        cursor.execute('''INSERT INTO config_Directorios (id,pathDirectorio) values (?,?)''', (1, directorio,))
        self.listaDirectorios.append(directorio)
        self.conexion.commit()

    def __delAllTipos__(self):
        cursor = self.conexion.cursor()
        cursor.execute('''DELETE FROM config_TipoArchivo''')
        self.conexion.commit()
        self.listaTipos = []

    def __delAllDirectorios__(self):
        cursor = self.conexion.cursor()
        cursor.execute('''DELETE FROM config_Directorios''')
        self.conexion.commit()
        self.listaDirectorios = []

    def __delAllClaves__(self):
        cursor = self.conexion.cursor()
        cursor.execute('''DELETE FROM config_VineKeys''')
        self.conexion.commit()
        self.listaClaves = []

    def setListaTipos(self, listaTipos=[]):
        self.__delAllTipos__()
        for tipo in listaTipos:
            self.addTipo(tipo)

    def delClave(self, clave):
        cursor = self.conexion.cursor()
        cursor.execute('''DELETE FROM config_VineKeys WHERE key=?''', (clave,))
        self.listaClaves.remove(clave)
        self.conexion.commit()

    def delTipo(self, tipo):
        cursor = self.conexion.cursor()
        cursor.execute('''DELETE FROM config_TipoArchivo WHERE tipo=?''', (tipo,))
        self.listaTipos.remove(tipo)
        self.conexion.commit()

    def delDirectorio(self, directorio):
        cursor = self.conexion.cursor()
        cursor.execute('''DELETE FROM config_Directorios WHERE pathDirectorio=?''', (directorio,))
        self.listaDirectorios.remove(directorio)
        self.conexion.commit()

    def setListaDirectorios(self, listaDirectorios=[]):
        self.__delAllDirectorios__()
        for directorio in listaDirectorios:
            self.addDirectorio(directorio)

    def setListaClaves(self, listaClaves=[]):
        self.__delAllClaves__()
        for clave in listaClaves:
            self.addClave(clave)

    def getClave(self):
        return self.listaClaves[0]


if __name__ == "__main__":
    config = BabelComicBookManagerConfig()
    ##    config.addClave('64f7e65686c40cc016b8b8e499f46d6657d26752')
    ##    config.addClave('7e4368b71c5a66d710a62e996a660024f6a868d4')
    ##    config.addDirectorio('c:\\Users\\bustoped\\Downloads\\Comics\\')
    ##    config.delDirectorio('c:\\Users\\bustoped\\Downloads\\Comics\\')
    ##    config.addTipo('cbz')
    cursor = config.conexion.cursor()

    ##    config.delTipo('cb7')
    ##    config.delDirectorio('home')
    for dire in config.listaClaves:
        print(dire)
##    config.addTipo('cb7')


