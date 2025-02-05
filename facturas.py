from PyQt6.QtWidgets import QHBoxLayout, QWidget
from PyQt6.uic.Compiler.qtproxies import QtGui
from PyQt6.QtGui import QIcon
from reportlab.lib.testutils import setOutDir

import conexion
import eventos
import var
from PyQt6 import QtWidgets, QtCore


class Facturas:

    @staticmethod
    def altaFactura():
        try:
            nuevaFactura = [var.ui.txtFechaFactura.text(),var.ui.txtdniclifac.text()]
            if var.ui.txtdniclifac.text() == "" or var.ui.txtdniclifac.text() is None:
                eventos.Eventos.crearMensajeError("Error al grabar factura","Recuerda seleccionar un cliente antes de grabar una factura")
            if var.ui.txtFechaFactura.text() == "" or var.ui.txtFechaFactura.text() is None:
                eventos.Eventos.crearMensajeError("Error al grabar factura","No es posible grabar una factura sin seleccionar una fecha")
            elif conexion.Conexion.altaFactura(nuevaFactura):
                eventos.Eventos.crearMensajeInfo("Factura grabada","Se ha grabado una nueva factura")
                Facturas.cargaTablaFacturas()
            else:
                eventos.Eventos.crearMensajeError("Error","No se ha podido grabar factura")
        except Exception as e:
            print("factura",e)

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