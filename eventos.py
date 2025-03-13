import csv
import json
import os
import sys
import time
import re
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QHeaderView, QCompleter
from PyQt6.QtWidgets import QHeaderView

import locale
import eventos
import clientes
import conexion
import conexionserver
import var
from PyQt6 import QtWidgets, QtGui, QtCore
import zipfile
import shutil

import vendedores

# Establecer configuracion regional

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
locale.setlocale(locale.LC_MONETARY, 'es_ES.UTF-8')


class Eventos():
    @staticmethod
    def mensajeSalir():
        """
            Muestra un mensaje de confirmación para salir de la aplicación.

            Procedimiento:
            1. Crea un cuadro de mensaje con el título 'Salir' y el mensaje '¿Desea salir?'.
            2. Si el usuario selecciona 'Sí', cierra la aplicación.
            3. Si el usuario selecciona 'No', oculta el cuadro de mensaje.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de salida.
            """
        mbox = Eventos.crearMensajeSalida('Salir', "¿Desea salir?")

        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            mbox.hide()

    @staticmethod
    def crearMensajeSalida(titulo_ventana, mensaje):
        """
                Crea un cuadro de mensaje de confirmación para salir de la aplicación.

                Procedimiento:
                1. Crea un cuadro de mensaje con el título y mensaje proporcionados.
                2. Establece el icono del cuadro de mensaje como una pregunta.
                3. Establece el icono de la ventana del cuadro de mensaje.
                4. Establece los botones estándar del cuadro de mensaje a 'Sí' y 'No'.
                5. Establece el botón predeterminado a 'No'.
                6. Cambia el texto de los botones a 'Sí' y 'No' respectivamente.
                7. Retorna el cuadro de mensaje creado.

                Parámetros:
                - titulo_ventana: Título de la ventana del cuadro de mensaje.
                - mensaje: Mensaje a mostrar en el cuadro de mensaje.

                Retorna:
                - mbox: El cuadro de mensaje creado.
                """
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        mbox.setWindowIcon(QtGui.QIcon('./img/icono.png'))
        mbox.setText(mensaje)
        mbox.setWindowTitle(titulo_ventana)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Sí')
        mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')
        return mbox

    @staticmethod
    def crearMensajeInfo(titulo_ventana, mensaje):
        """
                Crea y muestra un cuadro de mensaje de información.

                Procedimiento:
                1. Crea un cuadro de mensaje con el título y mensaje proporcionados.
                2. Establece el icono del cuadro de mensaje como información.
                3. Establece el icono de la ventana del cuadro de mensaje.
                4. Establece los botones estándar del cuadro de mensaje a 'Aceptar'.
                5. Establece el botón predeterminado a 'Aceptar'.
                6. Cambia el texto del botón a 'Aceptar'.
                7. Muestra el cuadro de mensaje.

                Parámetros:
                - titulo_ventana: Título de la ventana del cuadro de mensaje.
                - mensaje: Mensaje a mostrar en el cuadro de mensaje.
            """
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
        mbox.setWindowIcon(QtGui.QIcon('img/icono.png'))
        mbox.setWindowTitle(titulo_ventana)
        mbox.setText(mensaje)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
        mbox.exec()

    @staticmethod
    def crearMensajeError(titulo_ventana, mensaje):
        """
                Crea y muestra un cuadro de mensaje de error.

                Procedimiento:
                1. Crea un cuadro de mensaje con el título y mensaje proporcionados.
                2. Establece el icono del cuadro de mensaje como un error crítico.
                3. Establece el icono de la ventana del cuadro de mensaje.
                4. Establece los botones estándar del cuadro de mensaje a 'Aceptar'.
                5. Establece el botón predeterminado a 'Aceptar'.
                6. Cambia el texto del botón a 'Aceptar'.
                7. Muestra el cuadro de mensaje.

                Parámetros:
                - titulo_ventana: Título de la ventana del cuadro de mensaje.
                - mensaje: Mensaje a mostrar en el cuadro de mensaje.
            """
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        mbox.setWindowIcon(QtGui.QIcon('img/icono.png'))
        mbox.setWindowTitle(titulo_ventana)
        mbox.setText(mensaje)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
        mbox.exec()

    @staticmethod
    def cargarProv():
        """
            Carga las provincias en los campos de selección de la interfaz de usuario.

            Procedimiento:
            1. Limpia los campos de selección de provincias de clientes, propiedades y delegaciones de vendedores.
            2. Obtiene la lista de provincias desde la base de datos.
            3. Asigna la lista de provincias a los campos de selección correspondientes.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de carga de provincias.
            """
        var.ui.cmbProvcli.clear()
        var.ui.cmbProvprop.clear()
        var.ui.cmbDeleVen.clear()
        listado = var.claseConexion.listaProv()
        var.provincias = listado

        var.ui.cmbProvcli.addItems(listado)
        var.ui.cmbProvprop.addItems(listado)
        var.ui.cmbDeleVen.addItems(listado)

    @staticmethod
    def cargaMunicli():
        """
            Carga los municipios en el campo de selección de la interfaz de usuario.

            Procedimiento:
            1. Limpia el campo de selección de municipios de clientes.
            2. Obtiene la lista de municipios desde la base de datos según la provincia seleccionada.
            3. Asigna la lista de municipios al campo de selección correspondiente.
            4. Configura el autocompletado del campo de selección de municipios.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de carga de municipios.
            """
        var.ui.cmbMunicli.clear()
        provinciaCli = var.ui.cmbProvcli.currentText()
        listado = var.claseConexion.listaMunicipio(provinciaCli)
        var.ui.cmbMunicli.addItems(listado)

        var.municli = listado

        completer = QtWidgets.QCompleter(var.municli, var.ui.cmbMunicli)
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        var.ui.cmbMunicli.setCompleter(completer)

    @staticmethod
    def cargaMuniprop():
        """
                Carga los municipios en el campo de selección de la interfaz de usuario.

                Procedimiento:
                1. Limpia el campo de selección de municipios de propiedades.
                2. Obtiene la lista de municipios desde la base de datos según la provincia seleccionada.
                3. Asigna la lista de municipios al campo de selección correspondiente.
                4. Configura el autocompletado del campo de selección de municipios.

                Excepciones:
                - Captura y muestra cualquier excepción que ocurra durante el proceso de carga de municipios.
                """
        var.ui.cmbMuniprop.clear()
        provinciaProp = var.ui.cmbProvprop.currentText()
        listado = var.claseConexion.listaMunicipio(provinciaProp)
        var.ui.cmbMuniprop.addItems(listado)

        var.muniprop = listado

        completer = QtWidgets.QCompleter(var.muniprop, var.ui.cmbMuniprop)
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        var.ui.cmbMuniprop.setCompleter(completer)

    @staticmethod
    def checkMunicipioCli():
        """
            Verifica si el municipio seleccionado es válido.

            Procedimiento:
            1. Comprueba si el municipio seleccionado en el campo de selección de municipios de clientes está en la lista de municipios.
            2. Si el municipio no está en la lista, establece el índice del campo de selección a 0.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de verificación del municipio.
            """
        if var.ui.cmbMunicli.currentText() not in var.municli:
            var.ui.cmbMunicli.setCurrentIndex(0)

    @staticmethod
    def checkProvinciaCli():
        """
                Verifica si la provincia seleccionada es válida.

                Procedimiento:
                1. Comprueba si la provincia seleccionada en el campo de selección de provincias de clientes está en la lista de provincias.
                2. Si la provincia no está en la lista, establece el índice del campo de selección a 0.

                Excepciones:
                - Captura y muestra cualquier excepción que ocurra durante el proceso de verificación de la provincia.
                """
        if var.ui.cmbProvcli.currentText() not in var.provincias:
            var.ui.cmbProvcli.setCurrentIndex(0)

    @staticmethod
    def checkMunicipioProp():
        """
                Verifica si el municipio seleccionado es válido.

                Procedimiento:
                1. Comprueba si el municipio seleccionado en el campo de selección de municipios de propiedades está en la lista de municipios.
                2. Si el municipio no está en la lista, establece el índice del campo de selección a 0.

                Excepciones:
                - Captura y muestra cualquier excepción que ocurra durante el proceso de verificación del municipio.
                """
        if var.ui.cmbMuniprop.currentText() not in var.muniprop:
            var.ui.cmbMuniprop.setCurrentIndex(0)

    @staticmethod
    def checkProvinciaProp():
        """
                Verifica si la provincia seleccionada es válida.

                Procedimiento:
                1. Comprueba si la provincia seleccionada en el campo de selección de provincias de propiedades está en la lista de provincias.
                2. Si la provincia no está en la lista, establece el índice del campo de selección a 0.

                Excepciones:
                - Captura y muestra cualquier excepción que ocurra durante el proceso de verificación de la provincia.
                """
        if var.ui.cmbProvprop.currentText() not in var.provincias:
            var.ui.cmbProvprop.setCurrentIndex(0)

    @staticmethod
    def checkProvinciaVen():
        """
            Verifica si la provincia seleccionada es válida.

            Procedimiento:
            1. Comprueba si la provincia seleccionada en el campo de selección de provincias de vendedores está en la lista de provincias.
            2. Si la provincia no está en la lista, establece el índice del campo de selección a 0.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de verificación de la provincia.
            """
        if var.ui.cmbDeleVen.currentText() not in var.provincias:
            var.ui.cmbDeleVen.setCurrentIndex(0)

    @staticmethod
    def isDniValido(dni):
        """
                Verifica si un DNI es válido.

                Procedimiento:
                1. Convierte el DNI a mayúsculas.
                2. Establece el DNI en el campo de texto correspondiente.
                3. Define la tabla de caracteres de control y los dígitos especiales.
                4. Reemplaza los dígitos especiales por sus valores numéricos.
                5. Verifica si el DNI tiene 9 caracteres.
                6. Extrae el dígito de control y los dígitos del DNI.
                7. Comprueba si el primer carácter es un dígito especial y lo reemplaza.
                8. Verifica si los dígitos son numéricos y si el dígito de control es correcto.
                9. Retorna True si el DNI es válido, False en caso contrario.

                Parámetros:
                - dni: El DNI a verificar.

                Retorna:
                - True si el DNI es válido, False en caso contrario.

                Excepciones:
                - Captura y muestra cualquier excepción que ocurra durante el proceso de validación del DNI.
            """
        try:
            dni = str(dni).upper()
            var.ui.txtDnicli.setText(str(dni))
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if dni.isdigit() and tabla[int(dni) % 23] == dig_control:
                    return True
                else:
                    return False
            else:
                return False

        except Exception as error:
            print("error en validar dni ", error)

    @staticmethod
    def isMovilValido(movil):
        """
            Verifica si un número de móvil es válido.

            Procedimiento:
            1. Define una expresión regular para validar números de móvil que comiencen con 6 o 7 y tengan 9 dígitos.
            2. Comprueba si el número de móvil coincide con la expresión regular.

            Parámetros:
            - movil: Número de móvil a verificar.

            Retorna:
            - True si el número de móvil es válido, False en caso contrario.
            """
        regex = r"^[67]\d{8}$"
        return re.fullmatch(regex, movil)

    @staticmethod
    def cargarTick():
        """
            Carga la imagen de un tick.

            Procedimiento:
            1. Crea un objeto QPixmap con la imagen del tick.

            @return: QPixmap con la imagen del tick.
            """
        pixmap = QPixmap("img/tick.svg")
        return pixmap

    @staticmethod
    def cargarCruz():
        """
            Carga la imagen de una cruz.

            Procedimiento:
            1. Crea un objeto QPixmap con la imagen de la cruz.

            @return: QPixmap con la imagen de la cruz.
            """
        pixmap = QPixmap("img/cruz.svg")
        return pixmap

    @staticmethod
    def abrirCalendar(pan, btn):
        """
            Abre el calendario y lo muestra en la interfaz de usuario.

            Procedimiento:
            1. Establece el panel y el botón en las variables globales.
            2. Muestra el calendario en la interfaz de usuario.

            Parámetros:
            - pan: Panel donde se mostrará el calendario.
            - btn: Botón que activa la apertura del calendario.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de apertura del calendario.

            @param pan: Panel donde se mostrará el calendario.
            @param btn: Botón que activa la apertura del calendario.
            @return: None
            """
        try:
            var.panel = pan
            var.btn = btn
            var.uicalendar.show()
        except Exception as error:
            print("error en abrir calendar ", error)

    @staticmethod
    def cargaFecha(qDate):
        """
            Carga la fecha seleccionada en el calendario en el campo correspondiente de la interfaz de usuario.

            Procedimiento:
            1. Formatea la fecha seleccionada en el calendario.
            2. Dependiendo del panel y botón seleccionados, asigna la fecha formateada al campo correspondiente.
            3. Si la fecha de inicio de alquiler es mayor que la fecha de fin, muestra un mensaje de error.
            4. Si la fecha de fin de alquiler es menor que la fecha de inicio, muestra un mensaje de error.
            5. Oculta el calendario después de un breve retraso.

            Parámetros:
            - qDate: La fecha seleccionada en el calendario (QDate).

            Retorna:
            - data: La fecha formateada como cadena (str).

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de carga de la fecha.
            """
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if var.panel == 0 and var.btn == 0:
                var.ui.txtAltacli.setText(str(data))
            elif var.panel == 1 and var.btn == 0:
                var.ui.txtAltaprop.setText(str(data))
            elif var.panel == 2 and var.btn == 0:
                var.ui.txtAltaVen.setText(str(data))
            elif var.panel == 0 and var.btn == 1:
                var.ui.txtBajacli.setText(str(data))
            elif var.panel == 1 and var.btn == 1:
                var.ui.txtBajaprop.setText(str(data))
            elif var.panel == 2 and var.btn == 1:
                var.ui.txtBajaVen.setText(str(data))
            elif var.panel == 3 and var.btn == 0:
                var.ui.txtFechaFactura.setText(str(data))
            elif var.panel == 4 and var.btn == 0:
                fecha_fin_text = var.ui.txtFinAlquiler.text()
                if fecha_fin_text:
                    fecha_fin = datetime.strptime(fecha_fin_text, '%d/%m/%Y')
                    fecha_inicio = datetime.strptime(data, '%d/%m/%Y')
                    if fecha_inicio > fecha_fin:
                        var.ui.txtInicioAlquiler.setStyleSheet('color: red;')
                        var.ui.txtInicioAlquiler.setStyleSheet('background-color: rgb(254, 255, 210);')
                        mbox = Eventos.crearMensajeError('Fecha Incorrecta',
                                                         "La fecha de inicio de alquiler no puede ser mayor a la de fin.")
                        mbox.exec()
                    else:
                        var.ui.txtInicioAlquiler.setStyleSheet('')
                        var.ui.txtInicioAlquiler.setStyleSheet('background-color: rgb(254, 255, 210);')
                var.ui.txtInicioAlquiler.setText(str(data))
            elif var.panel == 4 and var.btn == 1:
                fecha_inicio_text = var.ui.txtInicioAlquiler.text()
                if fecha_inicio_text:
                    fecha_inicio = datetime.strptime(fecha_inicio_text, '%d/%m/%Y')
                    fecha_fin = datetime.strptime(data, '%d/%m/%Y')
                    if fecha_fin < fecha_inicio:
                        var.ui.txtFinAlquiler.setStyleSheet('color: red;')
                        var.ui.txtFinAlquiler.setStyleSheet('background-color: rgb(254, 255, 210);')
                        mbox = Eventos.crearMensajeError('Fecha Incorrecta',
                                                         "La fecha de fin de alquiler no puede ser anterior a la de inicio.")
                        mbox.exec()
                    else:
                        var.ui.txtFinAlquiler.setStyleSheet('')
                        var.ui.txtFinAlquiler.setStyleSheet('background-color: rgb(254, 255, 210);')
                var.ui.txtFinAlquiler.setText(str(data))
            time.sleep(0.5)
            var.uicalendar.hide()
            return data
        except Exception as error:
            print("error en cargar fecha: ", error)

    @staticmethod
    def isMailValido(mail):
        """
           Verifica si un correo electrónico es válido.

           Procedimiento:
           1. Convierte el correo electrónico a minúsculas.
           2. Define una expresión regular para validar el formato del correo electrónico.
           3. Comprueba si el correo electrónico coincide con la expresión regular o si está vacío.

           Parámetros:
           - mail: Correo electrónico a verificar.

           Retorna:
           - True si el correo electrónico es válido o está vacío, False en caso contrario.
           """
        mail = mail.lower()
        regex = r'^([a-z0-9]+[\._])*[a-z0-9]+[@](\w+[.])*\w+$'
        if re.match(regex, mail) or mail == "":
            return True
        else:
            return False

    @staticmethod
    def resizeTablaClientes():
        """
            Ajusta el tamaño de las columnas de la tabla de clientes.

            Procedimiento:
            1. Obtiene el encabezado horizontal de la tabla de clientes.
            2. Recorre cada columna del encabezado.
            3. Si la columna no está en las posiciones 0, 3 o 6, ajusta su tamaño para que se estire.
            4. Si la columna está en las posiciones 0, 3 o 6, ajusta su tamaño para que se ajuste al contenido.
            5. Establece la fuente de los elementos del encabezado en negrita.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de ajuste de tamaño de las columnas.

            @param None
            @return None
            """
        try:
            header = var.ui.tablaClientes.horizontalHeader()
            for i in range(header.count()):
                if i not in (0, 3, 6):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_items = var.ui.tablaClientes.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as e:
            print("error en resize tabla clientes ", e)

    @staticmethod
    def resizeTablaPropiedades():
        """
                Ajusta el tamaño de las columnas de la tabla de propiedades.

                Procedimiento:
                1. Obtiene el encabezado horizontal de la tabla de propiedades.
                2. Recorre cada columna del encabezado.
                3. Si la columna está en las posiciones 1, 2 o 7, ajusta su tamaño para que se estire.
                4. Si la columna no está en las posiciones 1, 2 o 7, ajusta su tamaño para que se ajuste al contenido.
                5. Establece la fuente de los elementos del encabezado en negrita.

                Excepciones:
                - Captura y muestra cualquier excepción que ocurra durante el proceso de ajuste de tamaño de las columnas.

                @param None
                @return None
            """
        try:
            header = var.ui.tablaProp.horizontalHeader()
            for i in range(header.count()):
                if i in (1, 2, 7):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_items = var.ui.tablaProp.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as e:
            print("error en resize tabla clientes ", e)

    @staticmethod
    def resizeTablaVendedores():
        """
           Ajusta el tamaño de las columnas de la tabla de vendedores.

           Procedimiento:
           1. Obtiene el encabezado horizontal de la tabla de vendedores.
           2. Recorre cada columna del encabezado.
           3. Si la columna no está en las posiciones 0, 2 o 4, ajusta su tamaño para que se estire.
           4. Si la columna está en las posiciones 0, 2 o 4, ajusta su tamaño para que se ajuste al contenido.
           5. Establece la fuente de los elementos del encabezado en negrita.

           Excepciones:
           - Captura y muestra cualquier excepción que ocurra durante el proceso de ajuste de tamaño de las columnas.

           @param None
           @return None
           """
        try:
            header = var.ui.tablaVendedores.horizontalHeader()
            for i in range(header.count()):
                if i not in (0, 2, 4):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_items = var.ui.tablaVendedores.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as e:
            print("error en resize tabla clientes ", e)

    @staticmethod
    def resizeTablaFacturas():
        """
            Ajusta el tamaño de las columnas de la tabla de facturas.

            Procedimiento:
            1. Obtiene el encabezado horizontal de la tabla de facturas.
            2. Recorre cada columna del encabezado.
            3. Si la columna no está en la posición 0, ajusta su tamaño para que se estire.
            4. Si la columna está en la posición 0, ajusta su tamaño para que se ajuste al contenido.
            5. Establece la fuente de los elementos del encabezado en negrita.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de ajuste de tamaño de las columnas.

            @param None
            @return None
            """
        try:
            header = var.ui.tablaFacturas.horizontalHeader()
            for i in range(header.count()):
                if i != 0:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_items = var.ui.tablaVendedores.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as e:
            print("error en resize tabla clientes ", e)

    @staticmethod
    def resizeTablaVentas_3():
        """
            Ajusta el tamaño de las columnas de la tabla de ventas.

            Procedimiento:
            1. Obtiene el encabezado horizontal de la tabla de ventas.
            2. Recorre cada columna del encabezado.
            3. Si la columna no está en la posición 0, ajusta su tamaño para que se estire.
            4. Si la columna está en la posición 0, ajusta su tamaño para que se ajuste al contenido.
            5. Establece la fuente de los elementos del encabezado en negrita.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de ajuste de tamaño de las columnas.

            @param None
            @return None
            """
        try:
            header = var.ui.tablaVentas.horizontalHeader()
            for i in range(header.count()):
                if i != 0:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                header_items = var.ui.tablaVentas.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)
        except Exception as e:
            print("error en resize tabla ventas3 ", e)

    @staticmethod
    def crearBackup():
        """
            Crea una copia de seguridad de la base de datos en un archivo ZIP.

            Procedimiento:
            1. Obtiene la fecha y hora actual y la formatea.
            2. Genera el nombre del archivo ZIP de la copia de seguridad.
            3. Abre un cuadro de diálogo para seleccionar la ubicación y el nombre del archivo ZIP.
            4. Si se acepta el cuadro de diálogo y se selecciona un archivo, crea el archivo ZIP y guarda la base de datos en él.
            5. Muestra un mensaje de confirmación si la copia de seguridad se crea correctamente.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de creación de la copia de seguridad.

            @param None
            @return None
            """
        try:
            fecha = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            copia = str(fecha) + '_backup.zip'
            directorio, fichero = var.dlgAbrir.getSaveFileName(None, "Guardar Copia Seguridad", copia, '.zip')
            if var.dlgAbrir.accept and fichero:
                fichzip = zipfile.ZipFile(fichero, 'w')
                fichzip.write("bbdd.sqlite", os.path.basename("bbdd.sqlite"), zipfile.ZIP_DEFLATED)
                fichzip.close()
                shutil.move(fichero, directorio)

                mbox = Eventos.crearMensajeInfo('Copia de seguridad', "Copia de seguridad creada.")
                mbox.exec()

        except Exception as error:
            print("error en crear backup: ", error)

    @staticmethod
    def restaurarBackup():
        """
            Restaura una copia de seguridad de la base de datos desde un archivo ZIP.

            Procedimiento:
            1. Abre un cuadro de diálogo para seleccionar el archivo ZIP de la copia de seguridad.
            2. Si se selecciona un archivo, extrae el contenido del archivo ZIP.
            3. Muestra un mensaje de confirmación si la restauración se realiza correctamente.
            4. Reconecta la base de datos y recarga las provincias y la tabla de clientes.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de restauración de la copia de seguridad.

            @param None
            @return None
            """
        try:
            filename = var.dlgAbrir.getOpenFileName(None, "Restaurar Copia Seguridad", "", "*.zip;;All Files (*)")
            file = filename[0]
            if file:
                with zipfile.ZipFile(file, 'r') as bbdd:
                    bbdd.extractall(pwd=None)
                bbdd.close()
                mbox = Eventos.crearMensajeInfo('Copia de seguridad', "Copia de seguridad restaurada.")
                mbox.exec()
                conexion.Conexion.db_conexion()
                eventos.Eventos.cargarProv()
                clientes.Clientes.cargaTablaClientes()
        except Exception as error:
            print("error en restaurar backup: ", error)

    @staticmethod
    def limpiarPanel():
        """
            Limpia los campos de los paneles de clientes, propiedades y vendedores en la interfaz de usuario.

            Procedimiento:
            1. Limpia los campos de texto y selección del panel de clientes.
            2. Limpia los campos de texto y selección del panel de propiedades.
            3. Limpia los campos de texto y selección del panel de vendedores.
            4. Limpia los campos de texto y selección del panel de ventas
            5. Limpia los campos de texto y selección del panel de alquileres
            6. Recarga las provincias en los campos de selección.
            7. Recarga las tablas de propiedades y vendedores.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de limpieza de los paneles.

            @param None
            @return None
            """
        import propiedades
        objetosPanelCli = [var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli, var.ui.txtNomcli,
                           var.ui.txtEmailcli, var.ui.txtMovilcli, var.ui.txtDircli, var.ui.cmbProvcli,
                           var.ui.cmbMunicli, var.ui.txtBajacli]
        for i, dato in enumerate(objetosPanelCli):
            if i in (7, 8):
                pass
            else:
                dato.setText("")

        var.ui.lblTickcli.clear()
        var.ui.txtDnicli.setStyleSheet(
            'border: 1px solid black; border-radius: 5px; background-color: rgb(254, 255, 210)')
        var.ui.txtDnicli.setPlaceholderText("")
        var.ui.txtMovilcli.setPlaceholderText("")
        var.ui.txtMovilcli.setStyleSheet('border: 1px solid black; border-radius: 5px;')
        var.ui.txtEmailcli.setPlaceholderText("")
        var.ui.txtEmailcli.setStyleSheet('border: 1px solid black; border-radius: 5px;')

        objetosPanelProp = [var.ui.lblProp, var.ui.txtAltaprop, var.ui.txtBajaprop, var.ui.txtDirprop,
                            var.ui.cmbProvprop,
                            var.ui.cmbMuniprop, var.ui.cmbTipoprop,
                            var.ui.spinHabprop, var.ui.spinBanosprop, var.ui.txtSuperprop, var.ui.txtPrecioAlquilerprop,
                            var.ui.txtPrecioVentaprop,
                            var.ui.txtCpprop, var.ui.areatxtDescriprop, var.ui.rbtDisponprop, var.ui.rbtAlquilprop,
                            var.ui.chkVentaprop, var.ui.chkInterprop,
                            var.ui.chkAlquilprop, var.ui.rbtVentaprop, var.ui.txtNomeprop, var.ui.txtMovilprop]
        for i, dato in enumerate(objetosPanelProp):
            if i in (4, 5, 6):
                pass
            elif i in (7, 8):
                dato.setValue(0)
            elif i == 13:
                dato.setPlainText("")
            elif i == 14:
                dato.setChecked(True)
            elif i in (15, 16, 17, 18, 19):
                dato.setChecked(False)
            else:
                dato.setText("")

        var.ui.btnBuscaTipoProp.setChecked(False)
        propiedades.Propiedades.cargarTablaPropiedades()

        objetosPanelVendedores = [var.ui.lblIdVen, var.ui.txtDniVen, var.ui.txtNomVen, var.ui.txtAltaVen,
                                  var.ui.txtBajaVen,
                                  var.ui.txtMovilVen, var.ui.txtEmailVen, var.ui.cmbDeleVen]
        for i, dato in enumerate(objetosPanelVendedores):
            if i == 7:
                pass
            else:
                dato.setText("")

        eventos.Eventos.cargarProv()
        var.ui.chkHistoriaVen.setChecked(False)
        vendedores.Vendedores.cargaTablaVendedores()

        # 🔴 Limpiar panel de Ventas
        objetosPanelVentas = [
            var.ui.lblNumFactura, var.ui.lblSubTotal, var.ui.lblIVA, var.ui.lblTotal,  # QLabel
            var.ui.txtFechaFactura, var.ui.txtdniclifac, var.ui.txtCliApel, var.ui.txtCliNom,  # QLineEdit
            var.ui.txtIdVendedor, var.ui.txtCodProp, var.ui.txtTipoProp, var.ui.txtPrecioProp,
            var.ui.txtDirProp, var.ui.txtLocProp
        ]

        for dato in objetosPanelVentas:
            if isinstance(dato, QtWidgets.QLabel):  # Limpiar labels
                dato.clear()
            elif isinstance(dato, QtWidgets.QLineEdit):  # Limpiar campos de texto
                dato.setText("")

        # Recargar Provincias
        eventos.Eventos.cargarProv()

        # 🏠💰 Limpiar panel de Alquileres
        objetosPanelAlquileres = [
            var.ui.txtNumAlquiler, var.ui.txtInicioAlquiler, var.ui.txtFinAlquiler,  # Fechas y número de alquiler
            var.ui.txtDniClienteAlquiler, var.ui.txtIdPropiedadAlquiler, var.ui.txtVendedorAlquiler,
            # Cliente, propiedad y vendedor
            var.ui.txtPrecioAlquiler  # Precio
        ]

        for dato in objetosPanelAlquileres:
            dato.setText("")

        # Limpiar tabla de visualización de alquileres
        var.ui.pnlVisualizacionAlquileres.clearContents()
        var.ui.pnlVisualizacionAlquileres.setRowCount(0)

        # Recargar Provincias
        eventos.Eventos.cargarProv()



    @staticmethod
    def abrirTipoprop():
        """
            Abre el diálogo de gestión de tipos de propiedades.

            Procedimiento:
            1. Muestra el diálogo de gestión de tipos de propiedades.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de apertura del diálogo.

            @param None
            @return None
            """
        try:
            var.dlggestion.show()
        except Exception as e:
            print("error en abrir tipo prop: ", e)

    @staticmethod
    def exportCSVprop():
        """
            Exporta los datos de las propiedades a un archivo CSV.

            Procedimiento:
            1. Obtiene la fecha y hora actual y la formatea.
            2. Genera el nombre del archivo CSV de la exportación.
            3. Abre un cuadro de diálogo para seleccionar la ubicación y el nombre del archivo CSV.
            4. Si se acepta el cuadro de diálogo y se selecciona un archivo, crea el archivo CSV y guarda los datos de las propiedades en él.
            5. Muestra un mensaje de error si ocurre algún problema durante la exportación.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de exportación de datos a CSV.

            @param None
            @return None
            """
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = str(fecha) + '_DatosPropiedades.csv'
            directorio, fichero = var.dlgAbrir.getSaveFileName(None, "Exporta Datos a CSV", file, '.csv')
            if fichero:
                registros = var.claseConexion.cargarAllPropiedadesBD()
                with open(fichero, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(
                        ["Codigo", "Alta", "Baja", "Dirección", "Provincia", "Municipio", "Tipo", "Nº habitaciones",
                         "Nº Baños", "Superficie", "Precio Alquiler", "Precio Compra", "Código postal", "Observaciones",
                         "Operación", "Estado", "Propietario", "Móvil"])
                    for registro in registros:
                        writer.writerow(registro)
                shutil.move(fichero, directorio)
            else:
                eventos.Eventos.crearMensajeError("Error",
                                                  "Se ha producido un error al exportar los datos en formato CSV.")
        except Exception as e:
            print("error en exportar cvs tipo prop: ", e)

    @staticmethod
    def exportJSONprop():
        """
            Exporta los datos de las propiedades a un archivo JSON.

            Procedimiento:
            1. Obtiene la fecha y hora actual y la formatea.
            2. Genera el nombre del archivo JSON de la exportación.
            3. Abre un cuadro de diálogo para seleccionar la ubicación y el nombre del archivo JSON.
            4. Si se acepta el cuadro de diálogo y se selecciona un archivo, crea el archivo JSON y guarda los datos de las propiedades en él.
            5. Muestra un mensaje de error si ocurre algún problema durante la exportación.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de exportación de datos a JSON.

            @param None
            @return None
            """
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = str(fecha) + '_DatosPropiedades.json'
            directorio, fichero = var.dlgAbrir.getSaveFileName(None, "Exporta Datos a JSON", file, '.json')
            if fichero:
                keys = ["Codigo", "Alta", "Baja", "Dirección", "Provincia", "Municipio", "Tipo", "Nº habitaciones",
                        "Nº Baños", "Superficie", "Precio Alquiler", "Precio Compra", "Código postal", "Observaciones",
                        "Operación", "Estado", "Propietario", "Móvil"]
                registros = var.claseConexion.cargarAllPropiedadesBD()
                lista_propiedades = [dict(zip(keys, registro)) for registro in registros]
                with open(fichero, 'w', newline='', encoding='utf-8') as jsonFile:
                    json.dump(lista_propiedades, jsonFile, ensure_ascii=False, indent=4)
                shutil.move(fichero, directorio)
            else:
                eventos.Eventos.crearMensajeError("Error",
                                                  "Se ha producido un error al exportar los datos en formato JSON.")
        except Exception as e:
            print("error en exportar cvs tipo prop: ", e)

    @staticmethod
    def abrir_informeProp():
        """
            Abre el diálogo de informe de propiedades.

            Procedimiento:
            1. Muestra el diálogo de informe de propiedades.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de apertura del diálogo.

            @param None
            @return None
            """
        try:
            var.dlgInformeProp.show()
        except Exception as e:
            print("error en abrir informe propiedades: ", e)

    @staticmethod
    def abrir_about():
        """
                Abre el diálogo de información 'Acerca de'.

                Procedimiento:
                1. Muestra el diálogo de información 'Acerca de'.

                Excepciones:
                - Captura y muestra cualquier excepción que ocurra durante el proceso de apertura del diálogo.

                @param None
                @return None
                """
        try:
            var.dlgabout.show()
        except Exception as e:
            print("error en abrir about: ", e)

    @staticmethod
    def siguienteCli():
        """
               Avanza a la siguiente página de la tabla de clientes.

               Procedimiento:
               1. Incrementa el número de la página actual de clientes.
               2. Carga los datos de la tabla de clientes para la nueva página.

               Parámetros:
               - Ninguno

               Retorna:
               - Ninguno
               """
        var.paginaActualCli += 1
        clientes.Clientes.cargaTablaClientes()

    @staticmethod
    def anteriorCli():
        """
            Retrocede a la página anterior de la tabla de clientes.

            Procedimiento:
            1. Verifica si la página actual es mayor que 0.
            2. Si es mayor que 0, decrementa el número de la página actual.
            3. Carga los datos de la tabla de clientes para la nueva página.

            Parámetros:
            - Ninguno

            Retorna:
            - Ninguno
            """
        if var.paginaActualCli > 0:
            var.paginaActualCli -= 1
            clientes.Clientes.cargaTablaClientes()

    @staticmethod
    def siguienteProp():
        """
            Avanza a la siguiente página de la tabla de propiedades.

            Procedimiento:
            1. Incrementa el número de la página actual de propiedades.
            2. Carga los datos de la tabla de propiedades para la nueva página.

            Parámetros:
            - Ninguno

            Retorna:
            - Ninguno
            """
        import propiedades
        var.paginaActualProp += 1
        propiedades.Propiedades.cargarTablaPropiedades()

    @staticmethod
    def anteriorProp():
        """
            Retrocede a la página anterior de la tabla de propiedades.

            Procedimiento:
            1. Verifica si la página actual es mayor que 0.
            2. Si es mayor que 0, decrementa el número de la página actual.
            3. Carga los datos de la tabla de propiedades para la nueva página.

            Parámetros:
            - Ninguno

            Retorna:
            - Ninguno
            """
        import propiedades
        if var.paginaActualProp > 0:
            var.paginaActualProp -= 1
            propiedades.Propiedades.cargarTablaPropiedades()

    @staticmethod
    def cambiarCliMaxpPagina():
        """
            Cambia el número máximo de clientes por página y recarga la tabla de clientes.

            Procedimiento:
            1. Establece la página actual de clientes a 0.
            2. Obtiene el valor del campo de texto correspondiente al número máximo de clientes por página.
            3. Si el valor es mayor que 15, lo establece a 15.
            4. Recarga la tabla de clientes con el nuevo valor.

            Parámetros:
            - Ninguno

            Retorna:
            - Ninguno
            """
        var.paginaActualCli = 0
        var.maxClientesPagina = int(var.ui.spinClipPag.text())
        if var.maxClientesPagina > 15:
            var.maxClientesPagina = 15
        clientes.Clientes.cargaTablaClientes()

    @staticmethod
    def cambiarPropMaxpPagina():
        """
            Cambia el número máximo de propiedades por página y recarga la tabla de propiedades.

            Procedimiento:
            1. Establece la página actual de propiedades a 0.
            2. Obtiene el valor del campo de texto correspondiente al número máximo de propiedades por página.
            3. Si el valor es mayor que 10, lo establece a 10.
            4. Recarga la tabla de propiedades con el nuevo valor.

            Parámetros:
            - Ninguno

            Retorna:
            - Ninguno
            """
        import propiedades
        var.paginaActualProp = 0
        var.maxPropPagina = int(var.ui.spinProppPag.text())
        if var.maxPropPagina > 10:
            var.maxPropPagina = 10
        propiedades.Propiedades.cargarTablaPropiedades()

    @staticmethod
    def exportJSONven():
        """
            Exporta los datos de los vendedores a un archivo JSON.

            Procedimiento:
            1. Obtiene la fecha y hora actual y la formatea.
            2. Genera el nombre del archivo JSON de la exportación.
            3. Abre un cuadro de diálogo para seleccionar la ubicación y el nombre del archivo JSON.
            4. Si se acepta el cuadro de diálogo y se selecciona un archivo, crea el archivo JSON y guarda los datos de los vendedores en él.
            5. Muestra un mensaje de error si ocurre algún problema durante la exportación.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de exportación de datos a JSON.

            @param None
            @return None
            """
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = str(fecha) + '_DatosVendedores.json'
            directorio, fichero = var.dlgAbrir.getSaveFileName(None, "Exporta Datos a JSON", file, '.json')
            if fichero:
                keys = ["Id", "Dni", "Nombre", "Alta", "Baja", "Movil", "Email", "Delegacion"]
                registros = var.claseConexion.cargarAllVendedoresBD()
                lista_propiedades = [dict(zip(keys, registro)) for registro in registros]
                with open(fichero, 'w', newline='', encoding='utf-8') as jsonFile:
                    json.dump(lista_propiedades, jsonFile, ensure_ascii=False, indent=4)
                shutil.move(fichero, directorio)
            else:
                eventos.Eventos.crearMensajeError("Error",
                                                  "Se ha producido un error al exportar los datos en formato JSON.")
        except Exception as e:
            print("error en exportar cvs tipo prop: ", e)

    @staticmethod
    def resizeTablaAlquileresGestion():
        """
            Ajusta el tamaño de las columnas de la tabla de gestión de alquileres.

            Procedimiento:
            1. Obtiene el encabezado horizontal de la tabla de gestión de alquileres.
            2. Recorre cada columna del encabezado.
            3. Si la columna no está en las posiciones 0 o 2, ajusta su tamaño para que se estire.
            4. Si la columna está en las posiciones 0 o 2, ajusta su tamaño para que se ajuste al contenido.
            5. Establece la fuente de los elementos del encabezado en negrita.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de ajuste de tamaño de las columnas.

            @param None
            @return None
            """
        try:
            header = var.ui.pnlGestionAlquileres.horizontalHeader()
            for i in range(header.count()):
                if i not in (0, 2):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_items = var.ui.pnlGestionAlquileres.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)
        except Exception as e:
            print("error en resize tabla clientes ", e)

    @staticmethod
    def pnlVisualizacionAlquileres():
        """
                Ajusta el tamaño de las columnas de la tabla de visualización de alquileres.

                Procedimiento:
                1. Obtiene el encabezado horizontal de la tabla de visualización de alquileres.
                2. Recorre cada columna del encabezado.
                3. Si la columna no está en la posición 0, ajusta su tamaño para que se estire.
                4. Si la columna está en la posición 0, ajusta su tamaño para que se ajuste al contenido.
                5. Establece la fuente de los elementos del encabezado en negrita.

                Excepciones:
                - Captura y muestra cualquier excepción que ocurra durante el proceso de ajuste de tamaño de las columnas.

                @param None
                @return None
            """
        try:
            header_labels = ['Recibo', 'Propiedad', 'Mensualidad', 'Importe', 'Gestión']
            var.ui.pnlVisualizacionAlquileres.setHorizontalHeaderLabels(header_labels)

            header = var.ui.pnlVisualizacionAlquileres.horizontalHeader()
            for i in range(header.count()):
                if i != 0:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_items = var.ui.pnlVisualizacionAlquileres.horizontalHeaderItem(i)
                if header_items is not None:
                    font = header_items.font()
                    font.setBold(True)
                    header_items.setFont(font)
        except Exception as e:
            print("error en resize visualizacion alquileres ", e)
