import os
from datetime import datetime

from PyQt6 import QtSql, QtWidgets, QtGui, QtCore

import alquileres
import conexion
import eventos
import propiedades
import var
from eventos import Eventos
from facturas import Facturas


class Conexion:
    '''
    @staticmethod
    método de una clase que no depende de una instancia específica de esa clase.
    Se puede llamarlo directamente a través de la clase, sin necesidad de crear un objeto de esa clase.
    Es útil en comportamientos o funcionalidades que son más a una clase en general que a una instancia en particular.
    '''

    @staticmethod
    def db_conexion():
        """

        :return: conexion con la base de datos.
        :rtype: bool

        Método para establecer conexión con la base de datos
        Si éxito devuelve True, en caso contrario devuelve False.

        """
        # Verifica si el archivo de base de datos existe
        if not os.path.isfile('bbdd.sqlite'):
            eventos.Eventos.crearMensajeError("Error", 'El archivo de la base de datos no existe.')
            return False

        # Crear la conexión con la base de datos SQLite
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('bbdd.sqlite')

        if db.open():
            # Verificar si la base de datos contiene tablas
            query = QtSql.QSqlQuery()
            query.exec("SELECT name FROM sqlite_master WHERE type='table';")

            if not query.next():  # Si no hay tablas
                eventos.Eventos.crearMensajeError("Error", "Base de datos vacía o no válida.")
                return False

            else:
                eventos.Eventos.crearMensajeInfo("Aviso", "Conexión a la Base de Datos realizada")
                return True

        else:
            eventos.Eventos.crearMensajeError("Error", "No se pudo abrir la base de datos.")
            return False

    '''
    GESTION DE CLIENTES
    '''

    @staticmethod
    def listaProv():
        """

        :return: lista de provincias
        :rtype: list

        Método que devuelve la lista de provincias

        """
        listaprov = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")
        if query.exec():
            while query.next():
                listaprov.append(query.value(1))
        return listaprov

    @staticmethod
    def listaMunicipio(provincia):
        """

        :param provincia: nombre de la provincia
        :type provincia: str
        :return: lista de municipios de una provincia
        :rtype: list

        Método que devuelve todos los municipios de una provincia

        """
        try:
            listamunicipio = []
            query = QtSql.QSqlQuery()
            query.prepare(
                "SELECT * FROM municipios WHERE idprov = (SELECT idprov FROM provincias WHERE provincia = :provincia)")
            query.bindValue(":provincia", provincia)
            if query.exec():
                while query.next():
                    listamunicipio.append(query.value(1))
            return listamunicipio
        except Exception as e:
            print("error al cargar municipios")

    @staticmethod
    def altaCliente(nuevocli):
        """

        :param nuevocli: lista de datos del cliente
        :type nuevocli: list
        :return: éxito en la creación de un cliente
        :rtype: bool

        Método que inserta datos cliente en la base de datos

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "INSERT into clientes (dnicli, altacli, apelcli, nomecli, emailcli, movilcli, dircli, provcli, municli) values (:dnicli, :altacli, :apelcli, :nomecli, :emailcli, :movilcli, :dircli, :provcli, :municli)")
            query.bindValue(":dnicli", str(nuevocli[0]))
            query.bindValue(":altacli", str(nuevocli[1]))
            query.bindValue(":apelcli", str(nuevocli[2]))
            query.bindValue(":nomecli", str(nuevocli[3]))
            query.bindValue(":emailcli", str(nuevocli[4]))
            query.bindValue(":movilcli", str(nuevocli[5]))
            query.bindValue(":dircli", str(nuevocli[6]))
            query.bindValue(":provcli", str(nuevocli[7]))
            query.bindValue(":municli", str(nuevocli[8]))

            if query.exec():
                return True
            else:
                return False

        except Exception as e:
            print("Error alta cliente", e)

    @staticmethod
    def listadoClientes():
        """

        :return: devuelve la lista de clientes
        :rtype: list

        Método que devuelve el listado total de clientes de la base de datos

        """
        try:
            listado = []
            historico = var.ui.chkHistoriacli.isChecked()
            if historico:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM clientes ORDER BY apelcli, nomecli ASC")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)

            else:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM clientes WHERE bajacli is null ORDER BY apelcli, nomecli ASC")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
            return listado
        except Exception as e:
            print("Error al listar clientes")

    @staticmethod
    def datosOneCliente(dni):
        """

        :param dni: dni de un cliente
        :type dni: str
        :return: datos de un cliente
        :rtype: list

        Método que devuelve los datos de un cliente al introducir su dni

        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM clientes WHERE dnicli = :dni")
            query.bindValue(":dni", str(dni))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as e:
            print("Error al cargar UN cliente en la tabla.", e)

    @staticmethod
    def modifCliente(registro):
        """

        :param registro: datos de un cliente
        :type registro: list
        :return: éxito en la modificación de detos de un cliente
        :rtype: bool

        Método que modifica los datos de un cliente en la base de datos

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from clientes where dnicli = :dni")
            query.bindValue(":dni", str(registro[0]))
            if query.exec() and query.next():
                count = query.value(0)
                if count == 1:  # verificamos que solo nos devuelve un resultado, la fila para el dni que buscamos

                    query.prepare(
                        "UPDATE clientes set altacli= :altacli, apelcli = :apelcli, nomecli= :nomecli, emailcli = :emailcli, movilcli = :movilcli, dircli = :dircli, provcli=:provcli, municli=:municli, bajacli = :bajacli WHERE dnicli = :dni")
                    query.bindValue(":dni", str(registro[0]))
                    query.bindValue(":altacli", str(registro[1]))
                    query.bindValue(":apelcli", str(registro[2]))
                    query.bindValue(":nomecli", str(registro[3]))
                    query.bindValue(":emailcli", str(registro[4]))
                    query.bindValue(":movilcli", str(registro[5]))
                    query.bindValue(":dircli", str(registro[6]))
                    query.bindValue(":provcli", str(registro[7]))
                    query.bindValue(":municli", str(registro[8]))
                    if registro[9] == "":
                        query.bindValue(":bajacli", QtCore.QVariant())  # QVariant añade un null a la BD
                    else:
                        query.bindValue(":bajacli", str(registro[9]))

                    if query.exec():
                        return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            print("Error al modificar un cliente en conexion.", e)

    @staticmethod
    def bajaCliente(dni):
        """

        :param dni: dni de un cliente
        :type dni: str
        :return: éxito al dar de baja a un cliente
        :rtype: bool

        Método que añade fecha de baja a un cliente

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT COUNT(*) from clientes where dnicli = :dni")
            query.bindValue(":dni", str(dni))
            if query.exec() and query.next():
                count = query.value(0)
                if count == 1:
                    query.prepare("UPDATE clientes SET bajacli = :bajacli WHERE dnicli = :dni")
                    query.bindValue(":bajacli", datetime.now().strftime("%d/%m/%Y"))
                    query.bindValue(":dni", str(dni))
                    if query.exec():
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        except Exception as e:
            print("Error en la conexión al dar de baja cliente", e)

    '''
    GESTION DE PROPIEDADES
    '''

    @staticmethod
    def cargarMunicipios():
        try:
            listaMuni = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM MUNICIPIOS")
            if query.exec():
                while query.next():
                    listaMuni.append(query.value(1))
                return listaMuni
        except Exception as e:
            print('Error cargando municipios')

    @staticmethod
    def cargarTipoprop():
        """

        :return: todos los tipos de propiedad
        :rtype: list

        Método que devuelve todos los tipos de propiedad almacenados en la bd

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT tipo from tipopropiedad ")
            if query.exec():
                registro = []
                while query.next():
                    registro.append(str(query.value(0)))
                return registro
        except Exception as e:
            print("error cargando tipos de propiedad", e)

    @staticmethod
    def altaTipoprop(tipo):
        """

        :param tipo: nuevo tipo de propiedad
        :type tipo: str
        :return: tipos de propiedad
        :rtype: list

        Método que introduce un nuevo tipo de propiedad y devuelve la lista de tipos de propiedad

        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("INSERT into tipopropiedad (tipo) values (:tipo) ")
            query.bindValue(":tipo", str(tipo))
            if query.exec():
                registro = Conexion.cargarTipoprop()
                return registro
            else:
                return registro
        except Exception as e:
            print("Error en conexion al dar de alta tipo propiedad", e)

    @staticmethod
    def bajaTipoprop(tipo):
        """

        :param tipo: tipo de propiedad
        :type tipo: str
        :return: éxito o no en la eliminación de un tipo de propiedad
        :rtype: bool

        Método que elimina un tipo de propiedad

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE from tipopropiedad where tipo = :tipo ")
            query.bindValue(":tipo", str(tipo))
            if query.exec() and query.numRowsAffected() == 1:
                return True
            else:
                return False
        except Exception as e:
            print("Error en conexion al dar de baja tipo propiedad", e)

    @staticmethod
    def altaPropiedad(propiedad):
        """

        :param propiedad: datos de una propiedad
        :type propiedad: list
        :return: éxito al introducir propiedad en la base de datos
        :rtype: bool

        Método que introduce una nueva propiedad en la base de datos

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "INSERT into propiedades (alta,direccion,provincia,municipio,tipo_propiedad,num_habitaciones,num_banos,superficie,precio_alquiler,precio_venta,codigo_postal,descripcion,tipo_operacion,estado,nombre_propietario,movil) values (:alta,:direccion,:provincia,:municipio,:tipo_propiedad,:num_habitaciones,:num_banos,:superficie,:precio_alquiler,:precio_venta,:codigo_postal,:descripcion,:tipo_operacion,:estado,:nombre_propietario,:movil) ")
            query.bindValue(":alta", str(propiedad[0]))
            query.bindValue(":direccion", str(propiedad[1]))
            query.bindValue(":provincia", str(propiedad[2]))
            query.bindValue(":municipio", str(propiedad[3]))
            query.bindValue(":tipo_propiedad", str(propiedad[4]))
            query.bindValue(":num_habitaciones", str(propiedad[5]))
            query.bindValue(":num_banos", str(propiedad[6]))
            query.bindValue(":superficie", str(propiedad[7]))
            query.bindValue(":precio_alquiler", str(propiedad[8]))
            query.bindValue(":precio_venta", str(propiedad[9]))
            query.bindValue(":codigo_postal", str(propiedad[10]))
            query.bindValue(":descripcion", str(propiedad[11]))
            query.bindValue(":tipo_operacion", str(propiedad[12]))
            query.bindValue(":estado", str(propiedad[13]))
            query.bindValue(":nombre_propietario", str(propiedad[14]))
            query.bindValue(":movil", str(propiedad[15]))

            if query.exec():
                return True
            else:
                return False


        except Exception as e:
            print("Error al dar de alta propiedad en conexion", e)

    @staticmethod
    def modifProp(propiedad):
        """

        :param propiedad: datos de propiedad
        :type propiedad: list
        :return: éxito en la modificación de los datos de una propiedad
        :rtype: bool

        Método que modifica los datos de propiedad en la base de datos

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from propiedades where codigo = :codigo")
            query.bindValue(":codigo", propiedad[0])
            if query.exec() and query.next():
                count = query.value(0)
                if count == 1:  # verificamos que solo nos devuelve un resultado, la fila para el codigo que buscamos

                    query.prepare(
                        "UPDATE propiedades set alta = :alta, baja = :baja, direccion = :direccion, municipio = :municipio, provincia = :provincia, tipo_propiedad = :tipo_propiedad, num_habitaciones=:num_habitaciones, num_banos = :num_banos, superficie = :superficie, precio_alquiler = :precio_alquiler, precio_venta = :precio_venta, codigo_postal = :codigo_postal, descripcion = :descripcion, tipo_operacion = :tipo_operacion, estado=:estado, nombre_propietario =:nombre_propietario, movil =:movil WHERE codigo = :codigo")
                    query.bindValue(":codigo", str(propiedad[0]))
                    query.bindValue(":alta", str(propiedad[1]))
                    query.bindValue(":direccion", str(propiedad[3]))
                    query.bindValue(":provincia", str(propiedad[4]))
                    query.bindValue(":municipio", str(propiedad[5]))
                    query.bindValue(":tipo_propiedad", str(propiedad[6]))
                    query.bindValue(":num_habitaciones", str(propiedad[7]))
                    query.bindValue(":num_banos", str(propiedad[8]))
                    query.bindValue(":superficie", str(propiedad[9]))
                    query.bindValue(":precio_alquiler", str(propiedad[10]))
                    query.bindValue(":precio_venta", str(propiedad[11]))
                    query.bindValue(":codigo_postal", str(propiedad[12]))
                    query.bindValue(":descripcion", str(propiedad[13]))
                    query.bindValue(":tipo_operacion", str(propiedad[14]))
                    query.bindValue(":estado", str(propiedad[15]))
                    query.bindValue(":nombre_propietario", str(propiedad[16]))
                    query.bindValue(":movil", str(propiedad[17]))
                    if propiedad[2] == "":
                        query.bindValue(":baja", QtCore.QVariant())  # QVariant añade un null a la BD
                    else:
                        query.bindValue(":baja", str(propiedad[2]))

                    if query.exec():
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

        except Exception as e:
            print("Error al modificar propiedad en conexión.", e)

    @staticmethod
    def bajaProp(propiedad):
        """

        :param propiedad: datos de una propiedad
        :type propiedad: list
        :return: éxito al dar de baja a una propiedad
        :rtype: bool
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from propiedades where codigo = :codigo")
            query.bindValue(":codigo", propiedad[0])
            if query.exec() and query.next():
                count = query.value(0)
                if count == 1:  # verificamos que solo nos devuelve un resultado a consulta, por tanto la propiedad existe.
                    query.prepare("update propiedades set baja =:baja, estado =:estado where codigo = :codigo ")
                    query.bindValue(":codigo", str(propiedad[0]))
                    query.bindValue(":baja", str(propiedad[
                                                     2]))  # dejamos el segundo espacio del array para fecha de alta, y comprobar mas tarde que no sea posterior a fecha de baja
                    query.bindValue(":estado", str(propiedad[3]))
                    if query.exec():
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

        except Exception as e:
            print("Error al dar de baja propiedad en conexión.", e)

    @staticmethod
    def listadoPropiedades():
        """

        :return: datos filtrados de todas las propiedades
        :rtype: list
        """
        try:
            listado = []
            historico = var.ui.chkHistoriaprop.isChecked()
            municipio = var.ui.cmbMuniprop.currentText()
            filtrado = var.ui.btnBuscaTipoProp.isChecked()
            tipoSeleccionado = var.ui.cmbTipoprop.currentText()

            base_query = "SELECT * FROM propiedades"
            condiciones = []
            parametros_bind = {}

            if not historico:
                condiciones.append("baja is NULL")
            if filtrado:
                condiciones.append("tipo_propiedad = :tipo_propiedad")
                parametros_bind[":tipo_propiedad"] = tipoSeleccionado
                condiciones.append("municipio = :municipio")
                parametros_bind[":municipio"] = municipio
            elif not historico:
                condiciones.append("estado = 'Disponible'")

            if condiciones:
                base_query += " WHERE " + " AND ".join(condiciones)
            base_query += " ORDER BY municipio ASC"

            query = QtSql.QSqlQuery()
            query.prepare(base_query)
            for clave, valor in parametros_bind.items():
                query.bindValue(clave, valor)

            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)

            return listado

        except Exception as e:
            print("Error al listar propiedades en listadoPropiedades", e)

    @staticmethod
    def datosOnePropiedad(codigo):
        """

        :param codigo: codigo de propiedad
        :type codigo: int
        :return: datos de una propiedad
        :rtype: list
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM propiedades WHERE codigo = :codigo")
            query.bindValue(":codigo", str(codigo))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as e:
            print("Error al cargar UNA propiedad en conexion.", e)

    @staticmethod
    def cargarAllPropiedadesBD():
        """

        :return: datos de todas las propiedades
        :rtype: list

        Método que devuelve los datos de todas las propiedades almacenadasen la BD

        """
        try:
            listado = []

            base_query = "SELECT * FROM propiedades ORDER BY municipio ASC"

            query = QtSql.QSqlQuery()
            query.prepare(base_query)

            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)

            return listado

        except Exception as e:
            print("Error al listar propiedades en cargarAllpropiedades", e)

    '''
    GESTION DE VENDEDORES
    '''

    @staticmethod
    def altaVendedor(nuevoVendedor):
        """

        :param nuevoVendedor: datos de un vendedor
        :type nuevoVendedor: list
        :return: éxito en añadir a un vendedor a la base de datos
        :rtype: bool

        Método que añade un nuevo vendedor a la base de datos

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "INSERT into vendedores (dniVendedor,nombreVendedor,altaVendedor,movilVendedor,mailVendedor,delegacionVendedor) values (:dniVendedor, :nombreVendedor, :altaVendedor, :movilVendedor, :mailVendedor, :delegacionVendedor)")
            query.bindValue(":dniVendedor", str(nuevoVendedor[0]))
            query.bindValue(":nombreVendedor", str(nuevoVendedor[1]))
            query.bindValue(":altaVendedor", str(nuevoVendedor[2]))
            query.bindValue(":movilVendedor", str(nuevoVendedor[3]))
            query.bindValue(":mailVendedor", str(nuevoVendedor[4]))
            query.bindValue(":delegacionVendedor", str(nuevoVendedor[5]))

            if query.exec():
                return True
            else:
                return False

        except Exception as e:
            print("Error alta vendedor en conexion", e)

    @staticmethod
    def datosOneVendedor(valor, tipo_busqueda="idVendedor"):
        """

        :param valor: valor del tipo de búsqueda que se introduzca introducida
        :type valor: object
        :param tipo_busqueda: nombre de la columna de bd por la que se va a realizar la búsqueda
        :type tipo_busqueda: str
        :return: datos de un vendedor
        :rtype: list

        Método que devuelve los datos de un vendedor en función de un parámetro de búsqueda, siendo su id el predeterminado

        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM vendedores WHERE " + tipo_busqueda + " = :valor")
            query.bindValue(":valor", str(valor))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as e:
            print("Error al cargar UN cliente en la tabla.", e)

    @staticmethod
    def listadoVendedores():
        """

        :return: datos de vendedores
        :rtype: list

        Método que devuelve la lista de vendedores

        """
        try:
            listado = []
            historico = var.ui.chkHistoriaVen.isChecked()
            if historico:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM vendedores ORDER BY idVendedor ASC")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)

            else:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM vendedores WHERE bajaVendedor is null ORDER BY idVendedor ASC")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
            return listado
        except Exception as e:
            print("Error al listar vendedores")

    @staticmethod
    def listadoFacturas():
        """
            Devuelve el listado de todas las facturas.

            Procedimiento:
            1. Prepara y ejecuta una consulta SQL para obtener todas las facturas ordenadas por ID.
            2. Recorre los resultados de la consulta y los añade a una lista.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de obtención de datos.

            @param None
            @return list: Lista de todas las facturas.
            """
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM facturas ORDER BY id ASC")
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("Error al listar facturas")

    @staticmethod
    def bajaVendedor(dni):
        """

        :param dni: dni de un vendedor
        :type dni: str
        :return: éxito al dar de baja a un vendedor en la base de datos
        :rtype: bool

        Método que añade una fecha de baja al vendedor

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT COUNT(*) from vendedores where dniVendedor = :dni")
            query.bindValue(":dni", str(dni))
            if query.exec() and query.next():
                count = query.value(0)
                if count == 1:
                    query.prepare("UPDATE vendedores SET bajaVendedor = :bajaVendedor WHERE dniVendedor = :dni")
                    query.bindValue(":bajaVendedor", datetime.now().strftime("%d/%m/%Y"))
                    query.bindValue(":dni", str(dni))
                    if query.exec():
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        except Exception as e:
            print("Error en la conexión al dar de baja vendedor", e)

    @staticmethod
    def modifVendedor(registro):
        """

        :param registro: datos de vendedor
        :type registro: list
        :return: éxito al modificar datos de vendedor en la base de datos
        :rtype: bool

        Método que modifica los datos de un vendedor en la base de datos

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from vendedores where idVendedor = :id")
            query.bindValue(":id", str(registro[0]))
            if query.exec() and query.next():
                count = query.value(0)
                if count == 1:  # verificamos que solo nos devuelve un resultado, la fila para el dni que buscamos

                    query.prepare(
                        "UPDATE vendedores set nombreVendedor= :nombreVendedor, altaVendedor = :altaVendedor, bajaVendedor= :bajaVendedor, movilVendedor = :movilVendedor, mailVendedor = :mailVendedor, delegacionVendedor = :delegacionVendedor WHERE idVendedor = :id")
                    query.bindValue(":id", str(registro[0]))
                    query.bindValue(":nombreVendedor", str(registro[1]))
                    query.bindValue(":altaVendedor", str(registro[2]))
                    query.bindValue(":movilVendedor", str(registro[3]))
                    query.bindValue(":mailVendedor", str(registro[4]))
                    query.bindValue(":delegacionVendedor", str(registro[5]))
                    if registro[6] == "":
                        query.bindValue(":bajaVendedor", QtCore.QVariant())  # QVariant añade un null a la BD
                    else:
                        query.bindValue(":bajaVendedor", str(registro[6]))

                    if query.exec():
                        return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            print("Error al modificar un vendedor en conexion.", e)

    @staticmethod
    def cargarAllVendedoresBD():
        """

        :return: datos de todos los vendedores
        :rtype: list

        Método que devuelve todos los datos de los vendedores en la base de datos

        """
        try:
            listado = []

            base_query = "SELECT * FROM vendedores ORDER BY idVendedor ASC"

            query = QtSql.QSqlQuery()
            query.prepare(base_query)

            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)

            return listado

        except Exception as e:
            print("Error al listar vendedores en cargarAllpropiedades", e)

    '''
    GESTION DE FACTURAS
    '''

    @staticmethod
    def altaFactura(registro):
        """
            Añade una nueva factura a la base de datos.

            Procedimiento:
            1. Prepara y ejecuta una consulta SQL para insertar una nueva factura con la fecha y el DNI del cliente.
            2. Devuelve True si la inserción es exitosa, de lo contrario devuelve False.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de inserción de la factura.

            @param registro: Lista con los datos de la factura. El primer elemento es la fecha de la factura y el segundo es el DNI del cliente.
            @type registro: list
            @return: Éxito de la inserción de la factura.
            @rtype: bool
            """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO FACTURAS (fechafac, dnicli) values (:fechafac,:dnicli)")
            query.bindValue(":fechafac", str(registro[0]))
            query.bindValue(":dnicli", str(registro[1]))

            if query.exec():
                return True
            else:
                return False

        except Exception as e:
            print("Error al dar de alta factura en conexion.", e)

    @staticmethod
    def eliminarFactura(id):
        """
           Elimina una factura de la base de datos.

           Procedimiento:
           1. Prepara y ejecuta una consulta SQL para eliminar una factura por su ID.
           2. Devuelve True si la eliminación es exitosa, de lo contrario devuelve False.

           Excepciones:
           - Captura y muestra cualquier excepción que ocurra durante el proceso de eliminación de la factura.

           @param id: ID de la factura a eliminar.
           @type id: int
           @return: Éxito de la eliminación de la factura.
           @rtype: bool
           """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM facturas WHERE id = :id")
            query.bindValue(":id", id)
            if query.exec() and query.numRowsAffected() == 1:
                return True
            else:
                return False
        except Exception as e:
            print("Error al eliminar factura en conexion.", e)
            return False

    @staticmethod
    def altaVenta(registro):
        """
            Añade una nueva venta a la base de datos.

            Procedimiento:
            1. Prepara y ejecuta una consulta SQL para insertar una nueva venta con los datos proporcionados.
            2. Si la inserción es exitosa, actualiza el estado de la propiedad a 'Vendido' y establece la fecha de baja.
            3. Devuelve True si la inserción y la actualización son exitosas, de lo contrario devuelve False.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de inserción de la venta.

            @param registro: Lista con los datos de la venta. El primer elemento es el ID de la factura, el segundo es el código de la propiedad y el tercero es el ID del agente.
            @type registro: list
            @return: Éxito de la inserción de la venta.
            @rtype: bool
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO ventas (facventa, codprop, agente) VALUES (:facventa, :codprop, :agente)")
            query.bindValue(":facventa", str(registro[0]))
            query.bindValue(":codprop", registro[1])
            query.bindValue(":agente", str(registro[2]))
            if query.exec():
                update_query = QtSql.QSqlQuery()
                update_query.prepare(
                    "UPDATE propiedades SET estado = 'Vendido', baja = :fechaBaja WHERE codigo = :codigo")
                update_query.bindValue(":fechaBaja", QtCore.QVariant(datetime.now().strftime("%d/%m/%Y")))
                update_query.bindValue(":codigo", registro[1])
                if update_query.exec():
                    return True
                else:
                    print("Error en la ejecución de la consulta de actualización:", update_query.lastError().text())
                    return False
            else:
                print("Error en la ejecución de la consulta de inserción:", query.lastError().text())
                return False
        except Exception as e:
            print("Error al dar de alta factura en conexion:", e)
            return False

    @staticmethod
    def listadoVentas(idFactura):
        """
            Devuelve el listado de ventas asociadas a una factura específica.

            Procedimiento:
            1. Prepara y ejecuta una consulta SQL para obtener las ventas asociadas a la factura.
            2. Recorre los resultados de la consulta y los añade a una lista.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de obtención de datos.

            @param idFactura: ID de la factura para la cual se desean obtener las ventas.
            @type idFactura: int
            @return: Lista de ventas asociadas a la factura.
            @rtype: list
            """
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare(
                "SELECT v.idventa, v.codprop, p.direccion, p.municipio, p.tipo_propiedad, "
                "p.precio_venta FROM ventas AS v INNER JOIN propiedades as p on v.codprop = p.codigo WHERE v.facventa = :facventa")
            query.bindValue(":facventa", str(idFactura))

            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            else:
                print("Error en la ejecución de la consulta:", query.lastError().text())

            return listado
        except Exception as e:
            print("Error listando facturas en listadoFacturas - conexión", e)
            return []

    @staticmethod
    def bajaVenta(idVenta):
        """
            Elimina una venta de la base de datos.

            Procedimiento:
            1. Prepara y ejecuta una consulta SQL para eliminar una venta por su ID.
            2. Devuelve True si la eliminación es exitosa, de lo contrario devuelve False.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de eliminación de la venta.

            @param idVenta: ID de la venta a eliminar.
            @type idVenta: int
            @return: Éxito de la eliminación de la venta.
            @rtype: bool
            """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM ventas WHERE idventa = :idventa")
            query.bindValue(":idventa", str(idVenta))
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("Error al eliminar una venta en conexion.", e)
            return False

    @staticmethod
    def altaPropiedadVenta(codigoPropiedad):
        """
            Actualiza el estado de una propiedad a 'Disponible' y elimina la fecha de baja.

            Procedimiento:
            1. Prepara y ejecuta una consulta SQL para actualizar el estado de la propiedad y eliminar la fecha de baja.
            2. Devuelve True si la actualización es exitosa, de lo contrario devuelve False.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de actualización.

            @param codigoPropiedad: Código de la propiedad a actualizar.
            @type codigoPropiedad: int
            @return: Éxito de la actualización de la propiedad.
            @rtype: bool
            """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "UPDATE propiedades SET estado = 'Disponible', baja = :fechaBaja WHERE codigo = :codigo")
            query.bindValue(":codigo", str(codigoPropiedad))
            query.bindValue(":fechaBaja", QtCore.QVariant())
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("Error al vender una Propiedad en conexion.", e)

    @staticmethod
    def cargaVenta(codigoVenta):
        """
            Carga las ventas asociadas a una factura específica.

            Procedimiento:
            1. Prepara y ejecuta una consulta SQL para obtener las ventas asociadas a la factura.
            2. Recorre los resultados de la consulta y los añade a una lista.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de obtención de datos.

            @param codigoVenta: Código de la factura para la cual se desean obtener las ventas.
            @type codigoVenta: int
            @return: Lista de ventas asociadas a la factura.
            @rtype: list
            """
        try:
            listado = []
            base_query = "SELECT * FROM ventas WHERE facventa = :codigoVenta"
            query = QtSql.QSqlQuery()
            query.prepare(base_query)
            query.bindValue(":codigoVenta", str(codigoVenta))

            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            else:
                print("Error en la ejecución de la consulta:", query.lastError().text())

            return listado
        except Exception as e:
            print("Error al cargar ventas en conexion:", e)
            return []

    @staticmethod
    def cargaPropiedadVenta(codigoPropiedad):
        """
            Carga los datos de una propiedad específica.

            Procedimiento:
            1. Prepara y ejecuta una consulta SQL para obtener los datos de la propiedad con el código proporcionado.
            2. Si se encuentra la propiedad, devuelve una lista con sus datos.
            3. Si no se encuentra la propiedad, devuelve None.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de obtención de datos.

            @param codigoPropiedad: Código de la propiedad a buscar.
            @type codigoPropiedad: int
            @return: Lista con los datos de la propiedad o None si no se encuentra.
            @rtype: list or None
            """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM propiedades WHERE codigo = :id")
            query.bindValue(":id", codigoPropiedad)

            if query.exec():
                if query.next():
                    result = [query.value(i) for i in range(query.record().count())]
                    return result
                else:
                    print("No record found with the given id.")
                    return None
            else:
                print("Error in query execution:", query.lastError().text())
                return None
        except Exception as e:
            print("Error in selectById:", e)
            return None

    @staticmethod
    def cargaOneFactura(idFactura):
        """

        :param idFactura: La id de la factura
        :type idFactura: String
        :return: Lista con los datos de una factura
        :rtype: List

        Metodo para buscar una factura en concreto
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM facturas WHERE id = :id")
            query.bindValue(":id", idFactura)
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as e:
            print("Error cargando factura en cargaOneFactura - conexión", e)

    '''
    GESTION DE ALQUILERES
    '''

    @staticmethod
    def altaContratoAlquiler(nuevoAlquiler):
        """
            Añade un nuevo contrato de alquiler a la base de datos.

            Procedimiento:
            1. Prepara y ejecuta una consulta SQL para insertar un nuevo contrato de alquiler con los datos proporcionados.
            2. Si la inserción es exitosa, llama al método `altaMensualidades` para generar las mensualidades correspondientes.
            3. Actualiza el estado de la propiedad a 'Alquilado' y establece la fecha de inicio del alquiler.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de inserción del contrato de alquiler.

            @param nuevoAlquiler: Lista con los datos del nuevo contrato de alquiler.
                                  El primer elemento es el ID de la propiedad, el segundo es el DNI del cliente,
                                  el tercero es el ID del agente, el cuarto es la fecha de inicio del alquiler,
                                  el quinto es la fecha de fin del alquiler y el sexto es el precio del alquiler.
            @type nuevoAlquiler: list
            @return: Éxito de la inserción del contrato de alquiler.
            @rtype: bool
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "INSERT INTO alquileres (propiedad_id, cliente_dni, agente_id, fecha_inicio, fecha_fin, precio_alquiler) "
                "VALUES (:idPropiedad, :vendedor, :dniCliente, :inicioAlquiler, :finAlquiler, :precioAlquiler)"
            )
            query.bindValue(":idPropiedad", str(nuevoAlquiler[0]))
            query.bindValue(":vendedor", str(nuevoAlquiler[1]))
            query.bindValue(":dniCliente", str(nuevoAlquiler[2]))
            query.bindValue(":inicioAlquiler", str(nuevoAlquiler[3]))
            query.bindValue(":finAlquiler", str(nuevoAlquiler[4]))
            query.bindValue(":precioAlquiler", str(nuevoAlquiler[5]))

            if query.exec():
                Conexion.altaMensualidades(nuevoAlquiler[0], nuevoAlquiler[3], nuevoAlquiler[4], nuevoAlquiler[5])

                update_query = QtSql.QSqlQuery()
                update_query.prepare(
                    "UPDATE propiedades SET estado = 'Alquilado', baja = :fechaBaja WHERE codigo = :codigo"
                )
                update_query.bindValue(":fechaBaja", QtCore.QVariant(datetime.now().strftime("%d/%m/%Y")))
                update_query.bindValue(":codigo", str(nuevoAlquiler[0]))
                if update_query.exec():
                    return True
                else:
                    print("Error en la ejecución de la consulta de actualización:", update_query.lastError().text())
                    return False
            else:
                print("Error en la ejecución de la consulta:", query.lastError().text())
                return False
        except Exception as e:
            print("Error al dar de alta contrato de alquiler en conexion:", e)
            return False

    @staticmethod
    def listadoContratosAlquileres():
        """
            Devuelve el listado de todos los contratos de alquiler.

            Procedimiento:
            1. Prepara y ejecuta una consulta SQL para obtener todos los contratos de alquiler.
            2. Recorre los resultados de la consulta y los añade a una lista.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de obtención de datos.

            @param None
            @return list: Lista de todos los contratos de alquiler.
            """
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM alquileres")

            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            else:
                print("Error en la ejecución de la consulta:", query.lastError().text())

            return listado
        except Exception as e:
            print("Error listando contratos de alquiler en listadoContratosAlquileres - conexión", e)
            return []

    def altaMensualidades(propiedad_id, fecha_inicio, fecha_fin, precio_mensual):
        """
            Añade mensualidades para un contrato de alquiler.

            Procedimiento:
            1. Convierte las fechas de inicio y fin a objetos datetime.
            2. Inserta una mensualidad para cada mes entre las fechas de inicio y fin.
            3. Marca cada mensualidad como no pagada.

            Parámetros:
            @param propiedad_id: ID de la propiedad.
            @type propiedad_id: int
            @param fecha_inicio: Fecha de inicio del contrato de alquiler en formato dd/mm/yyyy.
            @type fecha_inicio: str
            @param fecha_fin: Fecha de fin del contrato de alquiler en formato dd/mm/yyyy.
            @type fecha_fin: str
            @param precio_mensual: Precio mensual del alquiler.
            @type precio_mensual: float

            Retorna:
            @return: Éxito de la inserción de las mensualidades.
            @rtype: bool
            """
        try:
            query = QtSql.QSqlQuery()
            fecha_inicio = datetime.strptime(fecha_inicio, "%d/%m/%Y")
            fecha_fin = datetime.strptime(fecha_fin, "%d/%m/%Y")

            while fecha_inicio <= fecha_fin:
                mes = fecha_inicio.strftime("%B")
                query.prepare(
                    "INSERT INTO mensualidades (propiedad, mensualidad, importe, pagado) "
                    "VALUES (:propiedad, :mensualidad, :importe, :pagado)"
                )
                query.bindValue(":propiedad", propiedad_id)
                query.bindValue(":mensualidad", mes)
                query.bindValue(":importe", precio_mensual)
                query.bindValue(":pagado", 0)  # 0 indica que no está pagado

                if not query.exec():
                    print(f"Error al insertar la mensualidad de {mes}: {query.lastError().text()}")
                    return False

                # Avanzar al siguiente mes
                if fecha_inicio.month == 12:
                    fecha_inicio = fecha_inicio.replace(year=fecha_inicio.year + 1, month=1)
                else:
                    fecha_inicio = fecha_inicio.replace(month=fecha_inicio.month + 1)

            return True
        except Exception as e:
            print("Error al insertar mensualidades:", e)
            return False

    @staticmethod
    def listadoMensualidades(numContrato):
        """
            Devuelve el listado de todas las mensualidades.

            Procedimiento:
            1. Prepara y ejecuta una consulta SQL para obtener todas las mensualidades.
            2. Recorre los resultados de la consulta y los añade a una lista.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de obtención de datos.

            @param None
            @return list: Lista de todas las mensualidades.
            """
        try:
            listado = []
            base_query = "SELECT * FROM mensualidades WHERE propiedad IN (SELECT propiedad_id FROM alquileres WHERE propiedad_id = :numero_contrato)"
            query = QtSql.QSqlQuery()
            query.prepare(base_query)
            query.bindValue(":numero_contrato", str(numContrato))

            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            else:
                print("Error en la ejecución de la consulta:", query.lastError().text())

            return listado
        except Exception as e:
            print("Error al cargar ventas en conexion:", e)
            return []
        #     listado = []
        #     query = QtSql.QSqlQuery()
        #     query.prepare("SELECT * FROM mensualidades")
        #
        #     if query.exec():
        #         while query.next():
        #             fila = [query.value(i) for i in range(query.record().count())]
        #             listado.append(fila)
        #     else:
        #         print("Error en la ejecución de la consulta:", query.lastError().text())
        #
        #     return listado
        # except Exception as e:
        #     print("Error listando mensualidades en listadoMensualidades - conexión", e)
        #     return []

    @staticmethod
    def actualizarEstadoMensualidad(id_mensualidad, estado):
        """
            Actualiza el estado de pago de una mensualidad.

            Procedimiento:
            1. Convierte el estado del checkbox a 1 (True) o 0 (False).
            2. Prepara y ejecuta una consulta SQL para actualizar el estado de la mensualidad.
            3. Devuelve True si la actualización es exitosa, de lo contrario devuelve False.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de actualización del estado.

            @param id_mensualidad: ID de la mensualidad a actualizar.
            @type id_mensualidad: int
            @param estado: Estado del checkbox que indica si la mensualidad está pagada.
            @type estado: QtCore.Qt.CheckState
            @return: Éxito de la actualización del estado de la mensualidad.
            @rtype: bool
            """
        try:
            query = QtSql.QSqlQuery()
            print("mensualidad:", id_mensualidad, "estado:", estado)

            # Convertimos el estado del checkbox a 1 (True) o 0 (False)
            pagado = 1 if estado == QtCore.Qt.CheckState.Checked.value else 0
            print("estado check:", pagado)

            query.prepare("UPDATE mensualidades SET pagado = :pagado WHERE id = :id")
            query.bindValue(":pagado", pagado)
            query.bindValue(":id", id_mensualidad)

            if query.exec():
                print(f"Estado actualizado: ID {id_mensualidad}, Pagado = {pagado}")
                return True
            else:
                print(f"Error actualizando el estado: {query.lastError().text()}")
                return False
        except Exception as e:
            print(f"Error en actualizarEstadoMensualidad: {e}")
            return False

    @staticmethod
    def borrarContrato(id_contrato):
        """
            Borra un contrato de alquiler de la base de datos.

            Procedimiento:
            1. Obtiene el `propiedad_id` del contrato antes de borrarlo.
            2. Verifica si existen mensualidades pagadas para el contrato.
            3. Si existen mensualidades pagadas, muestra un mensaje de error y no borra el contrato.
            4. Borra las mensualidades asociadas al contrato.
            5. Borra el contrato de alquiler.
            6. Actualiza el estado de la propiedad a 'Disponible'.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de eliminación del contrato.

            @param id_contrato: ID del contrato de alquiler a eliminar.
            @type id_contrato: int
            @return: Éxito de la eliminación del contrato.
            @rtype: bool
        """
        try:
            # Obtener propiedad_id antes de borrar el contrato
            query = QtSql.QSqlQuery()
            query.prepare("SELECT propiedad_id FROM alquileres WHERE id = :id_contrato")
            query.bindValue(":id_contrato", id_contrato)

            if not query.exec() or not query.next():
                print("Error al obtener propiedad_id:", query.lastError().text())
                return False

            propiedad_id = query.value(0)  # Guardar el ID de la propiedad

            # Verificar si existen mensualidades pagadas para el contrato
            query.prepare(
                "SELECT COUNT(*) FROM mensualidades WHERE propiedad = :propiedad_id AND pagado = 1"
            )
            query.bindValue(":propiedad_id", propiedad_id)

            if query.exec() and query.next() and query.value(0) > 0:
                eventos.Eventos.crearMensajeError(
                    "Mensualidades", "No se puede borrar el contrato porque tiene mensualidades pagadas."
                )
                print("No se puede borrar el contrato porque tiene mensualidades pagadas.")
                return False

            # Borrar mensualidades asociadas al contrato
            query.prepare("DELETE FROM mensualidades WHERE propiedad = :propiedad_id")
            query.bindValue(":propiedad_id", propiedad_id)
            if not query.exec():
                print("Error al borrar mensualidades:", query.lastError().text())
                return False

            # Borrar el contrato
            query.prepare("DELETE FROM alquileres WHERE id = :id_contrato")
            query.bindValue(":id_contrato", id_contrato)
            if not query.exec():
                print("Error al borrar el contrato:", query.lastError().text())
                return False

            # Actualizar la propiedad a 'Disponible'
            update_query = QtSql.QSqlQuery()
            update_query.prepare(
                "UPDATE propiedades SET estado = 'Disponible', baja = NULL WHERE codigo = :propiedad_id"
            )
            update_query.bindValue(":propiedad_id", propiedad_id)
            if not update_query.exec():
                print("Error al actualizar la propiedad:", update_query.lastError().text())
                return False

            print(f"Contrato {id_contrato} borrado correctamente.")
            alquileres.Alquileres.cargaTablaContratos()
            alquileres.Alquileres.cargaTablaMensualidades()

            eventos.Eventos.resizeTablaAlquileresGestion()
            eventos.Eventos.pnlVisualizacionAlquileres()

            propiedades.Propiedades.cargarTablaPropiedades()
            return True

        except Exception as e:
            print(f"Error en borrarContrato: {e}")
            return False

    @staticmethod
    def cargaMensualidades(numero_contrato):
        """
                Carga las mensualidades de un contrato de alquiler específico.

                Procedimiento:
                1. Prepara y ejecuta una consulta SQL para obtener las mensualidades del contrato.
                2. Recorre los resultados de la consulta y los añade a una lista.

                Excepciones:
                - Captura y muestra cualquier excepción que ocurra durante el proceso de obtención de datos.

                @param numero_contrato: Número del contrato de alquiler.
                @type numero_contrato: int
                @return: Lista de mensualidades del contrato de alquiler.
                @rtype: list
        """
        try:
            listado = []
            base_query = "SELECT * FROM mensualidades WHERE propiedad IN (SELECT propiedad_id FROM alquileres WHERE id = :numero_contrato)"
            query = QtSql.QSqlQuery()
            query.prepare(base_query)
            query.bindValue(":numero_contrato", str(numero_contrato))

            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            else:
                print("Error en la ejecución de la consulta:", query.lastError().text())

            return listado
        except Exception as e:
            print("Error al cargar ventas en conexion:", e)
            return []

    @staticmethod
    def datosOneAlquiler(idContrato):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare(
                "SELECT a.id, a.fecha_inicio, a.fecha_fin, a.agente_id, c.dnicli, c.nomecli, c.apelcli, p.codigo, "
                "p.tipo_propiedad, p.precio_alquiler, p.municipio, p.direccion FROM alquileres as a "
                "INNER JOIN propiedades as p ON a.propiedad_id = p.codigo "
                "INNER JOIN clientes as c ON a.cliente_dni = c.dnicli WHERE a.id = :idAlquiler")
            query.bindValue(':idAlquiler', idContrato)
            if query.exec():
                while query.next():
                    for i in range(12):
                        registro.append(query.value(i))
            return registro
        except Exception as e:
            print("Error datosOneAlquiler: ", e)

    @staticmethod
    def datosOneMensualidad(idMensualidad):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT id, mensualidad, pagado FROM mensualidades WHERE id = :idMensualidad")
            query.bindValue(":idMensualidad", idMensualidad)
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(query.value(i))
            return registro

        except Exception as e:
            print("Error al cargar datos de una mensualidad en conexcion", str(e))

    # @staticmethod
    # def getIdAlquilerByPropiedad(propiedad_id):
    #     """
    #     Devuelve el ID del alquiler asociado a una propiedad específica.
    #
    #     :param propiedad_id: ID de la propiedad
    #     :type propiedad_id: int
    #     :return: ID del alquiler asociado
    #     :rtype: int
    #     """
    #     try:
    #         query = QtSql.QSqlQuery()
    #         query.prepare("SELECT id FROM alquileres WHERE propiedad_id = :propiedad_id")
    #         query.bindValue(":propiedad_id", propiedad_id)
    #         if query.exec() and query.next():
    #             return query.value(0)
    #         else:
    #             return None
    #     except Exception as e:
    #         print("Error al obtener el ID del alquiler por propiedad:", e)
    #         return None
