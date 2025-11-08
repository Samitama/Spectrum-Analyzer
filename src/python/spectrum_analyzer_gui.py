from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import serial
import serial.tools.list_ports
import sys

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spectrum Analyzer")
        self.resize(600, 400)
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.layout = QtWidgets.QGridLayout(self.centralwidget)
        self.graphicsView = PlotWidget(self.centralwidget)
        self.layout.addWidget(self.graphicsView, 0, 0, 1, 5)

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.layout.addWidget(self.comboBox, 1, 0, 1, 1)

        self.label = QtWidgets.QLabel("COM PORT", self.centralwidget)
        self.layout.addWidget(self.label, 1, 1, 1, 1)

        self.comboBox2 = QtWidgets.QComboBox(self.centralwidget)
        self.layout.addWidget(self.comboBox2, 1, 2, 1, 1)

        self.label_2 = QtWidgets.QLabel("Baudrate", self.centralwidget)
        self.layout.addWidget(self.label_2, 1, 3, 1, 1)

        self.pushButton = QtWidgets.QPushButton("Connect", self.centralwidget)
        self.layout.addWidget(self.pushButton, 1, 4, 1, 1)

        self.pushButton.clicked.connect(self.toggle_connection)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)

        self.load_serial_comports()
        self.baudrate_selection()

        self.x = []
        self.y = []
        self.index = 0
        self.curve = self.graphicsView.plot(pen=pg.mkPen('y', width=4))

        self.ser = None
        self.connected = False

    def load_serial_comports(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.comboBox.addItem(port.device)

    def baudrate_selection(self):
        for baud in ["9600", "19200", "38400", "57600", "115200"]:
            self.comboBox2.addItem(baud)

    def toggle_connection(self):
        if self.connected:
            if self.ser and self.ser.is_open:
                self.ser.close()
            self.pushButton.setText("Connect")
            self.connected = False
        else:
            try:
                port = self.comboBox.currentText()
                baud = int(self.comboBox2.currentText())
                self.ser = serial.Serial(port, baudrate=baud, timeout=1)
                self.timer.start(20)
                self.connected = True
                self.pushButton.setText("Disconnect")
                print(f"{port} portuna bağlanıldı.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Hata", f"Bağlantı kurulamadı:\n{e}")
                self.connected = False

    def update_plot(self):
        if self.ser and self.ser.is_open:
            try:
                MAX_POINTS = 500  # çizilecek maksimum veri
                line = self.ser.readline().decode("utf-8").strip()
                print(f"Gelen veri: {line}")  # Debug için
                value = int(line)
                self.x.append(self.index)
                self.y.append(value)
                self.index += 1

                if len(self.x) >= MAX_POINTS:
                    self.x = self.x[-500:]
                    self.y = self.y[-500:]

                self.curve.setData(self.x,self.y)
                self.graphicsView.setYRange(0,1023)
                self.graphicsView.setXRange(self.x[0], self.x[-1])
            except Exception as e:
                print("Veri okuma hatası:", e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
