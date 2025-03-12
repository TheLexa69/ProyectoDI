from datetime import datetime

from PyQt6 import QtWidgets, QtGui, QtCore

import clientes
import conexion
import conexionserver
import eventos
import var


class Clientes:
    @staticmethod
    def altaCliente():
        """
            Da de alta un nuevo cliente en la base de datos.

            Recoge los datos del cliente desde la interfaz de usuario, verifica que todos los campos obligatorios estén completos
            y luego intenta insertar el nuevo cliente en la base de datos. Si la inserción es exitosa, muestra un mensaje de éxito
            y recarga la tabla de clientes. Si faltan campos obligatorios, muestra un mensaje de error indicando que algunos campos
            deben ser cubiertos. Si ocurre un error durante la inserción, muestra un mensaje de error indicando que hubo un problema
            al grabar el cliente.

            Excepciones:
                - Captura cualquier excepción que ocurra durante el proceso y la imprime en la consola.

            """
        try:
            nuevoCli = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text().title(),
                        var.ui.txtNomcli.text().title(), var.ui.txtEmailcli.text(),
                        var.ui.txtMovilcli.text(), var.ui.txtDircli.text(), var.ui.cmbProvcli.currentText(),
                        var.ui.cmbMunicli.currentText()]

            if Clientes.hasCamposObligatoriosCli(nuevoCli) and var.claseConexion.altaCliente(nuevoCli):
                eventos.Eventos.crearMensajeInfo("Aviso", "Cliente dado de alta en Base de Datos")

                Clientes.cargaTablaClientes()
            elif not Clientes.hasCamposObligatoriosCli(nuevoCli):
                eventos.Eventos.crearMensajeError("Error", "Algunos campos deben ser cubiertos.")

            else:
                eventos.Eventos.crearMensajeError("Error", "Error al grabar cliente.")

        except Exception as e:
            print("error alta cliente", e)

    @staticmethod
    def checkDniCli(dni):
        """
            Verifica la validez del DNI del cliente.

            Toma el DNI ingresado por el usuario, lo convierte a mayúsculas y lo valida.
            Si el DNI es válido, cambia el estilo del campo de texto para indicar validez y muestra un tick.
            Si el DNI no es válido, cambia el estilo del campo de texto para indicar error, borra el contenido y muestra un mensaje de error.

            Excepciones:
                - Captura cualquier excepción que ocurra durante el proceso y la imprime en la consola.
            """
        try:
            dni = str(dni).upper()
            var.ui.txtDnicli.setText(str(dni))
            check = eventos.Eventos.isDniValido(dni)
            if check:
                var.ui.txtDnicli.setStyleSheet(
                    'border: 1px solid #41AD48; border-radius: 5px; background-color: rgb(254, 255, 210)')
                Clientes.cargarTickcli()
            else:
                var.ui.txtDnicli.setStyleSheet(
                    'border: 1px solid #de6767; border-radius: 5px; font-style: italic; background-color: rgb(254, 255, 210)')
                var.ui.txtDnicli.setText(None)
                var.ui.txtDnicli.setPlaceholderText("dni no válido")
                var.ui.txtDnicli.setFocus()
                Clientes.cargarCruzcli()

        except Exception as e:
            print("Error check clientes" + e)

    @staticmethod
    def cargarTickcli():
        """
                Carga una imagen de tick en el label correspondiente.

                Utiliza la función cargarTick de la clase Eventos para obtener la imagen del tick y la establece en el label lblTickcli.
                Además, ajusta el contenido del label para que la imagen se escale correctamente.

                Excepciones:
                    - Captura cualquier excepción que ocurra durante el proceso y la imprime en la consola.
        """
        pixmap = eventos.Eventos.cargarTick()
        var.ui.lblTickcli.setPixmap(pixmap)
        var.ui.lblTickcli.setScaledContents(True)

    @staticmethod
    def cargarCruzcli():
        """
                Carga una imagen de cruz en el label correspondiente.

                Utiliza la función cargarCruz de la clase Eventos para obtener la imagen de la cruz y la establece en el label lblTickcli.
                Además, ajusta el contenido del label para que la imagen se escale correctamente.

                Excepciones:
                    - Captura cualquier excepción que ocurra durante el proceso y la imprime en la consola.
                """
        pixmap = eventos.Eventos.cargarCruz()
        var.ui.lblTickcli.setPixmap(pixmap)
        var.ui.lblTickcli.setScaledContents(True)

    @staticmethod
    def checkEmailCli(mail):
        """
           Verifica la validez del correo electrónico del cliente.

           Toma el correo electrónico ingresado por el usuario, lo convierte a minúsculas y lo valida.
           Si el correo es válido, cambia el estilo del campo de texto para indicar validez.
           Si el correo no es válido, cambia el estilo del campo de texto para indicar error, borra el contenido y muestra un mensaje de error.

           Excepciones:
               - Captura cualquier excepción que ocurra durante el proceso y la imprime en la consola.
           """
        try:
            mail = str(var.ui.txtEmailcli.text())
            if eventos.Eventos.isMailValido(mail):
                var.ui.txtEmailcli.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtEmailcli.setText(mail.lower())

            else:
                var.ui.txtEmailcli.setStyleSheet('border: 1px solid #de6767; border-radius: 5px; font-style: italic;')
                var.ui.txtEmailcli.setText(None)
                var.ui.txtEmailcli.setPlaceholderText("correo no válido")
                var.ui.txtEmailcli.setFocus()

        except Exception as error:
            print("error check email", error)

    @staticmethod
    def checkMovilCli(movil):
        """
            Verifica la validez del número de móvil del cliente.

            Toma el número de móvil ingresado por el usuario y lo valida.
            Si el número es válido, cambia el estilo del campo de texto para indicar validez.
            Si el número no es válido, cambia el estilo del campo de texto para indicar error, borra el contenido y muestra un mensaje de error.

            Excepciones:
                - Captura cualquier excepción que ocurra durante el proceso y la imprime en la consola.
            """
        try:
            if eventos.Eventos.isMovilValido(movil):
                var.ui.txtMovilcli.setStyleSheet('background-color: rgb(255, 255, 255);')
            else:
                var.ui.txtMovilcli.setStyleSheet('border: 1px solid #de6767; border-radius: 5px; font-style: italic;')
                var.ui.txtMovilcli.setText(None)
                var.ui.txtMovilcli.setPlaceholderText("móvil no válido")
                var.ui.txtMovilcli.setFocus()
        except Exception as e:
            print("error check movil", e)

    @staticmethod
    def hasCamposObligatoriosCli(datosClientes):
        """
            Verifica que todos los campos obligatorios del cliente estén completos.

            Toma una lista de datos del cliente, elimina el correo electrónico de la lista y verifica que
            todos los campos restantes no estén vacíos ni sean nulos. Si todos los campos obligatorios
            están completos, devuelve True; de lo contrario, devuelve False.

            :param datosClientes: Lista de datos del cliente.
            :return: True si todos los campos obligatorios están completos, False en caso contrario.
            """
        datos = datosClientes[:]
        emailCli = datos.pop(4)
        for dato in datos:
            if dato == "" or dato == None:
                return False
        return True

    @staticmethod
    def esFechasValidas(datosClientes):
        """
            Verifica que las fechas de alta y baja del cliente sean válidas.

            Toma una lista de datos del cliente, extrae las fechas de alta y baja,
            y verifica que la fecha de alta sea anterior a la fecha de baja.
            Si la fecha de alta es posterior a la fecha de baja, devuelve False.

            :param datosClientes: Lista de datos del cliente.
            :return: True si la fecha de alta es anterior a la fecha de baja, False en caso contrario.
            """
        import datetime

        datos = datosClientes[:]
        alta = datos[1]
        baja = datos[9]

        fecha_alta = datetime.datetime.strptime(alta, "%d/%m/%Y")
        fecha_baja = datetime.datetime.strptime(baja, "%d/%m/%Y")

        return fecha_alta < fecha_baja  # si fecha de alta es posterior a fecha de baja devuelve false

    @staticmethod
    def cargaTablaClientes():
        """
            Carga los datos de los clientes en la tabla de la interfaz de usuario.

            Obtiene la lista de clientes desde la base de datos, calcula la paginación y actualiza la tabla de clientes
            en la interfaz de usuario con los datos correspondientes a la página actual. También gestiona la habilitación
            y deshabilitación de los botones de navegación (anterior y siguiente) según la página actual.

            Excepciones:
                - Captura cualquier excepción que ocurra durante el proceso y la imprime en la consola.
            """
        try:
            listado = var.claseConexion.listadoClientes()
            var.lenClientes = len(listado)

            var.ui.spinClipPag.setValue(var.maxClientesPagina)

            inicioListado = var.paginaActualCli * var.maxClientesPagina
            sublistado = listado[inicioListado: inicioListado + var.maxClientesPagina]

            if listado[0] == sublistado[0]:
                var.ui.btnAnterior.setDisabled(True)
            else:
                var.ui.btnAnterior.setDisabled(False)

            if listado[-1] == sublistado[-1]:
                var.ui.btnSiguiente.setDisabled(True)
            else:
                var.ui.btnSiguiente.setDisabled(False)

            numPaginas = (var.lenClientes // var.maxClientesPagina) + 1
            if len(listado) % var.maxClientesPagina == 0:
                numPaginas -= 1
            var.ui.lblPaginas.setText("Página " + str(var.paginaActualCli + 1) + "/" + str(numPaginas))

            var.ui.tablaClientes.setRowCount(len(sublistado))
            index = 0
            for registro in sublistado:
                var.ui.tablaClientes.setItem(index, 0, QtWidgets.QTableWidgetItem(registro[0]))  # dni
                var.ui.tablaClientes.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[2]))  # apellido
                var.ui.tablaClientes.setItem(index, 2, QtWidgets.QTableWidgetItem(registro[3]))  # nombre
                var.ui.tablaClientes.setItem(index, 3, QtWidgets.QTableWidgetItem("  " + registro[5] + "  "))  # movil
                var.ui.tablaClientes.setItem(index, 4, QtWidgets.QTableWidgetItem(registro[7]))  # provincia
                var.ui.tablaClientes.setItem(index, 5, QtWidgets.QTableWidgetItem(registro[8]))  # municipio
                var.ui.tablaClientes.setItem(index, 6, QtWidgets.QTableWidgetItem(registro[9]))  # baja
                var.ui.tablaClientes.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaClientes.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaClientes.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                index += 1


        except Exception as e:
            print("Error cargaClientes en cargaTablaClientes", e)

    @staticmethod
    def cargaOneCliente():
        """
            Carga los datos de un cliente seleccionado en la interfaz de usuario.

            Obtiene la fila seleccionada en la tabla de clientes, extrae los datos del cliente y los carga en los campos
            correspondientes de la interfaz de usuario. También actualiza los campos relacionados con facturas y alquileres.

            Excepciones:
                - Captura cualquier excepción que ocurra durante el proceso y la imprime en la consola.
            """
        try:
            fila = var.ui.tablaClientes.selectedItems()
            datos = [dato.text() for dato in fila]

            registro = var.claseConexion.datosOneCliente(str(datos[0]))

            registro = [x if x != 'None' else "" for x in registro]
            listado = [var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli, var.ui.txtNomcli,
                       var.ui.txtEmailcli, var.ui.txtMovilcli, var.ui.txtDircli, var.ui.cmbProvcli, var.ui.cmbMunicli,
                       var.ui.txtBajacli]

            for i in range(len(listado)):
                if i in (7, 8):
                    listado[i].setCurrentText(registro[i])
                else:
                    listado[i].setText(registro[i])
                    if i == 0:
                        var.ui.lblTickcli.clear()

            var.ui.txtdniclifac.setText(registro[0])
            ##CARGA DNI EN ALQUILERES
            var.ui.txtDniClienteAlquiler.setText(registro[0])

            var.ui.txtCliApel.setText(registro[2])
            var.ui.txtCliNom.setText(registro[3])

        except Exception as e:
            print("Error en cargaOneCliente:", e)

    @staticmethod
    def buscaOneCliente():
        """
            Busca y carga los datos de un cliente en la interfaz de usuario.

            Obtiene el DNI del cliente desde la interfaz de usuario, busca los datos del cliente en la base de datos
            y, si el cliente existe, carga los datos en los campos correspondientes de la interfaz de usuario.
            Si el cliente no existe, muestra un mensaje de error.

            Excepciones:
                - Captura cualquier excepción que ocurra durante el proceso y la imprime en la consola.
            """
        try:
            dni = var.ui.txtDnicli.text()
            registro = var.claseConexion.datosOneCliente(dni)
            if registro:
                listado = [var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli, var.ui.txtNomcli,
                           var.ui.txtEmailcli, var.ui.txtMovilcli, var.ui.txtDircli, var.ui.cmbProvcli,
                           var.ui.cmbMunicli, var.ui.txtBajacli]
                for i in range(len(listado)):
                    if i in (7, 8):
                        listado[i].setCurrentText(registro[i])
                    else:
                        listado[i].setText(registro[i])
                        if i == 0:
                            var.ui.lblTickcli.clear()
            else:
                eventos.Eventos.crearMensajeError("Error",
                                                  "El cliente con DNI " + dni + " no existe en la base de datos")
            # Clientes.cargarCliente(registro)

        except Exception as e:
            print("Error cargaClientes", e)

    @staticmethod
    def modifCliente():
        """
            Modifica los datos de un cliente en la base de datos.

            Recoge los datos del cliente desde la interfaz de usuario, verifica que todos los campos obligatorios estén completos
            y que las fechas de alta y baja sean válidas. Luego intenta actualizar los datos del cliente en la base de datos.
            Si la modificación es exitosa, muestra un mensaje de éxito y recarga la tabla de clientes. Si faltan campos obligatorios
            o las fechas no son válidas, muestra un mensaje de error indicando el problema. Si ocurre un error durante la modificación,
            muestra un mensaje de error indicando que hubo un problema al modificar el cliente.

            Excepciones:
                - Captura cualquier excepción que ocurra durante el proceso y la imprime en la consola.
            """
        try:
            modifcli = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text().title(),
                        var.ui.txtNomcli.text().title(),
                        var.ui.txtEmailcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDircli.text(),
                        var.ui.cmbProvcli.currentText(),
                        var.ui.cmbMunicli.currentText(), var.ui.txtBajacli.text()]
            if modifcli[9] != "" and not Clientes.esFechasValidas(modifcli):
                eventos.Eventos.crearMensajeError("Aviso", "La fecha de baja no puede anterior a la de alta.")
            elif clientes.Clientes.hasCamposObligatoriosCli(modifcli[:-1]) and var.claseConexion.modifCliente(modifcli):
                eventos.Eventos.crearMensajeInfo('Aviso', "El cliente fue modificado correctamente en la base de datos")
                Clientes.cargaTablaClientes()
            elif not clientes.Clientes.hasCamposObligatoriosCli(modifcli):
                eventos.Eventos.crearMensajeError("Error",
                                                  "El cliente no está guardado en la base de datos o bien hay campos vacíos.")
            else:
                eventos.Eventos.crearMensajeError("Error", "Error al modificar cliente.")

        except Exception as e:
            print("Error en modifCliente", e)

    @staticmethod
    def bajaCliente():
        """
            Da de baja a un cliente en la base de datos.

            Obtiene el DNI del cliente desde la interfaz de usuario y lo utiliza para dar de baja al cliente en la base de datos.
            Si la baja es exitosa, muestra un mensaje de éxito con la fecha de baja y recarga la tabla de clientes.
            Si el cliente no existe o ya ha sido dado de baja, muestra un mensaje de error.

            Excepciones:
                - Captura cualquier excepción que ocurra durante el proceso y la imprime en la consola.
            """
        try:
            dni = var.ui.txtDnicli.text()
            if var.claseConexion.bajaCliente(dni):
                eventos.Eventos.crearMensajeInfo("Aviso",
                                                 "El cliente fue dado de baja a fecha de: " + datetime.now().strftime(
                                                     "%d/%m/%Y"))
                var.paginaActualCli = 0
                Clientes.cargaTablaClientes()
            else:
                eventos.Eventos.crearMensajeError("Error", "El cliente no existe o ya ha sido dado de baja.")

        except Exception as e:
            print("Error al dar de baja cliente", e)

    @staticmethod
    def historicoCli():
        """
           Carga el historial de clientes en la tabla de la interfaz de usuario.

           Establece la página actual de clientes a 0 y recarga la tabla de clientes
           con los datos correspondientes. Si ocurre un error durante el proceso,
           imprime un mensaje de error en la consola.

           Excepciones:
               - Captura cualquier excepción que ocurra durante el proceso y la imprime en la consola.
           """
        try:
            var.paginaActualCli = 0
            Clientes.cargaTablaClientes()
        except Exception as e:
            print("checkbox historico no funciona correcatamente", e)
