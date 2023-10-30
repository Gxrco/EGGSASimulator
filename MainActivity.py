from PyQt5 import uic
from PyQt5.QtGui import(
    QStandardItemModel,
    QStandardItem,
    QPixmap,
)
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QDialog,
    QLineEdit,
    QComboBox,
    QPushButton,
    QListView,
    QGraphicsScene,
    QGraphicsPixmapItem
)
import math

class DataManager:
    def __init__(self):
        self.devices = []
        self.IMax = 0
        self.PotenciaMax = 0

    def add_device(self, device):
        if len(self.devices) >= 10:
            return False  # Device limit reached
        self.devices.append(device)
        return True  # Device added successfully

    def get_devices(self):
        return self.devices
    
    def get_IMax(self):
        return self.IMax
    
    def set_IMax(self, value):
        self.IMax = value
    
    def get_PotenciaMax(self):
        return self.PotenciaMax
    
    def set_PotenciaMax(self, value):
        self.PotenciaMax = value
    
    def remove_device(self, device_name):
        for device in self.devices:
            if device.name == device_name:
                self.devices.remove(device)
                break

class Device:
    def __init__(self, name, image, voltage, current, power, usage_time):
        self.name = name
        self.image = image
        self.voltage = voltage
        self.current = current
        self.power = power
        self.usage_time = usage_time
        self.energy = float(power)*float(usage_time)/1000

class AddElements(QDialog):
    def __init__(self, data_manager):
        super().__init__()
        uic.loadUi('AddElements.ui', self)
        self.setWindowTitle("Agregar nuevo dispositivo")

        self.data_manager = data_manager

        self.cmbDispositivo = self.findChild(QComboBox, 'cmbDispositivo')
        self.txtVoltaje = self.findChild(QLineEdit, 'txtVoltaje')
        self.txtCorriente = self.findChild(QLineEdit, 'txtCorriente')
        self.txtPotencia = self.findChild(QLineEdit, 'txtPotencia')
        self.txtTiempoUso = self.findChild(QLineEdit, 'txtTiempoUso')

        self.populate_combo_box()

        self.btnAgregar.clicked.connect(self.extractData)
        self.btnCerrar.clicked.connect(self.close)
        self.btnLimpiar.clicked.connect(self.clearFields)


    def extractData(self):
        voltaje = float(self.txtVoltaje.text())
        corriente = float(self.txtCorriente.text())
        potencia = float(self.txtPotencia.text())
        tiempoUso = float(self.txtTiempoUso.text())
        name = self.cmbDispositivo.currentText()

        if voltaje * corriente == potencia:
            if self.data_manager.add_device(Device(name, self.getImage(name), voltaje, corriente, potencia, tiempoUso)):
                pass
            else:
                self.show_error_message("Error", "Se ha alcanzado el límite de dispositivos (10).")
        else:
            self.show_error_message("Error de potencia", "La potencia no coincide con la corriente y voltaje")


    def show_error_message(self, title, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.exec_()

    def getImage(self, name):
        appliance_images = {
            "Refrigerador": "src/fridge.png",
            "Lavadora": "src/lavadora.png",
            "Secadora de ropa": "src/secadora.png",
            "Lavavajillas": "src/lavavajillas.png",
            "Horno de microondas": "src/microondas.png",
            "Horno eléctrico": "src/horno.png",
            "Cafetera eléctrica": "src/cafetera.png",
            "Tostadora": "src/tostadora.png",
            "Batidora": "src/batidora.png",
            "Licuadora": "src/licuadora.png",
            "Freidora eléctrica": "src/freidora.png",
            "Aspiradora": "src/aspiradora.png",
            "Plancha eléctrica": "src/plancha.png",
            "Televisor": "src/televisor.png",
            "Computadora portátil": "src/laptop.png",
            "Teléfono móvil": "src/celular.png",
            "Tableta": "src/tablet.png",
            "Cámara digital": "src/camara.png",
            "Reproductor de DVD/Blu-ray": "src/display.png",
            "Horno tostador eléctrico": "src/toaster.png"
        }

        if name in appliance_images:
            return appliance_images[name]
        else:
            return "path_to_default_image.png"

    def populate_combo_box(self):
        items = [
        "Refrigerador",
        "Lavadora",
        "Secadora de ropa",
        "Lavavajillas",
        "Horno de microondas",
        "Horno eléctrico",
        "Cafetera eléctrica",
        "Tostadora",
        "Batidora",
        "Licuadora",
        "Freidora eléctrica",
        "Aspiradora",
        "Plancha eléctrica",
        "Televisor",
        "Computadora portátil",
        "Teléfono móvil",
        "Tableta",
        "Cámara digital",
        "Reproductor de DVD/Blu-ray",
        "Horno tostador eléctrico"]

        self.cmbDispositivo.clear()
        self.cmbDispositivo.addItems(items)

    def clearFields(self):
        self.txtVoltaje.clear()
        self.txtCorriente.clear()
        self.txtPotencia.clear()
        self.txtTiempoUso.clear()

class DeleteElements(QDialog):
    def __init__(self, data_manager):
        super().__init__()
        uic.loadUi('DeleteElements.ui', self)
        self.setWindowTitle("Gestionar lista")
    
        self.data_manager = data_manager

        self.lstDispositivos = self.findChild(QListView, 'lstDispositivos')
        self.btnEliminar = self.findChild(QPushButton, 'btnEliminar')

        self.btnEliminar.clicked.connect(self.delete_device)

        self.load_device_list()

    def load_device_list(self):
        devices = self.data_manager.get_devices()

        list_model = QStandardItemModel()
        for device in devices:
            item = QStandardItem(device.name)
            list_model.appendRow(item)

        self.lstDispositivos.setModel(list_model)

    def delete_device(self):

        selected_item = self.lstDispositivos.currentIndex()
        if selected_item.isValid():
            
            device_name = selected_item.data()
            self.data_manager.remove_device(device_name)
            self.load_device_list()

class MainWindow(QMainWindow):
    def __init__(self, data_manager):
        super().__init__()
        uic.loadUi('MainView.ui', self)
        self.setWindowTitle("Ejercicio 5 - Física III")
        self.data_manager = data_manager

        self.actionAgregar.triggered.connect(self.open_add_elements)
        self.actionGestionar.triggered.connect(self.open_delete_elements)

        self.btnResultados.clicked.connect(self.PerformResult)
        self.btnCalcular.clicked.connect(self.CableResult)
        self.btnResultados.clicked.connect(self.loadTopology)

        self.scene = QGraphicsScene(self.graphVentana)
        
        self.loadTopology()

        self.graphVentana.setScene(self.scene)

    def loadTopology(self):
        self.scene.clear()

        x_offset = 50
        y_offset = 30
        spacing = 150
        fixed_size = 50  # Tamaño cuadrado fijo para todas las imágenes

        # Dibujar la línea central del bus
        self.scene.addLine(x_offset, y_offset + fixed_size + 50, x_offset + len(self.data_manager.get_devices()) * spacing, y_offset + fixed_size + 50)

        for index, device in enumerate(self.data_manager.get_devices()):
            pixmap = QPixmap(device.image).scaled(fixed_size, fixed_size)  # Escalar la imagen al tamaño fijo
            pixmap_item = QGraphicsPixmapItem(pixmap)
            pixmap_item.setPos(x_offset + index * spacing, y_offset)
            self.scene.addItem(pixmap_item)

            # Dibujar líneas verticales que conectan cada dispositivo al bus
            self.scene.addLine(x_offset + index * spacing + fixed_size // 2, y_offset + fixed_size, 
                               x_offset + index * spacing + fixed_size // 2, y_offset + fixed_size + 50)

    def PerformResult(self):
        list = self.data_manager.get_devices()
        if(len(list) != 0):
            EnergiaTotal = 0
            for item in list:
                EnergiaTotal += item.energy
                if self.data_manager.get_IMax() < item.energy:
                    self.data_manager.set_IMax(item.energy)
                    self.data_manager.set_PotenciaMax(item.power)

            #Dado KWh
            energiaMensual = EnergiaTotal*30
            preciodia=EnergiaTotal*1.474041
            #Factura mensual
            preciomes=preciodia*30

            EnergiaMensual="{:.2f}".format(energiaMensual)
            PrecioMes="{:.2f}".format(preciomes)

            self.txtConsumo.setText(str(EnergiaMensual))
            self.txtCosto.setText(str(PrecioMes))
            self.txtTipo.setText("Baja tensión simple")

    def CableResult(self):
        longitud = self.txtLongitud.text()
        if( longitud != ''):
            pi = math.pi
            Dcms=2*self.data_manager.get_IMax()*math.sqrt(1.72*float(longitud))/(10*10*math.sqrt(pi*self.data_manager.get_PotenciaMax()))

            self.txtCalibre.setText(self.recommend_cable_calibre(Dcms))
        
    def recommend_cable_calibre(self, Dcms):
        if Dcms < 0.163:
            return "14"
        elif 0.163 < Dcms < 0.205:
            return "12"
        elif 0.205 < Dcms < 0.259:
            return "10"
        elif 0.259 < Dcms < 0.326:
            return "8"
        elif 0.326 < Dcms < 0.412:
            return "6"
        elif 0.412 < Dcms < 0.462:
            return "5"
        elif 0.462 < Dcms < 0.519:
            return "4"
        else:
            return "Mayor a lo establecido (>4)"

    def open_add_elements(self):
        dialog = AddElements(data_manager)
        dialog.exec_()

    def open_delete_elements(self):
        dialog = DeleteElements(data_manager)
        dialog.exec_()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    data_manager = DataManager()
    window = MainWindow(data_manager)
    window.show()
    sys.exit(app.exec_())
