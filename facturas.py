from mailbox import mboxMessage

from PyQt6.QtWidgets import QHBoxLayout, QWidget
from PyQt6.uic.Compiler.qtproxies import QtGui
from PyQt6.QtGui import QIcon
from reportlab.lib.testutils import setOutDir

import conexion
import propiedades
import eventos
import var
from PyQt6 import QtWidgets, QtCore


class Facturas:

    @staticmethod
    def altaFactura():
        try:
            nuevaFactura = [var.ui.txtFechaFactura.text(), var.ui.txtdniclifac.text()]
            if var.ui.txtdniclifac.text() == "" or var.ui.txtdniclifac.text() is None:
                eventos.Eventos.crearMensajeError("Error al grabar factura",
                                                  "Recuerda seleccionar un cliente antes de grabar una factura")
            if var.ui.txtFechaFactura.text() == "" or var.ui.txtFechaFactura.text() is None:
                eventos.Eventos.crearMensajeError("Error al grabar factura",
                                                  "No es posible grabar una factura sin seleccionar una fecha")
            elif conexion.Conexion.altaFactura(nuevaFactura):
                eventos.Eventos.crearMensajeInfo("Factura grabada", "Se ha grabado una nueva factura")
                Facturas.cargaTablaFacturas()
            else:
                eventos.Eventos.crearMensajeError("Error", "No se ha podido grabar factura")
        except Exception as e:
            print("factura", e)

    @staticmethod
    def cargaTablaFacturas():
        try:
            listado = var.claseConexion.listadoFacturas()
            var.ui.tablaFacturas.setRowCount(len(listado))
            index = 0
            for registro in listado:
                item_id = QtWidgets.QTableWidgetItem(str(registro[0]))
                item_id.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaFacturas.setItem(index, 0, item_id)  # id

                item_fecha = QtWidgets.QTableWidgetItem(str(registro[1]))
                item_fecha.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaFacturas.setItem(index, 1, item_fecha)  # fecha

                item_dni = QtWidgets.QTableWidgetItem(str(registro[2]))
                item_dni.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaFacturas.setItem(index, 2, item_dni)  # dni

                botondelfac = QtWidgets.QPushButton()
                botondelfac.setFixedSize(25, 25)
                botondelfac.setIconSize(QtCore.QSize(25, 25))
                botondelfac.setIcon(QIcon("./img/basura.ico"))
                botondelfac.setStyleSheet("background: transparent; border: none;")

                contenedor = QtWidgets.QWidget()
                layout = QHBoxLayout()
                layout.addWidget(botondelfac)
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                contenedor.setLayout(layout)

                container = QWidget()
                container.setLayout(layout)
                var.ui.tablaFacturas.setCellWidget(index, 3, container)
                botondelfac.clicked.connect(lambda checked, id=registro[0]: Facturas.bajaFactura(id))
                index += 1

        except IndexError as e:
            print("IndexError in cargaTablaFacturas:", e)
        except Exception as e:
            print("Error carga factura en cargaTablaFacturas", e)

    @staticmethod
    def cargaTablaVentas():
        idFactura = var.ui.lblNumFactura.text()
        listado = conexion.Conexion.listadoVentas(idFactura)
        var.ui.tablaVentas.setRowCount(len(listado))
        index = 0
        subtotal = 0
        for registro in listado:
            var.ui.tablaVentas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
            var.ui.tablaVentas.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[1])))
            var.ui.tablaVentas.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[2])))
            var.ui.tablaVentas.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[3])))
            var.ui.tablaVentas.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[4])))
            var.ui.tablaVentas.setItem(index, 5, QtWidgets.QTableWidgetItem(str(registro[5]) + " € "))

            botondelfac = QtWidgets.QPushButton()
            botondelfac.setFixedSize(30, 24)
            botondelfac.setIcon(QtGui.QIcon('img/papelera.ico'))
            botondelfac.setProperty("row", index)
            botondelfac.clicked.connect(
                lambda checked, idVenta=str(registro[0]), idpropiedad=str(registro[1]): Facturas.eliminarVenta(idVenta,
                                                                                                               idpropiedad))
            contenedor = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout()
            layout.addWidget(botondelfac)
            layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            contenedor.setLayout(layout)
            var.ui.tablaVentas.setCellWidget(index, 6, contenedor)
            if var.ui.tablaVentas.item(index, 0):
                var.ui.tablaVentas.item(index, 0).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
            if var.ui.tablaVentas.item(index, 1):
                var.ui.tablaVentas.item(index, 1).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
            if var.ui.tablaVentas.item(index, 2):
                var.ui.tablaVentas.item(index, 2).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
            if var.ui.tablaVentas.item(index, 3):
                var.ui.tablaVentas.item(index, 3).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
            if var.ui.tablaVentas.item(index, 4):
                var.ui.tablaVentas.item(index, 4).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
            if var.ui.tablaVentas.item(index, 5):
                var.ui.tablaVentas.item(index, 5).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
            subtotal += registro[5]

            index += 1

        iva = subtotal * 0.21
        total = subtotal + iva
        subTotalStr = f"{subtotal:,.1f} €"
        ivaStr = f"{iva:,.1f} €"
        totalStr = f"{total:,.1f} €"
        var.ui.lblSubTotal.setText(subTotalStr)
        var.ui.lblIVA.setText(ivaStr)
        var.ui.lblTotal.setText(totalStr)

    @classmethod
    def bajaFactura(cls, id):
        try:
            if conexion.Conexion.eliminarFactura(id):
                cls.cargaTablaFacturas()
                eventos.Eventos.crearMensajeInfo("Factura eliminada", "Se ha eliminado la factura")
            else:
                eventos.Eventos.crearMensajeError("Error", "No se ha podido eliminar la factura")
        except Exception as e:
            print("Error en bajaFactura", e)

    @staticmethod
    def cargaOneFactura():
        try:
            fila = var.ui.tablaFacturas.selectedItems()
            datos = [dato.text() for dato in fila]
            var.ui.lblNumFactura.setText(datos[0])
        except Exception as e:
            print("Error cargaVendedores en cargaOneVendedor", e)

    @staticmethod
    def cargarPropiedadVenta(propiedad):
        try:
            if str(propiedad[6]).lower() == "disponible":
                var.ui.txtCodProp.setText(str(propiedad[1]))
                var.ui.txtTipoProp.setText(str(propiedad[2]))
                var.ui.txtPrecioProp.setText(str(propiedad[3]) + " €")
                var.ui.txtDirProp.setText(str(propiedad[4]).title())
                var.ui.txtLocProp.setText(str(propiedad[5]))
                return True
            else:
                mbox = eventos.Eventos.crearMensajeError("Error", "La propiedad seleccionada no está disponible")
                mbox.exec()
                return False
        except Exception as e:
            print("Error en cargarPropiedadVenta", e)

    @staticmethod
    def grabarVenta():
        try:
            nuevaVenta = [var.ui.lblNumFactura.text(), var.ui.txtCodProp.text(), var.ui.txtIdVendedor.text()]
            if var.ui.txtCodProp.text() == "" or var.ui.txtCodProp.text() is None:
                eventos.Eventos.crearMensajeError("Error al grabar venta",
                                                  "Recuerda seleccionar una propiedad antes de grabar una venta")

            elif var.ui.txtIdVendedor.text() == "" or var.ui.txtIdVendedor.text() is None:
                eventos.Eventos.crearMensajeError("Error al grabar venta",
                                                  "Recuerda seleccionar un vendedor antes de grabar una venta")

            elif var.ui.lblNumFactura.text() == "" or var.ui.lblNumFactura.text() is None:
                eventos.Eventos.crearMensajeError("Error al grabar venta",
                                                  "Recuerda seleccionar una factura antes de grabar una venta")

            elif conexion.Conexion.altaVenta(nuevaVenta):
                eventos.Eventos.crearMensajeInfo("Venta grabada", "Se ha grabado una nueva venta")

                Facturas.cargaTablaVentas()
                propiedades.Propiedades.cargarTablaPropiedades()
            else:
                eventos.Eventos.crearMensajeError("Error", "No se ha podido grabar venta")

        except Exception as e:
            print("venta", e)

    def eliminarVenta(idVenta, idpropiedad):
        try:
            if conexion.Conexion.bajaVenta(idVenta) and conexion.Conexion.altaPropiedadVenta(str(idpropiedad)):
                mbox = eventos.Eventos.crearMensajeInfo("Venta eliminada","Se ha eliminado la venta")
                mbox.exec()
                Facturas.cargaTablaVentas()
                propiedades.Propiedades.cargarTablaPropiedades()
            else:
                mbox = eventos.Eventos.crearMensajeError("Error","No se ha podido eliminar la venta")
                mbox.exec()
        except Exception as e:
            print("Error en eliminarVenta",e)