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


class Facturas:

    @staticmethod
    def altaFactura():
        """
           Crea una nueva factura y la guarda en la base de datos.

           La función verifica que se haya seleccionado un cliente y una fecha antes de intentar
           guardar la factura. Si falta alguno de estos datos, se muestra un mensaje de error.
           Si la factura se guarda correctamente, se muestra un mensaje de éxito y se actualiza
           la tabla de facturas. En caso de error, se muestra un mensaje de error.

           Excepciones:
               Exception: Captura cualquier excepción y la imprime en la consola.
           """
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
        """
                Carga la tabla de facturas en la interfaz de usuario.

                La función obtiene el listado de facturas desde la base de datos y las muestra en la tabla de facturas
                de la interfaz de usuario. Para cada factura, se crea una fila con su ID, fecha y DNI del cliente.
                Además, se añade un botón para eliminar la factura.

                Excepciones:
                    IndexError: Captura cualquier excepción de índice y la imprime en la consola.
                    Exception: Captura cualquier otra excepción y la imprime en la consola.
                """
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
        """
                Carga la tabla de ventas en la interfaz de usuario.

                La función obtiene el listado de ventas desde la base de datos y las muestra en la tabla de ventas
                de la interfaz de usuario. Para cada venta, se crea una fila con sus datos correspondientes.
                Además, se añade un botón para eliminar la venta.

                Parámetros:
                    idVenta (str, opcional): El ID de la venta a cargar. Si no se proporciona, se utiliza el ID de la factura actual.

                Excepciones:
                    Exception: Captura cualquier excepción y la imprime en la consola.
                """
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

    @staticmethod
    def bajaFactura(id):
        """
                Elimina una factura de la base de datos.

                La función intenta eliminar una factura utilizando su ID. Si la eliminación es exitosa,
                se actualiza la tabla de facturas y se muestra un mensaje de éxito. Si no, se muestra un mensaje de error.

                Excepciones:
                    Exception: Captura cualquier excepción y la imprime en la consola.
        """
        try:
            if conexion.Conexion.eliminarFactura(id):
                Facturas.cargaTablaFacturas()
                eventos.Eventos.crearMensajeInfo("Factura eliminada", "Se ha eliminado la factura")
            else:
                eventos.Eventos.crearMensajeError("Error", "No se ha podido eliminar la factura")
        except Exception as e:
            print("Error en bajaFactura", e)

    @staticmethod
    def cargaOneFactura():
        """
            Carga una factura seleccionada en la interfaz de usuario.

            La función obtiene los datos de la factura seleccionada en la tabla de facturas y los muestra en la interfaz de usuario.
            Luego, carga las ventas asociadas a esa factura y las propiedades correspondientes.

            Excepciones:
                Exception: Captura cualquier excepción y la imprime en la consola.
            """
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
        """
            Carga los datos de una propiedad en la interfaz de usuario.

            La función recibe una lista con los datos de una propiedad y los muestra en los campos correspondientes
            de la interfaz de usuario. Si la propiedad no está disponible, muestra un mensaje de error.

            Parámetros:
                propiedad (list): Lista con los datos de la propiedad.

            Retorna:
                bool: True si la propiedad está disponible y se cargan los datos correctamente, False en caso contrario.

            Excepciones:
                Exception: Captura cualquier excepción y la imprime en la consola.
            """
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
        """
                Graba una nueva venta en la base de datos.

                La función verifica que se hayan seleccionado una propiedad, un vendedor y una factura antes de intentar
                guardar la venta. Si falta alguno de estos datos, se muestra un mensaje de error. Si la venta se guarda
                correctamente, se muestra un mensaje de éxito y se actualizan las tablas de ventas y propiedades. En caso
                de error, se muestra un mensaje de error.

                Excepciones:
                    Exception: Captura cualquier excepción y la imprime en la consola.
        """
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
        """
            Elimina una venta de la base de datos y actualiza las tablas de ventas y propiedades.

            La función intenta eliminar una venta utilizando su ID y marca la propiedad asociada como disponible.
            Si la eliminación es exitosa, se actualizan las tablas de ventas y propiedades y se muestra un mensaje de éxito.
            Si no, se muestra un mensaje de error.

            Parámetros:
                idventa (int): El ID de la venta a eliminar.
                idpropiedad (int): El ID de la propiedad asociada a la venta.

            Excepciones:
                Exception: Captura cualquier excepción y la imprime en la consola.
            """
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
        """
            Carga los datos de una propiedad en alquiler en la interfaz de usuario.

            La función recibe una lista con los datos de una propiedad en alquiler y los muestra en los campos correspondientes
            de la interfaz de usuario. Si la propiedad no está disponible, muestra un mensaje de error.

            Parámetros:
                listadoAlquileres (list): Lista con los datos de la propiedad en alquiler.

            Retorna:
                bool: True si la propiedad está disponible y se cargan los datos correctamente, False en caso contrario.

            Excepciones:
                Exception: Captura cualquier excepción y la imprime en la consola.
            """
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

    @staticmethod
    def guardarFactura():
        """
            Guarda la factura seleccionada y genera un informe.

            La función verifica si hay una factura seleccionada. Si no hay ninguna factura seleccionada,
            muestra un mensaje de error y termina la ejecución. Si hay una factura seleccionada, genera
            un informe de la factura.

            @return: None
            """
        if not var.ui.lblNumFactura.text():
            eventos.Eventos.crearMensajeError("Error", "No hay ninguna factura seleccionada")
            print("lblNumFactura no tiene valor")
            return
        informes.Informes.reportFact(var.ui.lblNumFactura.text())