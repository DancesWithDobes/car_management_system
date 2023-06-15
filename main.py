import sys
from PyQt5 import QtWidgets, QtCore
import sqlite3


class CarManagementSystem(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Car Management System")

        self.initialize_database()

        self.cars_tablewidget = QtWidgets.QTableWidget()
        self.cars_tablewidget.setColumnCount(5)
        self.cars_tablewidget.setHorizontalHeaderLabels(["Make", "Model", "Year", "Color", "License Plate"])
        self.cars_tablewidget.cellClicked.connect(self.view_car_details)

        self.add_vehicle_button = QtWidgets.QPushButton("Add Vehicle")
        self.remove_vehicle_button = QtWidgets.QPushButton("Remove Vehicle")
        self.add_maintenance_button = QtWidgets.QPushButton("Add Maintenance")
        self.remove_maintenance_button = QtWidgets.QPushButton("Remove Maintenance")
        self.add_incident_button = QtWidgets.QPushButton("Add Incident")
        self.remove_incident_button = QtWidgets.QPushButton("Remove Incident")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.add_vehicle_button)
        button_layout.addWidget(self.remove_vehicle_button)
        button_layout.addWidget(self.add_maintenance_button)
        button_layout.addWidget(self.remove_maintenance_button)
        button_layout.addWidget(self.add_incident_button)
        button_layout.addWidget(self.remove_incident_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.cars_tablewidget)
        main_layout.addLayout(button_layout)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.load_cars()

        self.add_vehicle_button.clicked.connect(self.add_vehicle)
        self.remove_vehicle_button.clicked.connect(self.remove_vehicle)
        self.add_maintenance_button.clicked.connect(self.add_maintenance)
        self.remove_maintenance_button.clicked.connect(self.remove_maintenance)
        self.add_incident_button.clicked.connect(self.add_incident)
        self.remove_incident_button.clicked.connect(self.remove_incident)

    def initialize_database(self):
        conn = sqlite3.connect("car_management.db")
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS cars (id INTEGER PRIMARY KEY AUTOINCREMENT, make TEXT, model TEXT, year INTEGER, color TEXT, license_plate TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS maintenance (id INTEGER PRIMARY KEY AUTOINCREMENT, car_id INTEGER, maintenance_type TEXT, FOREIGN KEY (car_id) REFERENCES cars(id))")
        cursor.execute("CREATE TABLE IF NOT EXISTS incidents (id INTEGER PRIMARY KEY AUTOINCREMENT, car_id INTEGER, description TEXT, FOREIGN KEY (car_id) REFERENCES cars(id))")

        conn.commit()
        conn.close()

    def load_cars(self):
        conn = sqlite3.connect("car_management.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM cars")
        cars = cursor.fetchall()

        self.cars_tablewidget.setRowCount(len(cars))
        for row, car in enumerate(cars):
            make_item = QtWidgets.QTableWidgetItem(car[1])
            model_item = QtWidgets.QTableWidgetItem(car[2])
            year_item = QtWidgets.QTableWidgetItem(str(car[3]))
            color_item = QtWidgets.QTableWidgetItem(car[4])
            license_plate_item = QtWidgets.QTableWidgetItem(car[5])

            self.cars_tablewidget.setItem(row, 0, make_item)
            self.cars_tablewidget.setItem(row, 1, model_item)
            self.cars_tablewidget.setItem(row, 2, year_item)
            self.cars_tablewidget.setItem(row, 3, color_item)
            self.cars_tablewidget.setItem(row, 4, license_plate_item)

        conn.close()

    def view_car_details(self, row, column):
        license_plate = self.cars_tablewidget.item(row, 4).text()

        maintenance_dialog = MaintenanceDialog(license_plate)
        maintenance_dialog.exec_()

        incident_dialog = IncidentDialog(license_plate)
        incident_dialog.exec_()

    def add_vehicle(self):
        dialog = AddVehicleDialog()
        if dialog.exec_():
            make = dialog.make_input.text()
            model = dialog.model_input.text()
            year = int(dialog.year_input.text())
            color = dialog.color_input.text()
            license_plate = dialog.license_plate_input.text()

            conn = sqlite3.connect("car_management.db")
            cursor = conn.cursor()

            cursor.execute("INSERT INTO cars (make, model, year, color, license_plate) VALUES (?, ?, ?, ?, ?)",
                           (make, model, year, color, license_plate))

            conn.commit()
            conn.close()

            self.load_cars()

    def remove_vehicle(self):
        selected_row = self.cars_tablewidget.currentRow()
        if selected_row >= 0:
            license_plate = self.cars_tablewidget.item(selected_row, 4).text()

            conn = sqlite3.connect("car_management.db")
            cursor = conn.cursor()

            cursor.execute("DELETE FROM cars WHERE license_plate = ?", (license_plate,))

            conn.commit()
            conn.close()

            self.load_cars()

    def add_maintenance(self):
        selected_row = self.cars_tablewidget.currentRow()
        if selected_row >= 0:
            license_plate = self.cars_tablewidget.item(selected_row, 4).text()

            dialog = AddMaintenanceDialog(license_plate)
            if dialog.exec_():
                maintenance_type = dialog.maintenance_type_input.text()

                conn = sqlite3.connect("car_management.db")
                cursor = conn.cursor()

                cursor.execute("SELECT id FROM cars WHERE license_plate = ?", (license_plate,))
                car_id = cursor.fetchone()[0]

                cursor.execute("INSERT INTO maintenance (car_id, maintenance_type) VALUES (?, ?)", (car_id, maintenance_type))

                conn.commit()
                conn.close()

    def remove_maintenance(self):
        selected_row = self.cars_tablewidget.currentRow()
        if selected_row >= 0:
            license_plate = self.cars_tablewidget.item(selected_row, 4).text()

            maintenance_dialog = MaintenanceDialog(license_plate)
            selected_maintenance = maintenance_dialog.selected_maintenance()

            if selected_maintenance:
                conn = sqlite3.connect("car_management.db")
                cursor = conn.cursor()

                cursor.execute("SELECT id FROM cars WHERE license_plate = ?", (license_plate,))
                car_id = cursor.fetchone()[0]

                cursor.execute("DELETE FROM maintenance WHERE car_id = ? AND maintenance_type = ?", (car_id, selected_maintenance))

                conn.commit()
                conn.close()

    def add_incident(self):
        selected_row = self.cars_tablewidget.currentRow()
        if selected_row >= 0:
            license_plate = self.cars_tablewidget.item(selected_row, 4).text()

            dialog = AddIncidentDialog(license_plate)
            if dialog.exec_():
                description = dialog.description_input.text()

                conn = sqlite3.connect("car_management.db")
                cursor = conn.cursor()

                cursor.execute("SELECT id FROM cars WHERE license_plate = ?", (license_plate,))
                car_id = cursor.fetchone()[0]

                cursor.execute("INSERT INTO incidents (car_id, description) VALUES (?, ?)", (car_id, description))

                conn.commit()
                conn.close()

    def remove_incident(self):
        selected_row = self.cars_tablewidget.currentRow()
        if selected_row >= 0:
            license_plate = self.cars_tablewidget.item(selected_row, 4).text()

            incident_dialog = IncidentDialog(license_plate)
            selected_incident = incident_dialog.selected_incident()

            if selected_incident:
                conn = sqlite3.connect("car_management.db")
                cursor = conn.cursor()

                cursor.execute("SELECT id FROM cars WHERE license_plate = ?", (license_plate,))
                car_id = cursor.fetchone()[0]

                cursor.execute("DELETE FROM incidents WHERE car_id = ? AND description = ?", (car_id, selected_incident))

                conn.commit()
                conn.close()


class AddVehicleDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Vehicle")

        self.make_label = QtWidgets.QLabel("Make:")
        self.make_input = QtWidgets.QLineEdit()

        self.model_label = QtWidgets.QLabel("Model:")
        self.model_input = QtWidgets.QLineEdit()

        self.year_label = QtWidgets.QLabel("Year:")
        self.year_input = QtWidgets.QLineEdit()

        self.color_label = QtWidgets.QLabel("Color:")
        self.color_input = QtWidgets.QLineEdit()

        self.license_plate_label = QtWidgets.QLabel("License Plate:")
        self.license_plate_input = QtWidgets.QLineEdit()

        self.add_button = QtWidgets.QPushButton("Add")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.cancel_button)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.make_label, self.make_input)
        form_layout.addRow(self.model_label, self.model_input)
        form_layout.addRow(self.year_label, self.year_input)
        form_layout.addRow(self.color_label, self.color_input)
        form_layout.addRow(self.license_plate_label, self.license_plate_input)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.add_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)


class AddMaintenanceDialog(QtWidgets.QDialog):
    def __init__(self, license_plate):
        super().__init__()

        self.setWindowTitle("Add Maintenance")

        self.maintenance_type_label = QtWidgets.QLabel("Maintenance Type:")
        self.maintenance_type_input = QtWidgets.QLineEdit()

        self.add_button = QtWidgets.QPushButton("Add")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.cancel_button)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.maintenance_type_label, self.maintenance_type_input)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.add_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)


class AddIncidentDialog(QtWidgets.QDialog):
    def __init__(self, license_plate):
        super().__init__()

        self.setWindowTitle("Add Incident")

        self.description_label = QtWidgets.QLabel("Description:")
        self.description_input = QtWidgets.QLineEdit()

        self.add_button = QtWidgets.QPushButton("Add")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.cancel_button)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.description_label, self.description_input)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.add_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)


class MaintenanceDialog(QtWidgets.QDialog):
    def __init__(self, license_plate):
        super().__init__()

        self.setWindowTitle("Maintenance")

        self.maintenance_listwidget = QtWidgets.QListWidget()

        self.view_button = QtWidgets.QPushButton("View")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.view_button)
        button_layout.addWidget(self.cancel_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.maintenance_listwidget)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.load_maintenance(license_plate)

        self.view_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def load_maintenance(self, license_plate):
        conn = sqlite3.connect("car_management.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM cars WHERE license_plate = ?", (license_plate,))
        car_id = cursor.fetchone()[0]

        cursor.execute("SELECT maintenance_type FROM maintenance WHERE car_id = ?", (car_id,))
        maintenance_records = cursor.fetchall()

        self.maintenance_listwidget.clear()
        for record in maintenance_records:
            maintenance_item = QtWidgets.QListWidgetItem(record[0])
            self.maintenance_listwidget.addItem(maintenance_item)

        conn.close()

    def selected_maintenance(self):
        selected_item = self.maintenance_listwidget.currentItem()
        if selected_item:
            return selected_item.text()
        return None


class IncidentDialog(QtWidgets.QDialog):
    def __init__(self, license_plate):
        super().__init__()

        self.setWindowTitle("Incidents")

        self.incident_listwidget = QtWidgets.QListWidget()

        self.view_button = QtWidgets.QPushButton("View")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.view_button)
        button_layout.addWidget(self.cancel_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.incident_listwidget)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.load_incidents(license_plate)

        self.view_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def load_incidents(self, license_plate):
        conn = sqlite3.connect("car_management.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM cars WHERE license_plate = ?", (license_plate,))
        car_id = cursor.fetchone()[0]

        cursor.execute("SELECT description FROM incidents WHERE car_id = ?", (car_id,))
        incident_records = cursor.fetchall()

        self.incident_listwidget.clear()
        for record in incident_records:
            incident_item = QtWidgets.QListWidgetItem(record[0])
            self.incident_listwidget.addItem(incident_item)

        conn.close()

    def selected_incident(self):
        selected_item = self.incident_listwidget.currentItem()
        if selected_item:
            return selected_item.text()
        return None


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = CarManagementSystem()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
