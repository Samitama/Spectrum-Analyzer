import sys
import serial 
from PyQt5 import QtWidgets, uic
import serial.tools.list_ports

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("spectrum_analyzer.ui", self)
        self.setWindowTitle("Spectrum Analyzer")
        self.load_serial_comports()
        self.baudrate_selection()
        self.pushButton.clicked.connect(self.comport_connection)

    def load_serial_comports(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.comboBox.addItem(f"{port.device}")

    def baudrate_selection(self):
        baudrates = ["9600","19200","38400","57600","115200"]
        for baud in baudrates:
            self.comboBox2.addItem(f"{baud}")

    def comport_connection(self):
        port = self.comboBox.currentText()
        baud = self.comboBox2.currentText()
        if port and baud:
            print(f"{port} ile {baud} secilmistir")
            self.ser = serial.Serial(port,baudrate=int(baud))
            

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()