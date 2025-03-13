from mailbox import mboxMessage

from PyQt6.QtWidgets import QHBoxLayout, QWidget
from PyQt6 import QtGui
from PyQt6.QtGui import QIcon
from reportlab.lib.testutils import setOutDir

import conexion
import informes
import propiedades
import eventos
import var
from PyQt6 import QtWidgets, QtCore


class Alquileres:

    @staticmethod
    def altaAlquiler():
        """
            Esta función se encarga de registrar un nuevo contrato de alquiler.

            Procedimiento:
            1. Recopila los datos del nuevo alquiler desde la interfaz de usuario.
            2. Verifica que todos los campos requeridos no estén vacíos.
            3. Si algún campo está vacío, muestra un mensaje de error específico.
            4. Si todos los campos están completos, intenta registrar el nuevo contrato de alquiler en la base de datos.
            5. Si el registro es exitoso, actualiza las tablas de contratos y mensualidades, y ajusta el tamaño de las tablas.
            6. Limpia los campos de entrada en la interfaz de usuario.
            7. Si ocurre un error durante el registro, muestra un mensaje de error.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de registro.

            """
        try:
            nuevoAlquiler = [
                var.ui.txtIdPropiedadAlquiler.text(),
                var.ui.txtDniClienteAlquiler.text(),
                var.ui.txtVendedorAlquiler.text(),
                var.ui.txtInicioAlquiler.text(),
                var.ui.txtFinAlquiler.text(),
                var.ui.txtPrecioAlquiler.text(),
            ]

            # print("Nuevo Alquiler:", nuevoAlquiler)

            # Verificamos que los campos no estén vacíos antes de grabar el contrato
            if nuevoAlquiler[0] == "":
                eventos.Eventos.crearMensajeError("Error grabar el contrato",
                                                  "Recuerda ingresar el ID de la propiedad")
                return

            elif nuevoAlquiler[1] == "":
                eventos.Eventos.crearMensajeError("Error grabar el contrato",
                                                  "Recuerda ingresar el DNI del cliente")
                return

            elif nuevoAlquiler[2] == "":
                eventos.Eventos.crearMensajeError("Error grabar el contrato",
                                                  "Recuerda ingresar el vendedor")
                return

            elif nuevoAlquiler[3] == "":
                eventos.Eventos.crearMensajeError("Error grabar el contrato",
                                                  "Recuerda ingresar la fecha de inicio del alquiler")
                return

            elif nuevoAlquiler[4] == "":
                eventos.Eventos.crearMensajeError("Error grabar el contrato",
                                                  "Recuerda ingresar la fecha de fin del alquiler")
                return

            elif nuevoAlquiler[5] == "":
                eventos.Eventos.crearMensajeError("Error grabar el contrato",
                                                  "Recuerda ingresar el precio del alquiler")
                return

            # print( f"Nuevo Alquiler: ID Propiedad: {nuevoAlquiler[0]}, DNI Cliente: {nuevoAlquiler[1]}, Vendedor: {nuevoAlquiler[2]}, Fecha Inicio: {nuevoAlquiler[3]}, Fecha Fin: {nuevoAlquiler[4]}, Precio: {nuevoAlquiler[5]}")
            if conexion.Conexion.altaContratoAlquiler(nuevoAlquiler):
                eventos.Eventos.crearMensajeInfo("Contrato grabado", "Se ha grabado una nueva venta")

                # idPropiedad = conexion.Conexion.getIdAlquilerByPropiedad(nuevoAlquiler[0])
                # print("ID Propiedad:", nuevoAlquiler[0])

                var.ui.pnlVisualizacionAlquileres.clear()

                Alquileres.cargaTablaContratos()
                Alquileres.cargaTablaMensualidades(nuevoAlquiler[0])
                propiedades.Propiedades.cargarTablaPropiedades()

                eventos.Eventos.resizeTablaAlquileresGestion()
                eventos.Eventos.pnlVisualizacionAlquileres()

                var.ui.txtIdPropiedadAlquiler.clear()
                var.ui.txtDniClienteAlquiler.clear()
                var.ui.txtVendedorAlquiler.clear()
                var.ui.txtInicioAlquiler.clear()
                var.ui.txtFinAlquiler.clear()
                var.ui.txtPrecioAlquiler.clear()


            else:
                eventos.Eventos.crearMensajeError("Error", "No se ha podido grabar el contrato de alquiler")
        except Exception as e:
            print("venta", e)

    @staticmethod
    def cargaTablaContratos():
        """
               Esta función carga los contratos de alquiler en la tabla de gestión de alquileres.

               Procedimiento:
               1. Obtiene el listado de contratos de alquiler desde la base de datos.
               2. Configura el número de filas y columnas de la tabla.
               3. Establece los encabezados de las columnas.
               4. Rellena la tabla con los datos de los contratos.
               5. Añade un botón de eliminar en cada fila para gestionar la eliminación de contratos.

               Excepciones:
               - Captura y muestra cualquier excepción que ocurra durante el proceso de carga de la tabla.
               """
        try:
            listado = conexion.Conexion.listadoContratosAlquileres()
            var.ui.pnlGestionAlquileres.setRowCount(len(listado))
            var.ui.pnlGestionAlquileres.setColumnCount(3)
            header = ['Nº Contrato', 'DNI Cliente', 'Gestión']
            var.ui.pnlGestionAlquileres.setHorizontalHeaderLabels(header)

            for index, registro in enumerate(listado):
                # NUM CONTRATO (id)
                item_id = QtWidgets.QTableWidgetItem(str(registro[0]))
                var.ui.pnlGestionAlquileres.setItem(index, 0, item_id)
                item_id.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                # DNI (dni del cliente)
                item_dni = QtWidgets.QTableWidgetItem(str(registro[2]))
                var.ui.pnlGestionAlquileres.setItem(index, 1, item_dni)
                item_dni.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                # Botón de eliminar en la columna Gestión
                botondelfac = QtWidgets.QPushButton()
                botondelfac.setFixedSize(25, 25)
                botondelfac.setIconSize(QtCore.QSize(25, 25))
                botondelfac.setIcon(QIcon("./img/basura.ico"))
                botondelfac.setStyleSheet("background: transparent; border: none;")
                botondelfac.setProperty("row", index)

                # Conectar el botón a la función borrarContrato
                botondelfac.clicked.connect( lambda _, id_contrato=registro[0]: conexion.Conexion.borrarContrato(id_contrato))

                contenedor = QtWidgets.QWidget()
                layout = QHBoxLayout()
                layout.addWidget(botondelfac)
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                contenedor.setLayout(layout)
                var.ui.pnlGestionAlquileres.setCellWidget(index, 2, contenedor)
                var.ui.pnlGestionAlquileres.resizeColumnsToContents()
        except Exception as e:
            print("Error en cargaTablaContratos:", e)

    @staticmethod
    def cargaTablaMensualidades(numContrato=None):
        """
            Carga las mensualidades de un contrato de alquiler en la tabla de visualización.

            @param numContrato: Número del contrato de alquiler. Si no se proporciona, se cargan todas las mensualidades.
            @type numContrato: int, optional

            @return: None
            """
        try:
            # Obtenemos el listado de mensualidades
            listado = conexion.Conexion.listadoMensualidades(numContrato)
            # print("Listado obtenido:", listado)

            if not listado:
                var.ui.pnlVisualizacionAlquileres.setRowCount(0)
                print("El listado está vacío, no se cargarán mensualidades.")
                return

            # Configuramos filas y columnas
            var.ui.pnlVisualizacionAlquileres.setRowCount(len(listado))
            var.ui.pnlVisualizacionAlquileres.setColumnCount(
                5)  # Total: recibo, propiedad, mensualidad, importe, gestión

            for index, registro in enumerate(listado):
                # Recibo (Columna 1)
                item_recibo = QtWidgets.QTableWidgetItem(str(registro[0]))  # ID de mensualidades
                var.ui.pnlVisualizacionAlquileres.setItem(index, 0, item_recibo)
                item_recibo.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                # Propiedad (Columna 2)
                item_propiedad = QtWidgets.QTableWidgetItem(str(registro[1]))
                var.ui.pnlVisualizacionAlquileres.setItem(index, 1, item_propiedad)
                item_propiedad.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                # Mensualidad (Columna 3)
                item_mensualidad = QtWidgets.QTableWidgetItem(str(registro[2]))
                var.ui.pnlVisualizacionAlquileres.setItem(index, 2, item_mensualidad)
                item_mensualidad.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                # Importe (Columna 4)
                item_importe = QtWidgets.QTableWidgetItem(str(registro[3]))
                var.ui.pnlVisualizacionAlquileres.setItem(index, 3, item_importe)
                item_importe.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                # Gestión (Columna 5: Checkbox)
                checkbox = QtWidgets.QCheckBox()
                estado_pagado = bool(int(registro[4]))  # Convertir estado a booleano
                checkbox.setChecked(estado_pagado)

                # Conectar el evento del checkbox al cambio en la base de datos
                checkbox.stateChanged.connect(
                    lambda estado, id_mensualidad=registro[0]: conexion.Conexion.actualizarEstadoMensualidad( id_mensualidad, estado) )

                checkbox_layout = QHBoxLayout()
                checkbox_layout.addWidget(checkbox)
                checkbox_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)  # Ajustar márgenes
                checkbox_container = QWidget()
                checkbox_container.setLayout(checkbox_layout)
                var.ui.pnlVisualizacionAlquileres.setCellWidget(index, 4, checkbox_container)

            # Ajustamos el tamaño de las columnas al contenido
            var.ui.pnlVisualizacionAlquileres.resizeColumnsToContents()

        except Exception as e:
            print("Error en cargaTablaMensualidades:", e)

    @staticmethod
    def cargaOneContrato():
        """
           Carga un contrato de alquiler seleccionado y sus mensualidades en la interfaz de usuario.

           @return: None
           """
        try:
            fila = var.ui.pnlGestionAlquileres.selectedItems()
            datos = [dato.text() for dato in fila]
            print("Datos seleccionados:", datos)
            try:
                mensualidades = conexion.Conexion.cargaMensualidades(datos[0]) #Obtengo el código de la propiedad
                var.ui.txtNumAlquiler.setText(datos[0])
                # print("Mensualidades:", mensualidades) #Guardamos las Mensualidades
                if mensualidades:
                    codProp = mensualidades[0][1]
                    # print("Código de la propiedad:", codProp) #Codigo de la propiedad
                    # propiedad = conexion.Conexion.listadoMensualidades(codProp)  # Recupera la propiedad a partir de su código
                    Alquileres.cargaTablaMensualidades(codProp)
                    # eventos.Eventos.resizeTablaAlquileresGestion()
                    eventos.Eventos.pnlVisualizacionAlquileres()

                else:
                    Alquileres.cargaTablaMensualidades()

            except Exception as e:
                print("Error en carga Factura", e)

        except Exception as e:
            print("Error cargaOneFactura en Facturas", e)

    @staticmethod
    def selectOneMensualidad():
        """
            Selecciona una mensualidad de la tabla de visualización de alquileres.

            @return: None
            """
        try:
            fila = var.ui.pnlVisualizacionAlquileres.selectedItems()
            datos = [dato.text() for dato in fila]
            print("Datos seleccionados:", datos)
            var.ui.txtNumRecibo.setText(datos[0]) #ID de la mensualidad

            # datos[0] = ID de la mensualidad
        except Exception as e:
            print("Error en selectOneMensualidad:", e)

    @staticmethod
    def guardarFactura():
        if not var.ui.txtNumRecibo.text() or not var.ui.txtNumAlquiler.text():
            eventos.Eventos.crearMensajeError("Error", "No hay ninguna alquiler o contrato seleccionado")
            print("txtNumRecibo no tiene valor o txtNumAlquiler no tiene valor")
            return
        informes.Informes.reportReciboMensualidad(var.ui.txtNumAlquiler.text(),var.ui.txtNumRecibo.text())