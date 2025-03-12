import eventos
import var
from PyQt6 import QtWidgets, QtCore
from datetime import datetime


class Vendedores():

    @staticmethod
    def checkDniVen(dni):
        """
            Verifica la validez del DNI del vendedor y actualiza el campo de texto correspondiente.

            Procedimiento:
            1. Convierte el DNI a mayúsculas y lo establece en el campo de texto.
            2. Verifica si el DNI es válido.
            3. Si el DNI es válido, cambia el estilo del campo de texto a verde.
            4. Si el DNI no es válido, cambia el estilo del campo de texto a rojo, borra el contenido y establece un texto de marcador de posición.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de verificación.
            """
        try:
            dni = str(dni).upper()
            var.ui.txtDniVen.setText(str(dni))
            check = eventos.Eventos.isDniValido(dni)
            if check:
                var.ui.txtDniVen.setStyleSheet('border: 1px solid #41AD48; border-radius: 5px;')
            else:
                var.ui.txtDniVen.setStyleSheet('border: 1px solid #de6767; border-radius: 5px; font-style: italic;')
                var.ui.txtDniVen.setText(None)
                var.ui.txtDniVen.setPlaceholderText("dni no válido")
                var.ui.txtDniVen.setFocus()

        except Exception as e:
            print("Error check clientes" + e)

    @staticmethod
    def checkMovilVen(movil):
        """
                Verifica la validez del número de móvil del vendedor y actualiza el campo de texto correspondiente.

                Procedimiento:
                1. Verifica si el número de móvil es válido.
                2. Si el número de móvil es válido, cambia el estilo del campo de texto a blanco.
                3. Si el número de móvil no es válido, cambia el estilo del campo de texto a rojo, borra el contenido y establece un texto de marcador de posición.

                Excepciones:
                - Captura y muestra cualquier excepción que ocurra durante el proceso de verificación.
                """
        try:
            if eventos.Eventos.isMovilValido(movil):
                var.ui.txtMovilVen.setStyleSheet('background-color: rgb(255, 255, 255);')
            else:
                var.ui.txtMovilVen.setStyleSheet('border: 1px solid #de6767; border-radius: 5px; font-style: italic;')
                var.ui.txtMovilVen.setText(None)
                var.ui.txtMovilVen.setPlaceholderText("móvil no válido")
                var.ui.txtMovilVen.setFocus()
        except Exception as e:
            print("error check movil", e)

    @staticmethod
    def checkEmailVen(mail):
        """
            Verifica la validez del correo electrónico del vendedor y actualiza el campo de texto correspondiente.

            Procedimiento:
            1. Verifica si el correo electrónico es válido.
            2. Si el correo electrónico es válido, cambia el estilo del campo de texto a blanco y lo establece en minúsculas.
            3. Si el correo electrónico no es válido, cambia el estilo del campo de texto a rojo, borra el contenido y establece un texto de marcador de posición.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de verificación.
            """
        try:
            if eventos.Eventos.isMailValido(mail):
                var.ui.txtEmailVen.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtEmailVen.setText(mail.lower())

            else:
                var.ui.txtEmailVen.setStyleSheet('border: 1px solid #de6767; border-radius: 5px; font-style: italic;')
                var.ui.txtEmailVen.setText(None)
                var.ui.txtEmailVen.setPlaceholderText("correo no válido")
                var.ui.txtEmailVen.setFocus()

        except Exception as error:
            print("error check email", error)

    @staticmethod
    def altaVendedor():
        """
                Da de alta a un nuevo vendedor en la base de datos y actualiza la tabla de vendedores.

                Procedimiento:
                1. Obtiene los datos del nuevo vendedor desde la interfaz de usuario.
                2. Verifica si el vendedor ya está presente en la base de datos.
                3. Si el vendedor ya existe, muestra un mensaje de error.
                4. Si los campos obligatorios están completos y el vendedor no existe, lo da de alta en la base de datos.
                5. Si los campos obligatorios no están completos, muestra un mensaje de error.
                6. Si ocurre algún error durante el proceso, muestra un mensaje de error.

                Excepciones:
                - Captura y muestra cualquier excepción que ocurra durante el proceso de alta del vendedor.
                """
        try:
            nuevoVendedor = [var.ui.txtDniVen.text(),var.ui.txtNomVen.text(),var.ui.txtAltaVen.text(),var.ui.txtMovilVen.text(),var.ui.txtEmailVen.text(),var.ui.cmbDeleVen.currentText()]

            if Vendedores.isVendedorPresent(nuevoVendedor):
                eventos.Eventos.crearMensajeError("Error","El DNI del vendedor introducido ya existe")
            elif Vendedores.hasCamposObligatorios(nuevoVendedor) and not Vendedores.isVendedorPresent(nuevoVendedor) and var.claseConexion.altaVendedor(nuevoVendedor):
                eventos.Eventos.crearMensajeInfo("Aviso","Vendedor dado de alta en Base de Datos")
                Vendedores.cargaTablaVendedores()
            elif not Vendedores.hasCamposObligatorios(nuevoVendedor):
                eventos.Eventos.crearMensajeError("Error","Algunos campos deben ser cubiertos.")

            else:
                eventos.Eventos.crearMensajeError("Error","Error al grabar vendedor.")

        except Exception as e:
            print("error alta vendedor", e)

    @staticmethod
    def hasCamposObligatorios(nuevoVendedor):
        """
                Verifica si los campos obligatorios del nuevo vendedor están completos.

                Procedimiento:
                1. Crea una copia de la lista de datos del nuevo vendedor.
                2. Elimina los campos de fecha de alta y correo electrónico de la lista.
                3. Recorre los datos restantes y verifica si alguno está vacío o es None.
                4. Si algún campo está vacío o es None, retorna False.
                5. Si todos los campos están completos, retorna True.

                Parámetros:
                - nuevoVendedor: Lista con los datos del nuevo vendedor.

                Retorna:
                - True si todos los campos obligatorios están completos, False en caso contrario.
                """
        datos = nuevoVendedor[:]
        fecha_alta = datos.pop(2)
        mail = datos.pop(3)
        for dato in datos:
            if dato == "" or dato == None:
                return False
        return True

    @staticmethod
    def isVendedorPresent(nuevoVendedor):
        """
            Verifica si un vendedor ya está presente en la base de datos.

            Procedimiento:
            1. Obtiene los datos del vendedor a partir del DNI.
            2. Si el registro no está vacío, retorna True.
            3. Si el registro está vacío, retorna False.

            Parámetros:
            - nuevoVendedor: Lista con los datos del nuevo vendedor.

            Retorna:
            - True si el vendedor ya está presente, False en caso contrario.
            """
        registro = var.claseConexion.datosOneVendedor(nuevoVendedor[0],"dniVendedor")
        if registro != []:
            return True
        else:
            return False

    @staticmethod
    def cargaTablaVendedores():
        """
            Carga la tabla de vendedores con los datos obtenidos de la base de datos.

            Procedimiento:
            1. Obtiene el listado de vendedores desde la base de datos.
            2. Configura el número de filas de la tabla según el número de vendedores.
            3. Rellena la tabla con los datos de los vendedores.
            4. Ajusta la alineación del texto en las celdas de la tabla.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de carga de la tabla.
            """
        try:
            listado = var.claseConexion.listadoVendedores()

            var.ui.tablaVendedores.setRowCount(len(listado))
            index = 0
            for registro in listado:
                var.ui.tablaVendedores.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0]))) #id
                var.ui.tablaVendedores.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[2])) #nombre
                var.ui.tablaVendedores.setItem(index, 2, QtWidgets.QTableWidgetItem(" " + registro[5] + " ")) #movil
                var.ui.tablaVendedores.setItem(index, 3, QtWidgets.QTableWidgetItem(registro[7])) #movil
                var.ui.tablaVendedores.setItem(index, 4, QtWidgets.QTableWidgetItem(registro[4])) #baja
                var.ui.tablaVendedores.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaVendedores.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaVendedores.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaVendedores.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaVendedores.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                index += 1


        except Exception as e:
            print("Error cargaVendedor en cargaTablaVendedores", e)

    @staticmethod
    def bajaVendedor():
        """
            Da de baja a un vendedor en la base de datos y actualiza la tabla de vendedores.

            Procedimiento:
            1. Obtiene el DNI del vendedor desde la interfaz de usuario.
            2. Intenta dar de baja al vendedor en la base de datos.
            3. Si la baja es exitosa, muestra un mensaje de confirmación y actualiza la tabla de vendedores.
            4. Si el vendedor no existe o ya ha sido dado de baja, muestra un mensaje de error.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de baja del vendedor.
            """
        try:
            dni = var.ui.txtDniVen.text()
            if var.claseConexion.bajaVendedor(dni):
                eventos.Eventos.crearMensajeInfo("Aviso","El vendedor fue dado de baja a fecha de: " + datetime.now().strftime("%d/%m/%Y"))
                Vendedores.cargaTablaVendedores()
            else:
                eventos.Eventos.crearMensajeError("Error","El vendedor no existe o ya ha sido dado de baja.")

        except Exception as e:
            print("Error al dar de baja vendedor", e)

    @staticmethod
    def cargaOneVendedor():
        """
            Carga los datos de un vendedor seleccionado en la interfaz de usuario.

            Procedimiento:
            1. Obtiene la fila seleccionada en la tabla de vendedores.
            2. Extrae los datos de la fila seleccionada.
            3. Obtiene los datos completos del vendedor desde la base de datos usando el DNI.
            4. Asigna los datos obtenidos a los campos correspondientes en la interfaz de usuario.
            5. Establece el ID del vendedor en el campo de texto correspondiente.
            6. Establece el ID del vendedor en el campo de texto de alquileres.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de carga de datos del vendedor.
            """
        try:
            fila = var.ui.tablaVendedores.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = var.claseConexion.datosOneVendedor(str(datos[0]))
            listado = [var.ui.lblIdVen,var.ui.txtDniVen, var.ui.txtNomVen, var.ui.txtAltaVen, var.ui.txtBajaVen,
                       var.ui.txtMovilVen, var.ui.txtEmailVen, var.ui.cmbDeleVen]
            for i in range(len(listado)):
                if i == 7:
                    listado[i].setCurrentText(registro[i])
                else:
                    listado[i].setText(registro[i])
            var.ui.txtIdVendedor.setText(str(registro[0]))
            #ALQUILERES
            var.ui.txtVendedorAlquiler.setText(str(registro[0]))

        except Exception as e:
            print("Error cargaVendedores en cargaOneVendedor", e)

    @staticmethod
    def historicoVendedores():
        """
            Carga el historial de vendedores en la tabla de vendedores.

            Procedimiento:
            1. Llama a la función `cargaTablaVendedores` para cargar los datos de los vendedores en la tabla.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de carga del historial de vendedores.
            """
        try:
            Vendedores.cargaTablaVendedores()
        except Exception as e:
            print("checkbox historico no funciona correctamente en vendedores", e)

    @staticmethod
    def modifVendedor():
        """
            Modifica los datos de un vendedor en la base de datos y actualiza la tabla de vendedores.

            Procedimiento:
            1. Obtiene los datos del vendedor desde la interfaz de usuario.
            2. Verifica si la fecha de baja es válida (no puede ser anterior a la fecha de alta).
            3. Verifica si los campos obligatorios están completos.
            4. Si los campos obligatorios están completos y la fecha de baja es válida, modifica el vendedor en la base de datos.
            5. Si la modificación es exitosa, muestra un mensaje de confirmación y actualiza la tabla de vendedores.
            6. Si los campos obligatorios no están completos, muestra un mensaje de error.
            7. Si ocurre algún error durante el proceso, muestra un mensaje de error.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de modificación del vendedor.
            """
        try:
            modifVendedor = [var.ui.lblIdVen.text(), var.ui.txtNomVen.text(),var.ui.txtAltaVen.text(),var.ui.txtMovilVen.text(),var.ui.txtEmailVen.text(),var.ui.cmbDeleVen.currentText(),var.ui.txtBajaVen.text()]
            if  modifVendedor[6] != "" and not Vendedores.esFechasValidas(modifVendedor):
                eventos.Eventos.crearMensajeError("Aviso","La fecha de baja no puede anterior a la de alta.")
            elif Vendedores.hasCamposObligatorios(modifVendedor[:-1]) and var.claseConexion.modifVendedor(modifVendedor):
                eventos.Eventos.crearMensajeInfo('Aviso',"El vendedor fue modificado correctamente en la base de datos")
                Vendedores.cargaTablaVendedores()
            elif not Vendedores.hasCamposObligatorios(modifVendedor):
                eventos.Eventos.crearMensajeError("Error","El vendedor no está guardado en la base de datos o bien hay campos vacíos.")
            else:
                eventos.Eventos.crearMensajeError("Error","Error al modificar vendedor.")

        except Exception as e:
            print("Error en modifCliente", e)

    @staticmethod
    def esFechasValidas(datosVendedores):
        """
            Verifica si la fecha de baja es posterior a la fecha de alta.

            Procedimiento:
            1. Extrae las fechas de alta y baja de los datos del vendedor.
            2. Convierte las fechas de alta y baja a objetos datetime.
            3. Compara las fechas y retorna True si la fecha de alta es anterior a la fecha de baja, False en caso contrario.

            Parámetros:
            - datosVendedores: Lista con los datos del vendedor.

            Retorna:
            - True si la fecha de alta es anterior a la fecha de baja, False en caso contrario.
            """
        import datetime

        datos = datosVendedores[:]
        alta = datos[2]
        baja = datos[6]

        fecha_alta = datetime.datetime.strptime(alta,"%d/%m/%Y")
        fecha_baja = datetime.datetime.strptime(baja,"%d/%m/%Y")

        return fecha_alta < fecha_baja #si fecha de alta es posterior a fecha de baja devuelve false

    @staticmethod
    def buscaOneVendedor():
        """
            Busca un vendedor en la base de datos por su número de móvil y carga sus datos en la interfaz de usuario.

            Procedimiento:
            1. Obtiene el número de móvil del campo de texto correspondiente.
            2. Busca el vendedor en la base de datos usando el número de móvil.
            3. Si el vendedor existe, carga sus datos en los campos correspondientes de la interfaz de usuario.
            4. Si el vendedor no existe, muestra un mensaje de error.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante el proceso de búsqueda del vendedor.
            """
        try:
            movil = var.ui.txtMovilVen.text()
            registro = var.claseConexion.datosOneVendedor(movil,"movilVendedor")
            if registro:
                listado = [var.ui.lblIdVen,var.ui.txtDniVen, var.ui.txtNomVen, var.ui.txtAltaVen, var.ui.txtBajaVen,
                           var.ui.txtMovilVen, var.ui.txtEmailVen, var.ui.cmbDeleVen]
                for i in range(len(listado)):
                    if i == 7:
                        listado[i].setCurrentText(registro[i])
                    else:
                        listado[i].setText(registro[i])
            else:
                eventos.Eventos.crearMensajeError("Error","El vendedor con móvil "+ movil + " no existe en la base de datos")
        except Exception as e:
            print("Error cargaVendedores en cargaOneVendedor", e)