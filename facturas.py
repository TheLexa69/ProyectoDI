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
    def cargaTablaVentas(idVenta=None):
        try:
            if not idVenta:
                idVenta = var.ui.lblNumFactura.text()

            if idVenta == "" or idVenta is None:
                var.ui.tablaVentas.setRowCount(1)
                for col in range(7):
                    var.ui.tablaVentas.setItem(0, col, QtWidgets.QTableWidgetItem(""))
                var.ui.lblSubTotal.setText("0.00 €")
                var.ui.lblIVA.setText("0.00 €")
                var.ui.lblTotal.setText("0.00 €")
                return

            listado = conexion.Conexion.listadoVentas(idVenta)
            var.ui.tablaVentas.setRowCount(len(listado))

            subtotal = 0

            for index, registro in enumerate(listado):
                for col, value in enumerate(registro[:6]):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    var.ui.tablaVentas.setItem(index, col, item)

                # Botón de eliminar
                botondelfac = QtWidgets.QPushButton()
                botondelfac.setFixedSize(25, 25)
                botondelfac.setIconSize(QtCore.QSize(25, 25))
                botondelfac.setIcon(QIcon("./img/basura.ico"))
                botondelfac.setStyleSheet("background: transparent; border: none;")
                botondelfac.setProperty("row", index)
                botondelfac.clicked.connect(
                    lambda _, idV=registro[0], idP=registro[1]: Facturas.eliminarVenta(idV, idP))

                contenedor = QtWidgets.QWidget()
                layout = QtWidgets.QHBoxLayout()
                layout.addWidget(botondelfac)
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                contenedor.setLayout(layout)

                var.ui.tablaVentas.setCellWidget(index, 6, contenedor)

                subtotal += float(registro[5])

            iva = subtotal * 0.10
            total = subtotal + iva

            var.ui.lblSubTotal.setText(f"{subtotal:,.2f} €")
            var.ui.lblIVA.setText(f"{iva:,.2f} €")
            var.ui.lblTotal.setText(f"{total:,.2f} €")

        except Exception as e:
            print("Error en cargaTablaVentas:", e)

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
            idVentaFactura = datos[0]
            var.ui.lblNumFactura.setText(idVentaFactura)  # HASTA AQUI CARGA EL ID DE LA FACTURA EN NUM FACTURA

            try:
                ventas = conexion.Conexion.cargaVenta(idVentaFactura)
                if ventas:
                    codProp = ventas[0][2]  # Guardar el codProp en la variable codProp
                    idFactura = ventas[0][1]
                    idVenta = ventas[0][0]

                    propiedad = conexion.Conexion.cargaPropiedadVenta( codProp)  # Recupera la propiedad a partir de su código

                    Facturas.cargaTablaVentas(idFactura)

                else :
                    Facturas.cargaTablaVentas()

            except Exception as e:
                print("Error en carga Factura", e)

        except Exception as e:
            print("Error cargaOneFactura en Facturas", e)

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

    def eliminarVenta(idventa, idpropiedad):
        try:
            if conexion.Conexion.bajaVenta(idventa) and conexion.Conexion.altaPropiedadVenta(str(idpropiedad)):
                eventos.Eventos.crearMensajeInfo("Venta eliminada", "Se ha eliminado la venta")
                Facturas.cargaTablaVentas()
                propiedades.Propiedades.cargarTablaPropiedades()
            else:
                eventos.Eventos.crearMensajeError("Error", "No se ha podido eliminar la venta")
        except Exception as e:
            print("Error en eliminarVenta", e)

    @staticmethod
    def cargarPropiedadAlquiler(listadoAlquileres):
        try:
            if str(listadoAlquileres[6]).lower() == "disponible":
                # var.ui.txtCodProp.setText(str(listadoAlquileres[1]))
                # var.ui.txtTipoProp.setText(str(listadoAlquileres[2]))
                var.ui.txtPrecioAlquiler.setText(str(listadoAlquileres[3]) + " €")
                # var.ui.txtDirProp.setText(str(listadoAlquileres[4]).title())
                # var.ui.txtLocProp.setText(str(listadoAlquileres[5]))

                # ALQUILERES
                var.ui.txtIdPropiedadAlquiler.setText(str(listadoAlquileres[1]))
                return True
            else:
                mbox = eventos.Eventos.crearMensajeError("Error", "La propiedad seleccionada no está disponible")
                mbox.exec()
                return False
        except Exception as e:
            print("Error en cargarPropiedadVenta", e)
