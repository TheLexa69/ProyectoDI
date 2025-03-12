import datetime

# from pandas.core.interchange.from_dataframe import primitive_column_to_ndarray
from reportlab.lib.testutils import setOutDir

import conexion
import conexionserver
import eventos
import facturas
import var
import re
from PyQt6 import QtWidgets, QtGui, QtCore

from eventos import Eventos


class Propiedades():

    @staticmethod
    def altaTipoPropiedad(venDialogo):
        """
            Añade un nuevo tipo de propiedad a la base de datos.

            Args:
                venDialogo (QDialog): El diálogo de gestión de propiedades.

            Raises:
                Exception: Si ocurre un error al añadir el tipo de propiedad.
            """
        try:
            tipo = var.dlggestion.ui.txtTipoprop.text().title()
            # registro = conexion.Conexion.altaTipoprop(tipo)
            # registro = conexionserver.ConexionServer.altaTipoprop(tipo)
            registro = var.claseConexion.altaTipoprop(tipo)
            if registro:
                var.ui.cmbTipoprop.clear()
                var.ui.cmbTipoprop.addItems(registro)
                eventos.Eventos.crearMensajeInfo("Aviso", "Tipo de propiedad añadida.")

                Propiedades.cargarTipopropGestion(venDialogo)
            else:
                eventos.Eventos.crearMensajeError("Aviso", "Error al añadir tipo de propiedad añadida.")

            var.dlggestion.ui.txtTipoprop.setText("")
        except Exception as e:
            print("Error alta tipo propiedad" + e)

    @staticmethod
    def bajaTipoPropiedad(venDialogo):
        """
            Elimina un tipo de propiedad de la base de datos.

            Args:
                venDialogo (QDialog): El diálogo de gestión de propiedades.

            Raises:
                Exception: Si ocurre un error al eliminar el tipo de propiedad.
            """
        try:
            tipo = var.dlggestion.ui.txtTipoprop.text().title()
            # if conexion.Conexion.bajaTipoprop(tipo):
            # if conexionserver.ConexionServer.bajaTipoprop(tipo):
            if var.claseConexion.bajaTipoprop(tipo):
                eventos.Eventos.crearMensajeInfo("Aviso", "Tipo de propiedad eliminada.")
                Propiedades.cargarTipoprop()
                var.dlggestion.ui.txtTipoprop.setText("")
                Propiedades.cargarTipopropGestion(venDialogo)
            else:
                eventos.Eventos.crearMensajeError("Aviso", "Error al eliminar tipo de propiedad.")
        except Exception as e:
            print("Error baja tipo propiedad" + e)

    @staticmethod
    def altaPropiedad():
        """
                Añade una nueva propiedad a la base de datos.

                Recopila los datos de la interfaz de usuario, verifica que los campos obligatorios estén completos y que los precios sean válidos.
                Si todo es correcto, guarda la propiedad en la base de datos y actualiza la tabla de propiedades.

                Raises:
                    Exception: Si ocurre un error al añadir la propiedad.
                """
        try:
            propiedad = [var.ui.txtAltaprop.text(), var.ui.txtDirprop.text(), var.ui.cmbProvprop.currentText(),
                         var.ui.cmbMuniprop.currentText(), var.ui.cmbTipoprop.currentText(),
                         var.ui.spinHabprop.text(), var.ui.spinBanosprop.text(), var.ui.txtSuperprop.text(),
                         var.ui.txtPrecioAlquilerprop.text(),
                         var.ui.txtPrecioVentaprop.text(),
                         var.ui.txtCpprop.text(), var.ui.areatxtDescriprop.toPlainText()]
            tipoOper = []
            if var.ui.chkAlquilprop.isChecked():
                tipoOper.append(var.ui.chkAlquilprop.text())
            if var.ui.chkVentaprop.isChecked():
                tipoOper.append(var.ui.chkVentaprop.text())
            if var.ui.chkInterprop.isChecked():
                tipoOper.append(var.ui.chkInterprop.text())
            propiedad.append(tipoOper)
            if var.ui.rbtDisponprop.isChecked():
                propiedad.append(var.ui.rbtDisponprop.text())
            elif var.ui.rbtAlquilprop.isChecked():
                propiedad.append(var.ui.rbtAlquilprop.text())
            elif var.ui.rbtVentaprop.isChecked():
                propiedad.append(var.ui.rbtVentaprop.text())

            propiedad.append(var.ui.txtNomeprop.text().title())
            propiedad.append(var.ui.txtMovilprop.text())

            precioAlquiler = propiedad[8]
            precioVenta = propiedad[9]

            # if Propiedades.hasCamposObligatoriosAlta(propiedad) and Propiedades.checkPrecioAlquiler(precioAlquiler) and Propiedades.checkPrecioVenta(precioVenta) and conexion.Conexion.altaPropiedad(propiedad):
            # if Propiedades.hasCamposObligatoriosAlta(propiedad) and Propiedades.checkPrecioAlquiler(precioAlquiler) and Propiedades.checkPrecioVenta(precioVenta) and conexionserver.ConexionServer.altaPropiedad(propiedad):
            if Propiedades.hasCamposObligatoriosAlta(propiedad) and Propiedades.checkPrecioAlquiler(
                    precioAlquiler) and Propiedades.checkPrecioVenta(precioVenta) and var.claseConexion.altaPropiedad(
                propiedad):
                eventos.Eventos.crearMensajeInfo("Aviso", "Se ha grabado la propiedad en la base de datos.")
                Propiedades.cargarTablaPropiedades()

            elif not Propiedades.hasCamposObligatoriosAlta(propiedad):
                eventos.Eventos.crearMensajeError("Error", "Hay campos vacíos que deben ser cubiertos.")

            elif not Propiedades.checkPrecioAlquiler(precioAlquiler):
                eventos.Eventos.crearMensajeError("Error",
                                                  "Para guardar una propiedad de tipo alquiler debe guardarse un precio y estar marcada la casilla 'Alquiler'.")

            elif not Propiedades.checkPrecioVenta(precioVenta):
                eventos.Eventos.crearMensajeError("Error",
                                                  "Para guardar una propiedad de tipo venta debe guardarse un precio y estar marcada la casilla 'Venta'.")
            else:
                eventos.Eventos.crearMensajeError("Error", "Se ha producido un error al grabar la propiedad.")
        except Exception as e:
            print(str(e))

    @staticmethod
    def checkMovilProp(movil):
        """
            Verifica si el número de móvil es válido y actualiza el estilo del campo de texto correspondiente.

            Args:
                movil (str): El número de móvil a verificar.

            Raises:
                Exception: Si ocurre un error durante la verificación del número de móvil.
            """
        try:
            if eventos.Eventos.isMovilValido(movil):
                var.ui.txtMovilprop.setStyleSheet('background-color: rgb(255, 255, 255);')
            else:
                var.ui.txtMovilprop.setStyleSheet('border: 1px solid #de6767; border-radius: 5px; font-style: italic;')
                var.ui.txtMovilprop.setText(None)
                var.ui.txtMovilprop.setPlaceholderText("móvil no válido")
                var.ui.txtMovilprop.setFocus()
        except Exception as e:
            print("error check movil", e)

    @staticmethod
    def cargarTablaPropiedades():
        """
            Carga la tabla de propiedades con los datos obtenidos de la base de datos.

            Obtiene la lista de propiedades desde la base de datos y la muestra en la tabla de propiedades de la interfaz de usuario.
            Si no hay propiedades que mostrar, se deshabilitan los botones de navegación y se muestra un mensaje indicándolo.
            Si hay propiedades, se habilitan los botones de navegación según corresponda y se muestra la lista paginada.

            Raises:
                Exception: Si ocurre un error al cargar las propiedades en la tabla.
            """
        try:
            listado = var.claseConexion.listadoPropiedades()
            var.lenPropiedades = len(listado)

            var.ui.spinProppPag.setValue(var.maxPropPagina)

            if len(listado) == 0:
                var.ui.btnSiguienteProp.setDisabled(True)
                var.ui.btnAnteriorProp.setDisabled(True)
                var.ui.tablaProp.setRowCount(4)
                var.ui.tablaProp.setItem(0, 0,
                                         QtWidgets.QTableWidgetItem("No hay propiedades con los filtros seleccionados"))
                var.ui.tablaProp.setSpan(0, 0, 4, 9)
                var.ui.tablaProp.item(0, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.lblPaginasProp.setText("Página 0/0")
            else:
                var.ui.tablaProp.clearSpans()

                inicioListado = var.paginaActualProp * var.maxPropPagina
                sublistado = listado[inicioListado: inicioListado + var.maxPropPagina]

                if listado[0] == sublistado[0]:
                    var.ui.btnAnteriorProp.setDisabled(True)
                else:
                    var.ui.btnAnteriorProp.setDisabled(False)

                if listado[-1] == sublistado[-1]:
                    var.ui.btnSiguienteProp.setDisabled(True)
                else:
                    var.ui.btnSiguienteProp.setDisabled(False)

                numPaginas = (var.lenPropiedades // var.maxPropPagina) + 1
                if len(listado) % var.maxPropPagina == 0:
                    numPaginas -= 1
                var.ui.lblPaginasProp.setText("Página " + str(var.paginaActualProp + 1) + "/" + str(numPaginas))

                var.ui.tablaProp.setRowCount(len(sublistado))
                index = 0
                for registro in sublistado:
                    registro = [x if x != None else '' for x in registro]
                    var.ui.tablaProp.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))  # codigo
                    var.ui.tablaProp.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[5]))  # municipio
                    var.ui.tablaProp.setItem(index, 2, QtWidgets.QTableWidgetItem(registro[6]))  # tipo_provincia
                    var.ui.tablaProp.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[7])))  # num_habitaciones
                    var.ui.tablaProp.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[8])))  # num_baños

                    if var.claseConexion == conexion.Conexion:
                        precio_alquiler = f"{registro[10]:,.1f} €" if registro[10] != "" else " - €"
                        var.ui.tablaProp.setItem(index, 5, QtWidgets.QTableWidgetItem(precio_alquiler))  # precio_alqui

                        precio_venta = f"{registro[11]:,.1f} €" if registro[11] != "" else " - €"
                        var.ui.tablaProp.setItem(index, 6, QtWidgets.QTableWidgetItem(precio_venta))  # precio_venta

                        tipo_operacion = registro[14].replace('[', '').replace(']', '').replace("'", "")
                        var.ui.tablaProp.setItem(index, 7, QtWidgets.QTableWidgetItem(tipo_operacion))  # tipo_operacion

                    elif var.claseConexion == conexionserver.ConexionServer:
                        var.ui.tablaProp.setItem(index, 5, QtWidgets.QTableWidgetItem(str(registro[10]) + " €"))
                        var.ui.tablaProp.setItem(index, 6, QtWidgets.QTableWidgetItem(str(registro[11]) + " €"))
                        var.ui.tablaProp.setItem(index, 7, QtWidgets.QTableWidgetItem(
                            str(registro[14].replace('[', '').replace(']', '').replace("'", ""))))

                    var.ui.tablaProp.setItem(index, 8, QtWidgets.QTableWidgetItem(str(registro[2])))  # fecha de baja

                    var.ui.tablaProp.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaProp.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaProp.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaProp.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaProp.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaProp.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaProp.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaProp.item(index, 7).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                    var.ui.tablaProp.item(index, 8).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    index += 1


        except Exception as e:
            print("Error al cargar propiedades en la tabla cargarTablaPropiedades", e)

    @staticmethod
    def cargaOnePropiedad():
        """
            Carga los datos de una propiedad seleccionada en la interfaz de usuario.

            Obtiene los datos de la propiedad seleccionada en la tabla de propiedades y los carga en los campos correspondientes de la interfaz de usuario.
            También actualiza las listas de propiedades en venta y alquiler, y carga los datos en las facturas si la propiedad está disponible.

            Raises:
                Exception: Si ocurre un error al cargar los datos de la propiedad.
            """
        try:
            fila = var.ui.tablaProp.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = var.claseConexion.datosOnePropiedad(str(datos[0]))
            listado = [var.ui.lblProp, var.ui.txtAltaprop, var.ui.txtBajaprop, var.ui.txtDirprop, var.ui.cmbProvprop,
                       var.ui.cmbMuniprop, var.ui.cmbTipoprop, var.ui.spinHabprop, var.ui.spinBanosprop,
                       var.ui.txtSuperprop, var.ui.txtPrecioAlquilerprop, var.ui.txtPrecioVentaprop, var.ui.txtCpprop,
                       var.ui.areatxtDescriprop, var.ui.rbtDisponprop, var.ui.rbtAlquilprop, var.ui.rbtVentaprop,
                       var.ui.chkInterprop, var.ui.chkAlquilprop, var.ui.chkVentaprop, var.ui.txtNomeprop,
                       var.ui.txtMovilprop]
            listadoVentas = []
            listadoAlquileres = []
            for i in range(len(listado)):
                if i in (4, 5, 6):
                    listado[i].setCurrentText(registro[i])
                elif i in (7, 8):
                    listado[i].setValue(int(registro[i]))
                elif i == 13:
                    listado[i].setPlainText(registro[i])
                elif i == 14:
                    listado[i].setChecked(registro[15] == "Disponible")
                elif i == 15:
                    listado[i].setChecked(registro[15] == "Alquilado")
                elif i == 16:
                    listado[i].setChecked(registro[15] == "Vendido")
                elif i in (17, 18, 19):
                    listado[17].setChecked("Intercambio" in registro[14])
                    listado[18].setChecked("Alquiler" in registro[14])
                    listado[19].setChecked("Venta" in registro[14])
                    if "Venta" in registro[14] and "Venta" not in listadoVentas:
                        listadoVentas.append("Venta")

                    if "Alquiler" in registro[14] and "Alquiler" not in listadoAlquileres:
                        listadoAlquileres.append("Alquiler")
                elif i == 20:
                    listado[i].setText(registro[16])
                elif i == 21:
                    listado[i].setText(registro[17])
                else:
                    listado[i].setText(registro[i])

            listadoVentas.append(registro[0])
            listadoVentas.append(registro[6])
            listadoVentas.append(registro[11])  # PRECIO VENTA
            listadoVentas.append(registro[3])
            listadoVentas.append(registro[5])

            listadoAlquileres.append(registro[0])
            listadoAlquileres.append(registro[6])
            listadoAlquileres.append(registro[10])  # PRECIO ALQUILER
            listadoAlquileres.append(registro[3])
            listadoAlquileres.append(registro[5])

            if "Disponible" in registro and "Disponible" not in listadoVentas:
                listadoVentas.append("Disponible")

            # if "Alquilado" in registro and "Alquilado" not in listadoVentas:
            #     listadoVentas.append("Alquilado")

            if "Vendido" in registro and "Vendido" not in listadoVentas:
                listadoVentas.append("Vendido")

            if "Disponible" in registro and "Disponible" not in listadoAlquileres:
                listadoAlquileres.append("Disponible")

            if "Alquilado" in registro and "Alquilado" not in listadoAlquileres:
                listadoAlquileres.append("Alquilado")

            if listadoVentas[0] == "Venta" and listadoVentas[6] == "Disponible":
                facturas.Facturas.cargarPropiedadVenta(listadoVentas)

            if listadoAlquileres[0] == "Alquiler" and listadoAlquileres[6] == "Disponible":
                facturas.Facturas.cargarPropiedadAlquiler(listadoAlquileres)

        except Exception as e:
            print("Error cargando UNA propiedad en propiedades.", e)

    @staticmethod
    def modifProp():
        """
                Modifica una propiedad existente en la base de datos.

                Recopila los datos de la interfaz de usuario, verifica que los campos obligatorios estén completos y que los precios sean válidos.
                Si todo es correcto, actualiza la propiedad en la base de datos y actualiza la tabla de propiedades.

                Raises:
                    Exception: Si ocurre un error al modificar la propiedad.
                """
        try:
            propiedad = [var.ui.lblProp.text(), var.ui.txtAltaprop.text(), var.ui.txtBajaprop.text(),
                         var.ui.txtDirprop.text(), var.ui.cmbProvprop.currentText(), var.ui.cmbMuniprop.currentText(),
                         var.ui.cmbTipoprop.currentText(), var.ui.spinHabprop.text(), var.ui.spinBanosprop.text(),
                         var.ui.txtSuperprop.text(), var.ui.txtPrecioAlquilerprop.text(),
                         var.ui.txtPrecioVentaprop.text(), var.ui.txtCpprop.text(),
                         var.ui.areatxtDescriprop.toPlainText()]
            tipoOper = []
            if var.ui.chkAlquilprop.isChecked():
                tipoOper.append(var.ui.chkAlquilprop.text())
            if var.ui.chkVentaprop.isChecked():
                tipoOper.append(var.ui.chkVentaprop.text())
            if var.ui.chkInterprop.isChecked():
                tipoOper.append(var.ui.chkInterprop.text())
            propiedad.append(tipoOper)
            if var.ui.rbtDisponprop.isChecked():
                propiedad.append(var.ui.rbtDisponprop.text())
            elif var.ui.rbtAlquilprop.isChecked():
                propiedad.append(var.ui.rbtAlquilprop.text())
            elif var.ui.rbtVentaprop.isChecked():
                propiedad.append(var.ui.rbtVentaprop.text())

            propiedad.append(var.ui.txtNomeprop.text().title())
            propiedad.append(var.ui.txtMovilprop.text())

            fecha_baja = propiedad[2]
            precioAlquiler = propiedad[10]
            precioVenta = propiedad[11]

            if fecha_baja != "" and not Propiedades.esFechasValidas(propiedad):
                eventos.Eventos.crearMensajeError("Error", "La fecha de baja no puede ser anterior a la fecha de alta.")

            elif fecha_baja != "" and var.ui.rbtDisponprop.isChecked():
                eventos.Eventos.crearMensajeError("Error",
                                                  "No es posible guardar fecha de baja si el estado del inmueble es 'Disponible'.")

            elif Propiedades.hasCamposObligatoriosModif(propiedad) and Propiedades.checkPrecioAlquiler(
                    precioAlquiler) and Propiedades.checkPrecioVenta(precioVenta) and var.claseConexion.modifProp(
                propiedad):
                eventos.Eventos.crearMensajeInfo("Aviso", "Se ha modificado la propiedad correctamente.")
                Propiedades.cargarTablaPropiedades()

            elif not Propiedades.hasCamposObligatoriosModif(propiedad):
                eventos.Eventos.crearMensajeError("Error", "Hay algunos campos obligatorios que están vacíos.")

            elif not Propiedades.checkPrecioAlquiler(precioAlquiler):
                eventos.Eventos.crearMensajeError("Error",
                                                  "Para guardar una propiedad de tipo alquiler debe guardarse un precio y estar marcada la casilla 'Alquiler'.")

            elif not Propiedades.checkPrecioVenta(precioVenta):
                eventos.Eventos.crearMensajeError("Error",
                                                  "Para guardar una propiedad de tipo venta debe guardarse un precio y estar marcada la casilla 'Venta'.")

            else:
                eventos.Eventos.crearMensajeError("Error", "Se ha producido un error al modificar la propiedad")

        except Exception as e:
            print("Error modificando cliente en propiedades.", e)

    @staticmethod
    def bajaProp():
        """
            Da de baja una propiedad existente en la base de datos.

            Recopila los datos de la interfaz de usuario, verifica que los campos obligatorios estén completos y que las fechas sean válidas.
            Si todo es correcto, da de baja la propiedad en la base de datos y actualiza la tabla de propiedades.

            Raises:
                Exception: Si ocurre un error al dar de baja la propiedad.
            """
        propiedad = [var.ui.lblProp.text(), var.ui.txtAltaprop.text(), var.ui.txtBajaprop.text()]
        if var.ui.rbtAlquilprop.isChecked():
            propiedad.append(var.ui.rbtAlquilprop.text())
        elif var.ui.rbtVentaprop.isChecked():
            propiedad.append(var.ui.rbtVentaprop.text())

        if propiedad[2] == "" or propiedad[2] is None:
            eventos.Eventos.crearMensajeError("Error", "Es necesario elegir una fecha para dar de baja la propiedad.")

        elif not var.ui.rbtDisponprop.isChecked() and var.claseConexion.bajaProp(
                propiedad) and Propiedades.esFechasValidas(propiedad):
            eventos.Eventos.crearMensajeInfo("Aviso", "Se ha dado de baja la propiedad.")
            var.paginaActualProp = 0
            Propiedades.cargarTablaPropiedades()

        elif var.ui.rbtDisponprop.isChecked():
            eventos.Eventos.crearMensajeError("Error",
                                              "Para dar de baja el estado de la propiedad no puede ser disponible.")

        elif not Propiedades.esFechasValidas(propiedad):
            eventos.Eventos.crearMensajeError("Error", "La fecha de baja no puede ser anterior a la fecha de alta.")

        else:
            eventos.Eventos.crearMensajeError("Error", "Se ha producido un error al dar de baja la propiedad.")

    @staticmethod
    def historicoProp():
        """
           Carga el historial de propiedades en la tabla de propiedades.

           Establece la página actual de propiedades a 0 y carga la tabla de propiedades con los datos históricos.

           Raises:
               Exception: Si ocurre un error al cargar el historial de propiedades.
           """
        try:
            var.paginaActualProp = 0
            Propiedades.cargarTablaPropiedades()
        except Exception as e:
            print("checkbox historico no funciona correcatamente", e)

    @staticmethod
    def buscaProp():
        """
            Realiza una búsqueda filtrada de propiedades.

            Establece la página actual de propiedades a 0 y carga la tabla de propiedades con los datos filtrados.

            Raises:
                Exception: Si ocurre un error durante la búsqueda filtrada.
            """
        try:
            var.paginaActualProp = 0
            Propiedades.cargarTablaPropiedades()
        except Exception as e:
            print("búsqueda filtrada no funciona correcatamente", e)

    @staticmethod
    def hasCamposObligatoriosAlta(datosPropiedades):
        """
                Verifica si los campos obligatorios para el alta de una propiedad están completos.

                Args:
                    datosPropiedades (list): Lista con los datos de la propiedad.

                Returns:
                    bool: True si todos los campos obligatorios están completos, False en caso contrario.
                """
        datos = datosPropiedades[:]
        descripcion = datos.pop(11)
        precio_alquiler = datos.pop(9)
        precio_venta = datos.pop(8)
        num_banos = datos.pop(6)
        num_habitaciones = datos.pop(5)

        for dato in datos:
            if dato == "" or dato is None:
                return False
        return True

    @staticmethod
    def hasCamposObligatoriosModif(datosPropiedades):
        """
            Verifica si los campos obligatorios para la modificación de una propiedad están completos.

            Args:
                datosPropiedades (list): Lista con los datos de la propiedad.

            Returns:
                bool: True si todos los campos obligatorios están completos, False en caso contrario.
            """
        datos = datosPropiedades[:]
        descripcion = datos.pop(13)
        precio_venta = datos.pop(11)
        precio_alquiler = datos.pop(10)
        num_banos = datos.pop(8)
        num_habitaciones = datos.pop(7)
        fecha_baja = datos.pop(2)

        for dato in datos:
            if dato == "" or dato is None:
                return False
        return True

    @staticmethod
    def esFechasValidas(datosPropiedades):
        """
                Verifica si las fechas de alta y baja de una propiedad son válidas.

                Args:
                    datosPropiedades (list): Lista con los datos de la propiedad.

                Returns:
                    bool: True si la fecha de alta es anterior a la fecha de baja, False en caso contrario.

                Raises:
                    ValueError: Si la fecha no tiene el formato correcto o no es válida.
                    TypeError: Si se esperaba una cadena de texto para la fecha.
            """
        datos = datosPropiedades[:]
        alta = datos[1]
        baja = datos[2]

        try:
            fecha_alta = datetime.datetime.strptime(alta, "%d/%m/%Y")
            fecha_baja = datetime.datetime.strptime(baja, "%d/%m/%Y")

            return fecha_alta < fecha_baja  # si fecha de alta es posterior a fecha de baja devuelve false

        except ValueError as e:
            print("Error: La fecha no tiene el formato correcto o no es válida.", e)
            return False
        except TypeError as e:
            print("Error: Se esperaba una cadena de texto para la fecha.", e)
            return False

    @staticmethod
    def is_num(value):
        """
                Verifica si un valor es un número.

                Args:
                    value (str): El valor a verificar.

                Returns:
                    bool: True si el valor es un número, False en caso contrario.
                """
        return bool(re.match(r'^-?\d+(\.\d+)?$', str(value)))

    @staticmethod
    def checkPrecioAlquiler(precioAlquiler):
        """
            Verifica si el precio de alquiler es válido.

            Args:
                precioAlquiler (str): El precio de alquiler a verificar.

            Returns:
                bool: True si el precio de alquiler es válido, False en caso contrario.
            """
        if Propiedades.is_num(precioAlquiler) and var.ui.chkAlquilprop.isChecked():
            return True
        elif (precioAlquiler == "" or precioAlquiler is None) and not var.ui.chkAlquilprop.isChecked():
            return True
        else:
            return False

    @staticmethod
    def checkPrecioVenta(precioVenta):
        """
            Verifica si el precio de venta es válido.

            Args:
                precioVenta (str): El precio de venta a verificar.

            Returns:
                bool: True si el precio de venta es válido, False en caso contrario.
            """
        if Propiedades.is_num(precioVenta) and var.ui.chkVentaprop.isChecked():
            return True
        elif (precioVenta == "" or precioVenta is None) and not var.ui.chkVentaprop.isChecked():
            return True
        else:
            return False

    @staticmethod
    def filtrar():
        """
            Filtra las propiedades según los criterios seleccionados.

            Alterna el estado del botón de búsqueda de tipo de propiedad y recarga la tabla de propiedades con los datos filtrados.
            """
        checkeado = var.ui.btnBuscaTipoProp.isChecked()
        var.ui.btnBuscaTipoProp.setChecked(not checkeado)
        Propiedades.cargarTablaPropiedades()

    @staticmethod
    def activarCheckPrecios():
        """
            Activa o desactiva los checkboxes de precios de venta y alquiler.

            Verifica si los campos de texto de precios de venta y alquiler están vacíos o no.
            Si no están vacíos, activa los checkboxes correspondientes; de lo contrario, los desactiva.
            """
        if var.ui.txtPrecioVentaprop.text() != "":
            var.ui.chkVentaprop.setChecked(True)
        else:
            var.ui.chkVentaprop.setChecked(False)

        if var.ui.txtPrecioAlquilerprop.text() != "":
            var.ui.chkAlquilprop.setChecked(True)
        else:
            var.ui.chkAlquilprop.setChecked(False)

    @staticmethod
    def cambiarAvailableRbt():
        """
            Cambia la disponibilidad de los botones de radio según el estado del campo de texto de baja.

            Si el campo de texto de baja está vacío, habilita el botón de radio de disponibilidad y deshabilita los botones de radio de alquiler y venta.
            Si el campo de texto de baja no está vacío, habilita los botones de radio de alquiler y venta, y deshabilita el botón de radio de disponibilidad.
            """
        if var.ui.txtBajaprop.text() == "" or var.ui.txtBajaprop.text() is None:
            var.ui.rbtDisponprop.setEnabled(True)
            var.ui.rbtAlquilprop.setEnabled(False)
            var.ui.rbtVentaprop.setEnabled(False)
            var.ui.rbtDisponprop.setChecked(True)
        else:
            var.ui.rbtAlquilprop.setEnabled(True)
            var.ui.rbtAlquilprop.setChecked(True)
            var.ui.rbtVentaprop.setEnabled(True)
            var.ui.rbtDisponprop.setEnabled(False)

    @staticmethod
    def cargarTipoprop():
        """
           Carga los tipos de propiedad en el comboBox correspondiente.

           Obtiene la lista de tipos de propiedad desde la base de datos y la añade al comboBox de tipos de propiedad en la interfaz de usuario.
           """
        registro = var.claseConexion.cargarTipoprop()
        var.ui.cmbTipoprop.clear()
        var.ui.cmbTipoprop.addItems(registro)

    def seleccionarTipoGestion(self):
        """
            Selecciona el tipo de propiedad en la gestión de propiedades.

            Obtiene el tipo de propiedad seleccionado en el comboBox de gestión de propiedades y lo establece en el campo de texto correspondiente.

            Args:
                self: La instancia actual del objeto.
            """
        tipo = self.ui.cmbTipopropGestion.currentText()
        self.ui.txtTipoprop.setText(tipo)

    def cargarTipopropGestion(self):
        """
            Carga los tipos de propiedad en el comboBox de gestión de propiedades.

            Obtiene la lista de tipos de propiedad desde la base de datos y la añade al comboBox de tipos de propiedad en la interfaz de usuario.

            Args:
                self: La instancia actual del objeto.
            """
        registro = var.claseConexion.cargarTipoprop()
        self.ui.cmbTipopropGestion.clear()
        self.ui.cmbTipopropGestion.addItems(registro)

    def cargaMuniInformeProp(self):
        """
            Carga los municipios en el comboBox del informe de propiedades.

            Obtiene la lista de municipios desde la base de datos y la añade al comboBox de municipios en la interfaz de usuario.
            También configura un completer para facilitar la búsqueda de municipios en el comboBox.

            Args:
                self: La instancia actual del objeto.
            """
        registro = var.claseConexion.cargarMunicipios()
        registro.insert(0, "")
        self.ui.cmbInformeMuniProp.setEditable(True)
        self.ui.cmbInformeMuniProp.clear()
        self.ui.cmbInformeMuniProp.addItems(registro)
        completer = QtWidgets.QCompleter(registro, self.ui.cmbInformeMuniProp)
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        self.ui.cmbInformeMuniProp.setCompleter(completer)
