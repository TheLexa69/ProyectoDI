import math
from dataclasses import dataclass
from datetime import datetime
from PIL import Image
from reportlab.pdfgen import canvas
import os, shutil
from PyQt6 import QtSql, QtWidgets, QtCore
import sqlite3

import conexion
import eventos
import var

class Informes:
    @staticmethod
    def reportClientes():
        """
            Genera un informe en formato PDF con la lista de clientes.

            El informe incluye los campos: DNI, Apellidos, Nombre, Móvil, Provincia y Municipio.
            Se crea un archivo PDF en el directorio `.\informes` con el nombre `listadoclientes` seguido de la fecha y hora actual.
            Si el número de registros excede el espacio disponible en una página, se crean páginas adicionales.

            Pasos:
            1. Crea el directorio `.\informes` si no existe.
            2. Genera el archivo PDF con el nombre basado en la fecha y hora actual.
            3. Consulta la base de datos para obtener el número de clientes y los datos de cada cliente.
            4. Escribe los datos en el PDF, creando nuevas páginas si es necesario.
            5. Guarda y abre el archivo PDF generado.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante la generación del informe.

            """
        ymax = 660
        ymin = 90
        ystep = 20
        xmin = 60

        try:
            rootPath = '.\\informes'
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            titulo = "Listado Clientes"
            fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            nomepdfcli = fecha + "_listadoclientes.pdf"
            pdf_path = os.path.join(rootPath, nomepdfcli)
            var.report = canvas.Canvas(pdf_path)

            items = ['DNI','APELLIDOS','NOMBRE','MOVIL','PROVINCIA','MUNICIPIO']
            var.report.setFont('Helvetica-Bold',size=10)
            var.report.drawString(55,680,str(items[0]))
            var.report.drawString(100,680,str(items[1]))
            var.report.drawString(200, 680, str(items[2]))
            var.report.drawString(285, 680, str(items[3]))
            var.report.drawString(360, 680, str(items[4]))
            var.report.drawString(450, 680, str(items[5]))
            var.report.line(40, 675, 540, 675)
            query = QtSql.QSqlQuery()
            query.exec("SELECT count(*) FROM clientes")
            if query.next():
                numRegistros = query.value(0)
                paginas = Informes.getMaxElementosPpag(ymax, ymin, ystep,numRegistros)
            Informes.topInforme(titulo, None)
            Informes.footInforme(titulo, paginas)

            query.prepare("SELECT dnicli, apelcli, nomecli, movilcli, provcli, municli from clientes order by apelcli")
            if query.exec():
                x = xmin
                y = ymax
                while query.next():
                    if y <= ymin:
                        var.report.setFont('Helvetica-Oblique',size=8)
                        var.report.drawString(450,80,"Página siguiente...")
                        var.report.showPage() #crea una pagina nueva
                        Informes.footInforme(titulo)
                        Informes.topInforme(titulo, None)
                        items = ['DNI', 'APELLIDOS', 'NOMBRE', 'MOVIL', 'PROVINCIA', 'MUNICIPIO']
                        var.report.setFont('Helvetica-Bold', size=10)
                        var.report.drawString(55, 680, str(items[0]))
                        var.report.drawString(100, 680, str(items[1]))
                        var.report.drawString(200, 680, str(items[2]))
                        var.report.drawString(285, 680, str(items[3]))
                        var.report.drawString(360, 680, str(items[4]))
                        var.report.drawString(450, 680, str(items[5]))
                        var.report.line(40, 675, 540, 675)
                        x = xmin
                        y = ymax


                    var.report.setFont('Helvetica',size=9)
                    dni = '***' + str(query.value(0)[3:6])  + '***'
                    var.report.drawCentredString(x + 5, y, str(dni))
                    var.report.drawString(x + 40, y, str(query.value(1)))
                    var.report.drawString(x + 140, y, str(query.value(2)))
                    var.report.drawString(x + 215, y, str(query.value(3)))
                    var.report.drawString(x + 300, y, str(query.value(4)))
                    var.report.drawString(x + 380, y, str(query.value(5)))
                    y -= ystep
            else:
                print(query.lastError().text())


            var.report.save()

            for file in os.listdir(rootPath):
                if file.endswith(nomepdfcli):
                    os.startfile(pdf_path)
        except Exception as e:
            print(e)

    @staticmethod
    def reportPropiedades(municipio):
        """
            Genera un informe en formato PDF con la lista de propiedades de un municipio específico.

            El informe incluye los campos: COD, DIRECCION, TIPO PROP., OPERACION, PRECIO ALQ., PRECIO VENTA.
            Se crea un archivo PDF en el directorio `.\informes` con el nombre `listadopropiedades` seguido de la fecha y hora actual.
            Si el número de registros excede el espacio disponible en una página, se crean páginas adicionales.

            Pasos:
            1. Crea el directorio `.\informes` si no existe.
            2. Genera el archivo PDF con el nombre basado en la fecha y hora actual.
            3. Consulta la base de datos para obtener el número de propiedades y los datos de cada propiedad.
            4. Escribe los datos en el PDF, creando nuevas páginas si es necesario.
            5. Guarda y abre el archivo PDF generado.

            Excepciones:
            - Captura y muestra cualquier excepción que ocurra durante la generación del informe.
            """
        try:
            ymax = 655
            ymin = 90
            ystep = 20
            xmin = 60

            rootPath = '.\\informes'
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            titulo = "Listado Propiedades"
            fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            nomepdfcli = fecha + "_listadopropiedades.pdf"
            pdf_path = os.path.join(rootPath, nomepdfcli)
            var.report = canvas.Canvas(pdf_path)

            items = ['COD','DIRECCION','TIPO PROP.','OPERACION','PRECIO ALQ.','PRECIO VENTA']
            var.report.setFont('Helvetica-Bold',size=10)
            var.report.drawString(55,680,str(items[0]))
            var.report.drawString(100,680,str(items[1]))
            var.report.drawString(210, 680, str(items[2]))
            var.report.drawString(295, 680, str(items[3]))
            var.report.drawString(380, 680, str(items[4]))
            var.report.drawString(460, 680, str(items[5]))
            var.report.line(40, 675, 540, 675)
            query = QtSql.QSqlQuery()
            query.prepare("SELECT count(*) FROM propiedades WHERE municipio = :municipio")
            query.bindValue(":municipio", municipio)
            if query.exec():
                if query.next():
                    numRegistros = query.value(0)
                    paginas = Informes.getMaxElementosPpag(ymax, ymin, ystep,numRegistros)
            Informes.topInforme(titulo, municipio)
            Informes.footInforme(titulo, paginas)


            query.prepare("SELECT codigo, direccion,tipo_propiedad, tipo_operacion, precio_alquiler, precio_venta from propiedades where municipio = :municipio order by municipio")
            query.bindValue(":municipio", str(municipio))
            if query.exec():
                x = xmin
                y = ymax
                while query.next():
                    if y <= ymin:
                        var.report.setFont('Helvetica-Oblique',size=8)
                        var.report.drawString(450,80,"Página siguiente...")
                        var.report.showPage() #crea una pagina nueva
                        Informes.footInforme(titulo)
                        Informes.topInforme(titulo, municipio)
                        items = ['COD','DIRECCION','TIPO PROP.','OPERACION','PRECIO ALQ.','PRECIO VENTA']
                        var.report.setFont('Helvetica-Bold',size=10)
                        var.report.drawString(55,680,str(items[0]))
                        var.report.drawString(100,680,str(items[1]))
                        var.report.drawString(210, 680, str(items[2]))
                        var.report.drawString(295, 680, str(items[3]))
                        var.report.drawString(380, 680, str(items[4]))
                        var.report.drawString(460, 680, str(items[5]))
                        var.report.line(40, 675, 540, 675)
                        x = xmin
                        y = ymax


                    var.report.setFont('Helvetica',size=9)
                    var.report.drawString(x + 5, y, str(query.value(0)))
                    var.report.drawString(x + 40, y, str(query.value(1)))
                    var.report.drawString(x + 150, y, str(query.value(2)))
                    operacion = query.value(3).replace("[","").replace("]","").replace("'","")
                    var.report.drawString(x + 240, y, str(operacion))
                    alquiler = "-" if not str(query.value(4)) else str(query.value(4))
                    var.report.drawRightString(x + 380, y, alquiler+" €")
                    compra = "-" if not str(query.value(5)) else str(query.value(5))
                    var.report.drawRightString(x + 470, y, compra+" €")
                    y -= ystep
            else:
                print(query.lastError().text())


            var.report.save()

            for file in os.listdir(rootPath):
                if file.endswith(nomepdfcli):
                    os.startfile(pdf_path)
        except Exception as e:
            print(e)

    @staticmethod
    def reportFact(idFactura):
        xidventa = 55
        xidpropiedad = xidventa + 35
        xdireccion = xidpropiedad + 50
        xlocalidad = xdireccion + 150
        xtipo = xlocalidad + 100
        xprecio = xtipo + 50
        try:
            if ((idFactura != None) and (idFactura != "")):
                rootPath = '.\\informes'
                if not os.path.exists(rootPath):
                    os.makedirs(rootPath)
                fecha = datetime.today()
                fecha = fecha.strftime("%Y_%m_%d_%H_%M_%S")
                nompdfcli = fecha + "_FacturaVentas.pdf"
                pdf_path = os.path.join(rootPath, nompdfcli)

                var.report = canvas.Canvas(pdf_path)
                titulo = "Factura Código " + idFactura
                listado_ventas = conexion.Conexion.listadoVentas(idFactura)
                factura = conexion.Conexion.cargaOneFactura(idFactura)
                cliente = conexion.Conexion.datosOneCliente(factura[2]) # ['20367722A', '27/07/2024', 'Fernández López', 'Manuel', 'fernandez.lopez@example.com', '602345678', 'Avenida de Castelao, 8', 'Pontevedra', 'Vigo', '']
                Informes.topInforme(titulo, cliente[8])
                Informes.topDatosCliente(cliente, factura[1])
                Informes.footInforme(titulo, 1)
                items = ["ID VENTA", "CÓDIGO", "DIRECCIÓN", "LOCALIDAD", "TIPO", "PRECIO"]
                Informes.footInforme(titulo, "1")
                var.report.setFont("Helvetica-Bold", size=10)
                var.report.drawString(55, 600, str(items[0]))
                var.report.drawString(110, 600, str(items[1]))
                var.report.drawString(160, 600, str(items[2]))
                var.report.drawString(290, 600, str(items[3]))
                var.report.drawString(390, 600, str(items[4]))
                var.report.drawString(440, 600, str(items[5]))
                var.report.line(50, 595, 525, 595)
                y = 580
                for registro in listado_ventas:
                    var.report.setFont("Helvetica", size=8)
                    var.report.drawCentredString(75, y, str(registro[0]))
                    var.report.drawCentredString(120, y, str(registro[1]).title())
                    var.report.drawString(170, y, str(registro[2]).title())
                    var.report.drawString(300, y, str(registro[3]).title())
                    var.report.drawString(390, y, str(registro[4]).title())
                    var.report.drawCentredString(470, y, str(registro[5]).title() + " €")
                    y -= 30

                var.report.save()

                for file in os.listdir(rootPath):
                    if file.endswith(nompdfcli):
                        os.startfile(pdf_path)
            else:
                mbox = eventos.Eventos.crearMensajeError("Error ifrome factura",
                                                         "No se ha seleccionado ninguna factura")
                mbox.exec()
        except Exception as e:
            print("Error reportFact = ", e)

    @staticmethod
    def reportReciboMensualidad(idAlquiler, idMensualidad):
        try:
            rootPath = '.\\informes'
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            titulo = "RECIBO MENSUALIDAD ALQUILER"
            fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            nomepdffac = fecha + "_recibo_alquiler_" + str(idAlquiler) + ".pdf"
            pdf_path = os.path.join(rootPath, nomepdffac)
            var.report = canvas.Canvas(pdf_path)

            datosAlq = conexion.Conexion.datosOneAlquiler(idAlquiler)
            fechaini = datosAlq[1]
            fechafin = datosAlq[2]
            idVendedor = str(datosAlq[3])
            dnicli = str(datosAlq[4])
            nomecli = str(datosAlq[5]) + " " + str(datosAlq[6])
            idProp = str(datosAlq[7])
            tipoprop = str(datosAlq[8])
            precioAlq = datosAlq[9]
            precioAlqStr = f"{precioAlq:,.1f} €"
            localidad = datosAlq[10]
            dirProp = datosAlq[11]

            var.report.drawString(55, 690, "DATOS CLIENTE:")
            var.report.drawString(100, 670, "DNI: " + dnicli)
            var.report.drawString(330, 670, "Nombre: " + nomecli)

            var.report.drawString(55, 640, "DATOS CONTRATO:")
            var.report.drawString(100, 620, "Num de contrato: " + str(idAlquiler))
            var.report.drawString(100, 600, "Num de vendedor: " + idVendedor)
            var.report.drawString(330, 620, "Fecha de inicio: " + fechaini)
            var.report.drawString(330, 600, "Fecha de fin: " + fechafin)

            var.report.drawString(55, 570, "DATOS INMUEBLE:")
            var.report.drawString(100, 550, "Num de propiedad: " + idProp)
            var.report.drawString(100, 530, "Tipo de propiedad: " + tipoprop)
            var.report.drawString(330, 550, "Dirección: " + dirProp)
            var.report.drawString(330, 530, "Localidad: " + localidad)

            var.report.line(40, 500, 540, 500)
            var.report.drawString(55, 470, "Mensualidad correspondiente a:")
            var.report.setFont('Helvetica-Bold', size=12)
            datos_mensualidad = conexion.Conexion.datosOneMensualidad(idMensualidad)
            estado_pago = datos_mensualidad[2]
            print("Estado de pago: ", estado_pago)# 0 = pendiente, 1 = pagado
            var.report.drawCentredString(300, 470, datos_mensualidad[1].upper())

            iva = precioAlq * 0.1
            total = precioAlq + iva

            var.report.setFont('Helvetica-Bold', size=10)
            var.report.drawString(370, 470, "Subtotal: ")
            var.report.drawRightString(540, 470, precioAlqStr)
            var.report.drawString(370, 450, "IVA (10%): ")
            var.report.drawRightString(540, 450, str(iva) + " €")
            var.report.setFont('Helvetica-Bold', size=12)
            var.report.drawString(370, 420, "Total: ")
            var.report.drawRightString(540, 420, str(total) + " €")
            var.report.line(40, 370, 540, 370)

            estado_pago_text = "PAGADA" if estado_pago == 1 else "PENDIENTE PAGO"
            estado_pago_color = "red" if estado_pago == 1 else "#CCCC00"
            var.report.setFont('Helvetica-Bold', size=18)
            var.report.setFillColor(estado_pago_color)
            var.report.drawCentredString(300, 380, estado_pago_text)
            var.report.setFillColor("black")

            Informes.topInformeAlquiler(titulo)
            Informes.footInforme(titulo, 1)

            var.report.save()
            for file in os.listdir(rootPath):
                if file.endswith(nomepdffac):
                    os.startfile(pdf_path)
        except Exception as e:
            print("Error en reportReciboMes", str(e))

    @staticmethod
    def getMaxElementosPpag(ymax, ymin, ystep, numRegistros):
        """
                Calcula el número máximo de elementos por página.

                Args:
                    ymax (int): Coordenada Y máxima.
                    ymin (int): Coordenada Y mínima.
                    ystep (int): Paso en Y entre elementos.
                    numRegistros (int): Número total de registros.

                Returns:
                    int: Número máximo de elementos por página.
                """
        numPpagina = math.ceil(numRegistros/(ymax - ymin) / ystep)
        return numPpagina

    def topInforme(titulo, municipio=None):
        """
            Dibuja la cabecera del informe PDF.

            Args:
                titulo (str): Título del informe.
                municipio (str): Nombre del municipio (opcional).

            Excepciones:
                - Captura y muestra cualquier excepción que ocurra durante el dibujo de la cabecera.
            """
        try:
            if municipio:
                municipio = municipio.upper()
            ruta_logo = '.\\img\\icono.png'
            logo = Image.open(ruta_logo)

            ruta_letras = '.\\img\\nombre-02.png'
            letras = Image.open(ruta_letras)
            # drawing = svg2rlg(svg_file)  PARA FICHERO SVG
            # renderP.drawToFile(drawing, "temp_image.png", fmt="PNG")
            # logo = QPixmap("temp_image.png")

            # Asegúrate de que el objeto 'logo' sea de tipo 'PngImageFile'
            if isinstance(logo, Image.Image) and isinstance(letras, Image.Image):
                var.report.drawImage(ruta_letras, 230, 790, width=120, height=60)
                var.report.line(40, 800, 540, 800)
                var.report.setFont('Helvetica-Bold', size=14)
                var.report.drawString(55, 785, 'InmoTeis')
                if municipio:
                    var.report.drawCentredString(110, 685, titulo)
                    var.report.drawCentredString(110, 665, municipio)
                else:
                    var.report.drawString(230, 715, titulo)
                var.report.line(40, 645, 540, 645)


                # Dibuja la imagen en el informe
                var.report.drawImage(ruta_logo, 480, 750, width=40, height=40)

                var.report.setFont('Helvetica', size=9)
                var.report.drawString(230, 772, 'CIF: A12345678')
                var.report.drawString(55, 772, 'Avda. Galicia - 101')
                var.report.drawString(55, 757, 'Vigo - 36216 - España')
                var.report.drawString(360, 772, 'Teléfono: 986 41 52 63')
                var.report.drawString(360, 757, 'e-mail: inmoteis@iesteis.es')
            else:
                print(f'Error: No se pudo cargar la imagen en {ruta_logo} o en {ruta_letras}')
        except Exception as error:
            print('Error en cabecera informe:', error)

    def topInformeAlquiler(titulo, municipio=None):
        """
            Dibuja la cabecera del informe PDF.

            Args:
                titulo (str): Título del informe.
                municipio (str): Nombre del municipio (opcional).

            Excepciones:
                - Captura y muestra cualquier excepción que ocurra durante el dibujo de la cabecera.
            """
        try:
            if municipio:
                municipio = municipio.upper()
            ruta_logo = '.\\img\\icono.png'
            logo = Image.open(ruta_logo)

            ruta_letras = '.\\img\\nombre-02.png'
            letras = Image.open(ruta_letras)
            # drawing = svg2rlg(svg_file)  PARA FICHERO SVG
            # renderP.drawToFile(drawing, "temp_image.png", fmt="PNG")
            # logo = QPixmap("temp_image.png")

            # Asegúrate de que el objeto 'logo' sea de tipo 'PngImageFile'
            if isinstance(logo, Image.Image) and isinstance(letras, Image.Image):
                var.report.drawImage(ruta_letras, 230, 790, width=120, height=60)
                var.report.line(40, 800, 540, 800)
                var.report.setFont('Helvetica-Bold', size=14)
                var.report.drawString(55, 785, 'InmoTeis')
                if municipio:
                    var.report.drawCentredString(110, 685, titulo)
                    var.report.drawCentredString(110, 665, municipio)
                else:
                    var.report.drawString(230, 715, titulo)
                var.report.line(40, 740, 540, 740)


                # Dibuja la imagen en el informe
                var.report.drawImage(ruta_logo, 480, 750, width=40, height=40)

                var.report.setFont('Helvetica', size=9)
                var.report.drawString(230, 772, 'CIF: A12345678')
                var.report.drawString(55, 772, 'Avda. Galicia - 101')
                var.report.drawString(55, 757, 'Vigo - 36216 - España')
                var.report.drawString(360, 772, 'Teléfono: 986 41 52 63')
                var.report.drawString(360, 757, 'e-mail: inmoteis@iesteis.es')
            else:
                print(f'Error: No se pudo cargar la imagen en {ruta_logo} o en {ruta_letras}')
        except Exception as error:
            print('Error en cabecera informe:', error)

    def footInforme(titulo, paginas):
        """
            Dibuja el pie de página del informe PDF.

            Args:
                titulo (str): Título del informe.
                paginas (int): Número total de páginas.

            Excepciones:
                - Captura y muestra cualquier excepción que ocurra durante el dibujo del pie de página.
            """
        try:
            total_pages = 0
            var.report.line(40, 50, 540, 50)
            fecha = datetime.today().strftime('%d-%m-%Y %H:%M:%S')
            var.report.setFont('Helvetica-Oblique', size=7)
            var.report.drawString(50, 40, str(fecha))
            var.report.drawString(250, 40, str(titulo))
            var.report.drawString(490, 40, str('Página %s' % var.report.getPageNumber() + '/' + str(paginas)))

        except Exception as error:
            print('Error en pie informe de cualquier tipo: ', error)

    @staticmethod
    def topDatosCliente(cliente, fecha):
        try:
            var.report.setFont('Helvetica-Bold', size=8)
            var.report.drawString(300, 710, 'DNI Cliente:')
            var.report.drawString(300, 692, 'Nombre:')
            var.report.drawString(300, 674, 'Dirección:')
            var.report.drawString(300, 656, 'Localidad:')
            var.report.drawString(55, 622, "Fecha Factura:")
            var.report.setFont('Helvetica', size=8)
            var.report.drawString(360, 710, cliente[0])
            var.report.drawString(360, 692, cliente[3] + " " + cliente[2])
            var.report.drawString(360, 674, cliente[6])
            var.report.drawString(360, 656, cliente[8])
            var.report.drawString(120, 622, fecha)
        except Exception as error:
            print('Error en cabecera informe:', error)

if __name__ == '__main__':
    Informes.reportClientes()