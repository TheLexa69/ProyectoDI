from mailbox import mboxMessage

from PyQt6.QtWidgets import QHBoxLayout, QWidget
from PyQt6 import QtGui
from PyQt6.QtGui import QIcon
from reportlab.lib.testutils import setOutDir

import conexion
import propiedades
import eventos
import var
from PyQt6 import QtWidgets, QtCore


class Alquileres:

    @staticmethod
    def altaAlquiler():
        try:
            nuevoAlquiler = [
                var.ui.txtIdPropiedadAlquiler.text(),
                var.ui.txtDniClienteAlquiler.text(),
                var.ui.txtVendedorAlquiler.text(),
                var.ui.txtInicioAlquiler.text(),
                var.ui.txtFinAlquiler.text(),
                var.ui.txtPrecioAlquiler.text(),
            ]

            print("Nuevo Alquiler:", nuevoAlquiler)

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

            print(
                f"Nuevo Alquiler: ID Propiedad: {nuevoAlquiler[0]}, DNI Cliente: {nuevoAlquiler[1]}, Vendedor: {nuevoAlquiler[2]}, Fecha Inicio: {nuevoAlquiler[3]}, Fecha Fin: {nuevoAlquiler[4]}, Precio: {nuevoAlquiler[5]}")
            if conexion.Conexion.altaContratoAlquiler(nuevoAlquiler):
                eventos.Eventos.crearMensajeInfo("Contrato grabado", "Se ha grabado una nueva venta")

                Alquileres.cargaTablaContratos()
                Alquileres.cargaTablaMensualidades()

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
                botondelfac.clicked.connect(
                    lambda _, id_contrato=registro[0]: conexion.Conexion.borrarContrato(id_contrato))

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
    def cargaTablaMensualidades():
        try:
            # Obtenemos el listado de mensualidades
            listado = conexion.Conexion.listadoMensualidades()
            print("Listado obtenido:", listado)  # Debug: Verifica el contenido de los datos

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
